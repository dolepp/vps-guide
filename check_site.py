"""Check the rendered artifact's navigation, SEO metadata and referral links."""
import json,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
root=Path(sys.argv[1]);site=sys.argv[2].rstrip('/');siteparts=urlsplit(site);prefix=siteparts.path.rstrip('/')
class Document(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.h1=0;self.title=0;self.desc=0;self.canon=[];self.links=[];self.refs=[];self.ids=set();self.scripts=[];self.jsonld=False;self.raw=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title+=1
  if tag=='meta' and a.get('name')=='description':self.desc+=bool(a.get('content'))
  if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
  if tag in ('a','link','script','img'):
   href=a.get('href') or a.get('src')
   if href:self.links.append(href)
  if tag=='a' and ('ref=' in a.get('href','') or 'sponsored' in a.get('rel','')):self.refs.append(a)
  if tag=='script' and a.get('type')=='application/ld+json':self.jsonld=True
 def handle_data(self,s):
  if self.jsonld:self.raw.append(s)
 def handle_endtag(self,tag):
  if tag=='script' and self.jsonld:
   json.loads(''.join(self.raw));self.jsonld=False;self.raw=[]
docs={};errors=[]
for path in root.rglob('*.html'):
 d=Document();source=path.read_text();d.feed(source);docs[path]=d
 if d.h1!=1:errors.append(f'{path}: expected 1 h1, got {d.h1}')
 if d.title!=1 or d.desc!=1:errors.append(f'{path}: missing/duplicate title or description')
 if len(d.canon)!=1 or not d.canon[0].startswith(site+'/'):errors.append(f'{path}: incorrect canonical {d.canon}')
 for a in d.refs:
  if 'ref=467715' not in a['href'] or 'sponsored' not in a.get('rel',''):errors.append(f'{path}: unqualified referral {a["href"]}')
 if '{BASE}' in source or '{AFFILIATE}' in source:errors.append(f'{path}: unresolved template')
for path,d in docs.items():
 for href in d.links:
  u=urlsplit(href)
  if u.scheme and u.scheme not in ('https','http'):continue
  if u.netloc and u.netloc!=siteparts.netloc:continue
  if u.netloc and prefix and not (u.path==prefix or u.path.startswith(prefix+'/')):continue
  if href.startswith('#'):target=path
  elif u.path.startswith('/'):
   clean=u.path
   if prefix and clean.startswith(prefix):clean=clean[len(prefix):]
   target=root/unquote(clean.lstrip('/'))
  else:target=path.parent/unquote(u.path)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{path}: missing target {href}')
  elif u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append(f'{path}: missing anchor {href}')
assert (root/'sitemap.xml').exists()
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'Validated {len(docs)} HTML pages: headings, canonical, structured data, links and referrals')
