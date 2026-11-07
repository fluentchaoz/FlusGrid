import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from pregen import build_pregen

class PregenCursor(unittest.TestCase):
    def test_cursor_bounds_and_count(self):
        # Contract for the cursor: x-fast, z-row, y descending per chunk.
        for start in (0,-256,4096):
            x=z=start; y=304; cubes=[]; chunks=0
            while chunks<1024:
                cubes.append((x,y,z)); y-=16
                if y < -64:
                    chunks+=1; y=304; x+=16
                    if x>start+496: x=start; z+=16
            self.assertEqual(len(cubes),24576)
            self.assertEqual(len(set(cubes)),24576)
            self.assertEqual(cubes[-1],(start+496,-64,start+496))
            self.assertEqual({v[1] for v in cubes},set(range(-64,320,16)))

    def test_generated_release_is_ownership_scoped(self):
        f={};build_pregen(lambda name,lines:f.update({name:lines}))
        self.assertTrue(any('ticket{owned:1b}' in line for line in f['pregen/release']))
        self.assertEqual(f['pregen/remove_ticket'],['$forceload remove $(x) $(z)'])
        self.assertFalse(any('forceload remove all' in line for lines in f.values() for line in lines))
        self.assertIn('execute unless data storage flusgrid:job ticket run return run function flusgrid:pregen/acquire with storage flusgrid:job cursor',f['pregen/step'])

if __name__=='__main__':unittest.main()
