"""Check local HTML links and assets in a completed static build."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'dist/site').resolve()
errors=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('href','src') or not value: continue
   url=urlsplit(value)
   if url.scheme or url.netloc or not url.path: continue
   path=(root/unquote(url.path).lstrip('/') if url.path.startswith('/') else current.parent/unquote(url.path)).resolve()
   if path.is_dir(): path=path/'index.html'
   if not path.is_file(): errors.append(f'{current.relative_to(root)} -> {value}')
pages=list(root.rglob('*.html'))
assert pages,'No generated HTML pages'
for current in pages:
 parser=Links(); parser.feed(current.read_text(encoding='utf-8'))
if errors: raise SystemExit('\n'.join(errors))
print(f'Checked local link and asset targets in {len(pages)} HTML pages')
