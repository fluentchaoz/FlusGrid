"""Contract checks for the generated experimental 10K controller."""
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "datapack/data/flusgrid/function/realm"

class TenK(unittest.TestCase):
    def load(self, name):
        return (P / (name + ".mcfunction")).read_text()

    def test_initial_bounds_and_counts(self):
        setup = (P.parent / "setup.mcfunction").read_text()
        smoke = (P.parent / "setup_smoke.mcfunction").read_text()
        self.assertIn("model:10000",setup)
        self.assertIn("min_x:-5008,max_x:4991", setup)
        self.assertIn("min_x:-128,max_x:127", smoke)
        self.assertIn("smoke:1b",smoke)
        for dim, cubes, smoke_cubes in [
            ("overworld",9375000,6144),
            ("nether",6250000,4096),
            ("end",6250000,4096),
        ]:
            complete=self.load("complete_"+dim)
            self.assertIn("set from storage flusgrid:realm start_bounds",complete)
            start=self.load("initial_start_"+dim)
            self.assertIn("x:-5008,z:-5008,ex:4976,ez:4976",start)
            self.assertIn(f"chunks:390625,total:{cubes}",start)
            self.assertIn(f"chunks:256,total:{smoke_cubes}",start)
            player=self.load("player10_"+dim)
            self.assertIn("if score @s fg_x >= #bmin_x",player)
            self.assertIn("if score @s fg_z <= #bmax_z",player)
            self.assertIn("nbt={OnGround:1b}",player)

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
        safe=self.load("checkpoint_safe")
        self.assertIn("minecraft:water",safe)
        self.assertIn("minecraft:lava",safe)
        self.assertIn("minecraft:air",safe)
        self.assertNotIn("#flusgrid:safe_floor",safe)

    def test_queued_tile_dispatch_uses_valid_root_nbt_predicate(self):
        dispatch = self.load("tile_start")
        self.assertIn("dispatch set from storage flusgrid:realm queue[0]", dispatch)
        for dim in ("overworld", "nether", "end"):
            self.assertIn(
                '{dispatch:{dimension:"' + dim + '"}} run function flusgrid:realm/tile_start_' + dim,
                dispatch,
            )
            self.assertNotIn('queue[0] {dimension:"' + dim + '"}', dispatch)
        self.assertIn("data remove storage flusgrid:realm dispatch",dispatch)
        tick = self.load("tick")
        self.assertIn("run function flusgrid:realm/tile_start with storage flusgrid:realm queue[0]", tick)

    def test_creative_requests_regions_without_teleport(self):
        players = self.load("players10")
        self.assertNotIn("gamemode=!creative", players)
        self.assertIn("gamemode=!spectator", players)
        for dim in ("overworld", "nether", "end"):
            player = self.load("player10_" + dim)
            self.assertIn("gamemode=creative", player)
            creative = player.index("execute if entity @s[gamemode=creative] run return 1")
            self.assertLess(player.index("request_here_" + dim), creative)
            self.assertLess(player.index("request_main_" + dim), creative)
            self.assertLess(player.index("request_neighbors_" + dim), creative)
            self.assertLess(creative, player.index("hold10_" + dim))
            self.assertNotIn("gamemode=creative", self.load("hold10_" + dim))
        for name in ("tile_coords", "target_to_tile"):
            code=self.load(name)
            self.assertEqual(code.count("matches ..-1 run scoreboard players add #mod flusgrid 512"), 2)
            self.assertLess(code.index("matches ..-1"),code.index("flusgrid -= #mod"))

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
