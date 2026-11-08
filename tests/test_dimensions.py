"""Check generated resources, vertical traversal, and namespace isolation."""
import unittest,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'datapack'
class Dimensions(unittest.TestCase):
 def test_owning_dimension_and_storage(self):
  for short,d in [('nether','the_nether'),('end','the_end')]:
   root=P/f'data/flusgrid_{short}/function'
   for p in root.rglob('*.mcfunction'):
    s=p.read_text()
    self.assertNotIn('flusgrid:',s,str(p))
    self.assertNotIn('minecraft:overworld',s,str(p))
   for size,total in [('',16384),('_2048',262144)]:
    s=(root/f'pregen{size}_start.mcfunction').read_text()
    self.assertIn(f'execute unless dimension minecraft:{d}',s)
    self.assertIn(f'total:{total}',s);self.assertIn('y:240',s)
   s=(root/'pregen/advance.mcfunction').read_text()
   self.assertIn('matches ..-16',s)
   self.assertEqual(len(range(240,-1,-16)),16)
 def test_end_protection_requires_initialized_arena(self):
  r=P/'data/flusgrid_end/function'
  self.assertIn('arena/tick',(r/'pregen/step.mcfunction').read_text())
  self.assertIn('arena {ready:1b}',(r/'internal/run.mcfunction').read_text())
  self.assertFalse((P/'data/flusgrid_end/predicate/protected_center.json').exists())
 def test_end_predicate_format_and_bounds(self):
  p=json.loads((P/'data/flusgrid_end/predicate/podium.json').read_text())
  self.assertEqual(p['type'],'minecraft:location_check')
  for axis in ('x','z'):
   self.assertEqual(p['predicate']['position'][axis],{'min':-8,'max':8.999})
 def test_load_and_tick_include_all_dimensions(self):
  for kind in ('load','tick'):
   v=json.loads((P/f'data/minecraft/tags/function/{kind}.json').read_text())['values']
   self.assertEqual(len(v),4)
   self.assertEqual(v[-1],'flusgrid:realm/'+kind)
 def test_function_targets_exist(self):
  for p in P.glob('data/*/function/**/*.mcfunction'):
   for ns,name in re.findall(r'\bfunction (flusgrid(?:_nether|_end)?):([a-z0-9_/]+)',p.read_text()):
    if name=='mask/phase_':
     for phase in range(9):self.assertTrue((P/f'data/{ns}/function/{name}{phase}.mcfunction').exists())
    else:self.assertTrue((P/f'data/{ns}/function/{name}.mcfunction').exists(),(p,ns,name))
if __name__=='__main__':unittest.main()
