import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const repo=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const root=path.resolve(repo,process.argv[2]||'.');
const manifest=JSON.parse(fs.readFileSync(path.join(repo,'scripts/media-manifest.json'),'utf8'));
for(const item of Object.values(manifest.images))if(item.optimized){
 const dest=path.join(root,item.optimized),source=path.join(repo,item.optimized);
 if(dest!==source&&!fs.existsSync(dest)){fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(source,dest);}
}
const attr=(tag,key)=>tag.match(new RegExp(`\\s${key}\\s*=\\s*(["'])(.*?)\\1`,'i'))?.[2];
const set=(tag,key,value)=>new RegExp(`\\s${key}\\s*=`,'i').test(tag)?tag.replace(new RegExp(`(\\s${key}\\s*=\\s*)(["'])(.*?)\\2`,'i'),`$1"${value}"`):tag.replace(/\s*\/?>$/,end=>` ${key}="${value}"${end}`);
let pages=0,images=0,dimensions=0,optimized=0;
const sizing='<style id="intrinsic-media-sizing">:where(img[data-intrinsic-size]){height:auto}</style>';
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){
 if(['.git','.vercel','node_modules','scripts','dist','public','.next','__pycache__'].includes(e.name))continue;
 const f=path.join(dir,e.name);if(e.isDirectory()){walk(f);continue;}if(!e.name.endsWith('.html'))continue;
 let text=fs.readFileSync(f,'utf8');const before=text;
 text=text.replace(/<img\b[^>]*>/gi,tag=>{
  const src=attr(tag,'src');if(!src)return tag;
  let key=src;
  if(src.startsWith('/')&&!src.startsWith('//'))key=src.split(/[?#]/)[0];
  else if(!/^(https?:|data:|\/\/)/i.test(src))key='/'+path.relative(root,path.resolve(path.dirname(f),src)).split(path.sep).join('/');
  const item=manifest.images[key];if(!item)return tag;
  images++;
  // Existing explicit layout dimensions belong to the page design.
  if(!attr(tag,'width')&&!attr(tag,'height')){tag=set(set(set(tag,'width',item.width),'height',item.height),'data-intrinsic-size','true');dimensions++;}
  if(item.optimized&&key!==item.optimized){
   if(!fs.existsSync(path.join(root,item.optimized)))throw new Error(`Missing optimized image ${item.optimized}`);
   tag=set(tag,'src',item.optimized);optimized++;
  }
  if(!attr(tag,'decoding'))tag=set(tag,'decoding','async');
  if((manifest.autoWidthClasses||[]).some(c=>(attr(tag,'class')||'').split(/\s+/).includes(c))&&!/\bwidth\s*:\s*auto\b/.test(attr(tag,'style')||''))tag=set(tag,'style',(attr(tag,'style')||'')+';width:auto');
  if(attr(tag,'loading')==='eager'&&!attr(tag,'fetchpriority'))tag=set(tag,'fetchpriority','high');
  return tag;
 });
 if(text.includes('data-intrinsic-size=')&&!text.includes('id="intrinsic-media-sizing"'))text=text.replace(/<\/head>/i,sizing+'\n</head>');
 // The homepage portrait is visible in the hero and must not wait for lazy loading.
 if(path.relative(root,f)==='index.html'&&manifest.eagerHomepageSource){
  text=text.replace(/<img\b[^>]*>/gi,tag=>{const src=attr(tag,'src');const original=manifest.eagerHomepageSource;const item=manifest.images[original];return src===original||src===item?.optimized?set(set(tag,'loading','eager'),'fetchpriority','high'):tag;});
 }
 if(text!==before){fs.writeFileSync(f,text);pages++;}
}}
walk(root);console.log(JSON.stringify({pages,images,dimensions,optimized}));
