"""Verify recovered article intent, metadata, dates, links, and redirect mapping."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parents[1]
DIST=BASE/'dist'
ORIGIN='https://www.drconnorrobertson.com'
posts=json.loads((BASE/'content/historical-posts.json').read_text())
manifest=json.loads((BASE/'content/historical-recovery-manifest.json').read_text())
config=json.loads((BASE/'vercel.json').read_text())
urls={n.find('{*}loc').text:n.find('{*}lastmod').text for n in ET.parse(DIST/'sitemap.xml').getroot()}
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.canonicals=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href','').startswith('/'):self.links.append(a['href'].split('#')[0])
        if tag=='h1':self.h1+=1
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a.get('href'))

for post in posts:
    file=DIST/post['relative_url'].strip('/')/'index.html'
    text=file.read_text();p=Page(text);canonical=ORIGIN+post['relative_url']
    assert p.h1==1,(file,p.h1)
    assert p.canonicals==[canonical],(file,p.canonicals)
    assert urls[canonical]==post['modified'][:10],(file,'lastmod')
    assert 'Revised edition of a historical article' in text
    assert 'content="noindex' not in text
    nodes=[]
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
        data=json.loads(block);nodes.extend(data.get('@graph',[data]))
    article=next(n for n in nodes if n.get('@type')=='BlogPosting')
    assert article['datePublished']==post['date']
    assert article['dateModified']==post['modified']
    for href in p.links:
        target=DIST/href.lstrip('/')
        assert target.exists() or (target/'index.html').exists(),(file,href)
    inbound=[f for f in DIST.rglob('index.html') if f!=file and f'href="{post["relative_url"]}"' in f.read_text()]
    assert len(inbound)>=2,(file,'insufficient inbound links')
for item in manifest['pages']:
    if item['action']!='redirect':continue
    matches=[r for r in config['redirects'] if r['source']==item['path']]
    assert len(matches)==1 and matches[0]['statusCode']==301 and matches[0]['destination']==item['destination']
    assert (DIST/item['destination'].strip('/')/'index.html').exists()
    assert ORIGIN+item['path'] not in urls
print(f'PASS: {len(posts)} restored articles, publication/modification dates, canonicals, sitemap, internal links, inbound links, and one direct 301 mapping')
