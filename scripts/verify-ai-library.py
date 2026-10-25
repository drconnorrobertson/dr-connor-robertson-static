"""Check the generated AI library after the complete Vercel build pipeline."""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from ai_growth import resources
ROOT=BASE/'dist'
ORIGIN='https://www.drconnorrobertson.com'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.h1=0;self.canonicals=[];self.hrefs=[];self.ids=set();self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.add(a['id'])
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a.get('href'))
        if tag=='a' and 'href' in a:self.hrefs.append(a['href'])

sitemap=ET.parse(ROOT/'sitemap.xml')
urls={n.text for n in sitemap.iter() if n.tag.endswith('}loc')}
paths=list((ROOT/'ai/implementation').rglob('index.html'))
assert len(paths)==43, len(paths)
parsed={}
for file in paths:
    text=file.read_text();info=Page(text);parsed[file]=info
    url=ORIGIN+'/'+file.parent.relative_to(ROOT).as_posix()+'/'
    assert info.h1==1,(file,'H1 count',info.h1)
    assert info.canonicals==[url],(file,'canonical',info.canonicals)
    assert url in urls,(file,'sitemap')
    assert 'content="noindex' not in text,(file,'noindex')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):json.loads(block)
    for href in info.hrefs:
        link=urlparse(href)
        if href.startswith('#'):
            assert unquote(link.fragment) in info.ids,(file,'anchor',href)
        if not href.startswith('/') or href.startswith('//'):continue
        target=ROOT/unquote(link.path).lstrip('/')
        if target.is_dir():target=target/'index.html'
        assert target.exists(),(file,'broken internal link',href)
        if link.fragment and target.suffix=='.html':assert unquote(link.fragment) in Page(target.read_text()).ids,(file,'target anchor',href)
rows=resources();assert len(rows)==92
assert len({r[1] for r in rows})==len(rows),'duplicate guide URLs'
assert len({r[0].lower() for r in rows})==len(rows),'duplicate titles'
for title,url,category,desc in rows:assert (ROOT/url.strip('/')/'index.html').exists(),url
for path in ['index.html','ai-business-strategy/index.html','blog/complete-resource-index-dr-connor-robertson/index.html']:
    assert '/ai/implementation/' in (ROOT/path).read_text(),path
print('PASS: 43 implementation pages, 92 unique guide URLs, sitemap, canonical URLs, H1s, JSON-LD, links and fragments')
