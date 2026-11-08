import unittest,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'datapack/data'
class Realm(unittest.TestCase):
 def test_portal_geometry(self):
  s=(P/'flusgrid/function/realm/portal.mcfunction').read_text()
  frames=re.findall(r'setblock (-?\d+) (-?\d+) (-?\d+) minecraft:end_portal_frame\[facing=(\w+),eye=false\]',s)
  self.assertEqual(len(frames),12)
  self.assertEqual(len({(x,y,z) for x,y,z,d in frames}),12)
  for x,y,z,d in frames:
   x,y,z=int(x),int(y),int(z)
   self.assertEqual(y,-32)
   self.assertEqual(d,'east' if x==-2 else 'west' if x==2 else 'south' if z==-2 else 'north')
 def test_mask_partitions_exact_grid_complement(self):
  actual=[]
  for phase in range(4):
   s=(P/f'flusgrid_end/function/mask/phase_{phase}.mcfunction').read_text()
   actual += [tuple(map(int,m)) for m in re.findall(r'execute positioned ~(\d+) ~(\d+) ~(\d+) run function',s)]
  expected={(x,y,z) for x in range(16) for y in range(16) for z in range(16) if x%4 or y%4 or z%4}
  self.assertEqual(set(actual),expected)
  self.assertEqual(len(actual),len(expected))
  for phase in range(4):
   s=(P/f'flusgrid_end/function/mask/phase_{phase+4}.mcfunction').read_text()
   check=[tuple(map(int,m)) for m in re.findall(r'execute positioned ~(\d+) ~(\d+) ~(\d+) run function',s)]
   self.assertEqual(set(check),{p for p in expected if phase*4<=p[1]<phase*4+4})
 def test_frontier_commit_is_only_after_completion(self):
  s=(P/'flusgrid/function/realm/tick.mcfunction').read_text()
  for line in s.splitlines():
   if 'realm/commit_' in line:self.assertIn('{state:"complete"}',line)
  for short in ['overworld','nether','end']:
   for direction in ['west','east','north','south']:
    s=(P/f'flusgrid/function/realm/expand_{short}_{direction}.mcfunction').read_text()
    self.assertNotIn(f'bounds.{short} set',s)
 def test_guard_before_pause_return(self):
  s=(P/'flusgrid/function/realm/tick.mcfunction').read_text()
  self.assertLess(s.index('realm/players'),s.index('manual_pause'))
 def test_no_automatic_ledger_reset(self):
  for p in P.glob('*/function/**/*.mcfunction'):
   for line in p.read_text().splitlines():
    if 'data remove storage' in line and ':ledger' in line:
     self.assertIn(':"protected"',line)
if __name__=='__main__':unittest.main()
