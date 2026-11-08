import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from pregen import build_pregen
from leaves import build_leaves,LEAVES

class Version4(unittest.TestCase):
 def test_large_job_contract(self):
  f={};build_pregen(lambda n,l:f.update({n:l}))
  s='\n'.join(f['pregen_2048_start'])
  self.assertIn('total:393216',s);self.assertIn('chunk_total:16384',s)
  self.assertIn('flusgrid 2032',s);self.assertIn('29997936',s)
  self.assertNotIn('total:24576',s)
  self.assertIn('flusgrid 1024','\n'.join(f['pregen_2048_here']))
  self.assertIn('storage flusgrid:job chunk_total','\n'.join(f['pregen/next_chunk']))
  self.assertIn('storage flusgrid:job total','\n'.join(f['pregen/step']))
 def test_leaf_state_coverage(self):
  f={};build_leaves(lambda n,l:f.update({n:l}))
  self.assertEqual(len(LEAVES),14)
  self.assertEqual(len(f['internal/preserve_leaves']),64)
  self.assertEqual(len(f['internal/persist_leaf']),14*7*2)
  for leaf in LEAVES:
   for d in range(1,8):
    for w in ('true','false'):
     a=f'minecraft:{leaf}_leaves[persistent=false,distance={d},waterlogged={w}]'
     b=f'minecraft:{leaf}_leaves[persistent=true,distance={d},waterlogged={w}]'
     self.assertTrue(any(a in l and b in l for l in f['internal/persist_leaf']))
if __name__=='__main__':unittest.main()
