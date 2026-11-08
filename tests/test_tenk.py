"""Contract checks for the generated experimental 10K controller."""
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "datapack/data/flusgrid/function/realm"

class TenK(unittest.TestCase):
    def load(self, name):
        return (P / (name + ".mcfunction")).read_text()

    def test_initial_bounds_and_counts(self):
        setup = (P.parent / "setup.mcfunction").read_text()
        self.assertIn("model:10000", setup)
        self.assertIn("x:-5008,z:-5008,ex:4976,ez:4976", setup)
        self.assertIn("chunks:390625,total:9375000", setup)
        for dim, cubes in [("overworld",9375000),("nether",6250000),("end",6250000)]:
            complete = self.load("complete_" + dim)
            self.assertIn("min_x:-5008,max_x:4991,min_z:-5008,max_z:4991",complete)
            if dim != "end":
                next_cubes = 6250000
                self.assertIn(f"chunks:390625,total:{next_cubes}",complete)

    def test_queue_commits_only_after_completion(self):
        tick = self.load("tick")
        self.assertLess(tick.index("realm/players10"),tick.index("manual_pause"))
        for dim in ("overworld","nether","end"):
            matched = [l for l in tick.splitlines() if "tile_complete_" + dim in l]
            self.assertEqual(len(matched),1)
            self.assertIn('{state:"complete"}',matched[0])
            self.assertIn("tile_mark_"+dim,self.load("tile_complete_"+dim))
            self.assertIn("pending."+dim,self.load("tile_enqueue_"+dim))
            self.assertIn('tiles.'+dim,self.load("tile_lookup_"+dim))

    def test_portal_return_is_automatic_and_no_spawn_fallback(self):
        tick = self.load("tick")
        self.assertIn("players10", tick)
        for dim in ("overworld","nether","end"):
            self.assertIn("hold10_"+dim,self.load("player10_"+dim))
            self.assertIn("return10",self.load("hold10_"+dim))
        point = self.load("return10")
        self.assertLess(point.index("unless loaded"),point.index("run tp"))
        self.assertLess(point.index("checkpoint_safe"),point.index("run tp"))
        self.assertNotIn("tp @s 0 ",point)
        self.assertIn("No loaded, clear checkpoint",self.load("return_failed"))

    def test_persistent_queue_and_tile_sizes(self):
        load=self.load("load")
        self.assertIn("unless data storage flusgrid:realm queue",load)
        self.assertIn("unless data storage flusgrid:realm tiles",load)
        for dim, cubes in (("overworld",24576),("nether",16384),("end",16384)):
            s=self.load("tile_start_"+dim)
            self.assertIn("scoreboard players add #ex flusgrid 496",s)
            self.assertIn("scoreboard players add #ez flusgrid 496",s)
            self.assertIn(f"chunks:1024,total:{cubes}",s)
        for dim in ("overworld","nether","end"):
            self.assertIn("remove #target_x", self.load("neighbor_"+dim+"_west"))
            self.assertIn("remove #target_z", self.load("neighbor_"+dim+"_north"))

if __name__=="__main__":
    unittest.main()
