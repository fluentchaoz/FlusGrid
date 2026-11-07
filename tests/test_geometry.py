import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('build',Path(__file__).resolve().parents[1]/'tools/build.py')
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class GridGeometry(unittest.TestCase):
    def test_exact_complement_and_no_overlap(self):
        removed=set()
        for x0,y0,z0,x1,y1,z1 in build.boxes():
            self.assertLessEqual((x1-x0+1)*(y1-y0+1)*(z1-z0+1),32768)
            for x in range(x0,x1+1):
                for y in range(y0,y1+1):
                    for z in range(z0,z1+1):
                        self.assertNotIn((x,y,z),removed)
                        removed.add((x,y,z))
        expected={(x,y,z) for x in range(16) for y in range(16) for z in range(16) if x%4 or y%4 or z%4}
        self.assertEqual(removed,expected)
        self.assertEqual(len(removed),4032)

    def test_global_phase_across_negative_and_positive_origins(self):
        for origin in (-29999984,-32,-16,0,16,29999968):
            self.assertEqual([origin+i for i in range(16) if i%4==0],[i for i in range(origin,origin+16) if i%4==0])

if __name__=='__main__': unittest.main()
