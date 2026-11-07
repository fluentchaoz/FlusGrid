"""Destructive fixture and assertions for a NEW disposable 26.3 test world."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]); p.mkdir(parents=True,exist_ok=True)
(p/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'FlusGrid area development tests','min_format':[121,0],'max_format':[121,0]}}))
f=p/'data/flusgrid_area_test/function'; f.mkdir(parents=True,exist_ok=True)
setup=['scoreboard objectives add fg_area dummy','execute unless loaded 128 -64 128 run return 0','execute unless loaded 175 319 175 run return 0']
setup += [f'fill 128 {y} 128 175 {y+7} 175 minecraft:stone strict' for y in range(-64,320,8)]
setup += ['setblock 128 -64 128 minecraft:diamond_ore strict','setblock 172 316 172 minecraft:oak_log[axis=x] strict','setblock 132 64 132 minecraft:chest[facing=west]{Items:[{Slot:0b,id:"minecraft:diamond",count:7}]} strict','setblock 127 64 128 minecraft:gold_block strict','function flusgrid:area_start {x:128,z:128}']
(f/'setup.mcfunction').write_text('\n'.join(setup)+'\n')
checks=['scoreboard players set #fail fg_area 0','scoreboard players set #finished fg_area 0','execute unless loaded 128 -64 128 run return 0','execute unless loaded 175 319 175 run return 0','execute unless data storage flusgrid:job {state:"complete",done:216,total:216} run scoreboard players add #fail fg_area 1']
for x in range(128,176,4):
 for y in range(-64,320,4):
  for z in range(128,176,4):
   block={(128,-64,128):'minecraft:diamond_ore',(172,316,172):'minecraft:oak_log[axis=x]',(132,64,132):'minecraft:chest[facing=west]'}.get((x,y,z),'minecraft:stone')
   checks.append(f'execute unless block {x} {y} {z} {block} run scoreboard players add #fail fg_area 1')
# Off-grid samples from every horizontal grid cell and height slice.
for x in range(129,176,4):
 for y in range(-63,320,4):
  for z in range(129,176,4):
   checks.append(f'execute unless block {x} {y} {z} minecraft:air run scoreboard players add #fail fg_area 1')
checks += ['execute unless data block 132 64 132 Items[{id:"minecraft:diamond",count:7}] run scoreboard players add #fail fg_area 1','execute unless block 127 64 128 minecraft:gold_block run scoreboard players add #fail fg_area 1','scoreboard players set #finished fg_area 1','scoreboard players get #fail fg_area']
(f/'check.mcfunction').write_text('\n'.join(checks)+'\n')
print(p)
