"""Regression checks for stable photo URLs and their promised HTTP encoding."""
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse, parse_qs
import json,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build import image_request_url, verify_photo_content_types
class PhotoContentTypes(unittest.TestCase):
 def test_unsplash_format_preserves_other_parameters(self):
  u=image_request_url('https://images.unsplash.com/photo-example?w=1200&q=80&fm=webp&fit=crop')
  p=urlparse(u);self.assertEqual(p.path,'/photo-example');self.assertEqual(parse_qs(p.query),{'w':['1200'],'q':['80'],'fit':['crop'],'fm':['jpg']});self.assertEqual(image_request_url(u),u)
 def test_other_origins_and_paths_unchanged(self):
  for u in ['https://example.com/photo-test?fm=webp','https://images.unsplash.com/other?fm=webp','https://www.drconnorrobertson.com/images/connor.jpg']:
   self.assertEqual(image_request_url(u),u)
 def test_non_jpeg_photo_blocks_publication(self):
  with TemporaryDirectory() as d:
   root=Path(d);(root/'images').mkdir();p=root/'images/photo-test';p.write_bytes(b'\xff\xd8\xff\xe0test');verify_photo_content_types(root)
   p.write_bytes(b'\x89PNG\r\n\x1a\n')
   with self.assertRaisesRegex(ValueError,'not JPEG'):verify_photo_content_types(root)
   p.unlink();(root/'images/other.png').write_bytes(b'\x89PNG');verify_photo_content_types(root)
 def test_root_header_is_narrow(self):
  config=json.loads((Path(__file__).resolve().parents[1]/'vercel.json').read_text());rules=[x for x in config['headers'] if x['source']=='/images/photo-(.*)'];self.assertEqual(rules,[{'source':'/images/photo-(.*)','headers':[{'key':'Content-Type','value':'image/jpeg'}]}])
if __name__=='__main__':unittest.main()
