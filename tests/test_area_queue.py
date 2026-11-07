import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from area import build_area

class AreaQueue(unittest.TestCase):
    def test_dimensions_and_order(self):
        functions={}
        build_area(lambda *args: None, lambda name, lines: functions.update({name:lines}))
        lines=functions["area/enqueue"]
        origins=[]
        for i in range(0,len(lines),8):
            dx=int(lines[i+1].split()[-1]); dz=int(lines[i+3].split()[-1]); y=int(lines[i+5].split()[-1])
            origins.append((dx,y,dz))
        self.assertEqual(len(origins),216)
        self.assertEqual(len(set(origins)),216)
        self.assertEqual(set(origins),{(x,y,z) for x in (0,16,32) for z in (0,16,32) for y in range(-64,320,16)})
        self.assertEqual(origins[0],(0,304,0))
        self.assertEqual(origins[-1],(32,-64,32))

if __name__ == "__main__": unittest.main()
