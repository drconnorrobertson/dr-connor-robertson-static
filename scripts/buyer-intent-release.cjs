const fs=require('fs'),path=require('path');
const root=process.argv[2]||'.';
const config=require('./buyer-intent-pages.json');
const escape=s=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
for(const [file,c] of Object.entries(config)){
 const p=path.join(root,file);let html=fs.readFileSync(p,'utf8');
 html=html.replace(/<title>[\s\S]*?<\/title>/i,'<title>'+escape(c.title)+'</title>');
 const meta=(key,value)=>{let found=false;html=html.replace(/<meta\b[^>]*>/gi,tag=>{const m=tag.match(/(?:name|property)\s*=\s*["']([^"']+)["']/i);if(!m||m[1].toLowerCase()!==key)return tag;found=true;return tag.replace(/content\s*=\s*(["'])[\s\S]*?\1/i,'content="'+escape(value)+'"');});if(!found)html=html.replace(/<\/head>/i,'<meta name="'+key+'" content="'+escape(value)+'">\n</head>');};
 meta('description',c.description);meta('og:title',c.title);meta('og:description',c.description);meta('twitter:title',c.title);meta('twitter:description',c.description);
 html=html.replace(/<!-- buyer-intent-release:start -->[\s\S]*?<!-- buyer-intent-release:end -->/g,'');
 const h=/<h1\b/i.test(html)?'h2':'h1';
 const section='<!-- buyer-intent-release:start --><section class="section buyer-intent-release" aria-labelledby="buyer-next-step"><div class="wrap container prose"><'+h+' id="buyer-next-step">'+escape(c.heading)+'</'+h+'>'+c.body+'</div></section><!-- buyer-intent-release:end -->';
 if(/<\/main>/i.test(html))html=html.replace(/<\/main>/i,section+'</main>');else if(/<footer\b/i.test(html))html=html.replace(/<footer\b/i,section+'<footer');else html=html.replace(/<\/body>/i,section+'</body>');
 fs.writeFileSync(p,html);
 console.log('Buyer intent updated: '+p);
}
