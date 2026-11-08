import unittest,json,re,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/'portal-test'
class PortalTest(unittest.TestCase):
 def test_test_pack_never_mutates_terrain_or_force_loads(self):
  for p in P.rglob('*.mcfunction'):
   self.assertNotRegex(p.read_text(),r'\b(?:fill|setblock|clone|forceload|place)\s')
   self.assertNotIn('function flusgrid:',p.read_text())
 def test_function_references_exist(self):
  for p in P.rglob('*.mcfunction'):
   for name in re.findall(r'function fg_portal_test:([a-z_]+)',p.read_text()):
    self.assertTrue((P/f'data/fg_portal_test/function/{name}.mcfunction').exists(),name)
 def test_destination_detected_before_checkpoint_update(self):
  s=(P/'data/fg_portal_test/function/player.mcfunction').read_text()
  self.assertLess(s.index('fg_portal_test:transition'),s.index('fg_portal_test:save'))
 def test_returns_only_to_valid_loaded_source(self):
  s=(P/'data/fg_portal_test/function/return.mcfunction').read_text()
  self.assertLess(s.index('unless loaded'),s.index('run tp'))
  self.assertLess(s.index('fg_portal_test:safe'),s.index('run tp'))
  self.assertNotRegex(s,r'tp @s 0\b')
 def test_zip_exact(self):
  with zipfile.ZipFile(R/'dist/FlusGrid-portal-return-test-0.1.zip') as z:
   self.assertEqual(set(z.namelist()),{p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()})
   for n in z.namelist():self.assertEqual(z.read(n),(P/n).read_bytes())
if __name__=='__main__':unittest.main()
