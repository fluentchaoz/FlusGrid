"""Generate an optional destructive test pack ONLY in a disposable server world.
Usage: python tests/make_runtime_tests.py /path/to/test-world/datapacks/flusgrid-tests
"""
import json, sys
from pathlib import Path
p=Path(sys.argv[1]); p.mkdir(parents=True,exist_ok=True)
(p/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'FlusGrid destructive development tests','min_format':[121,0],'max_format':[121,0]}}))
f=p/'data/flusgrid_test/function'; f.mkdir(parents=True,exist_ok=True)
lines=['scoreboard objectives add fg_test dummy','scoreboard players set #fail fg_test 0', 'scoreboard players set #finished fg_test 0',
       'execute unless loaded -16 64 -16 run return 0',
       'execute unless loaded 63 0 15 run return 0',
       'fill 0 64 0 15 79 15 minecraft:stone strict',
       'setblock 0 64 0 minecraft:chest[facing=east]{Items:[{Slot:0b,id:"minecraft:diamond",count:7}]} strict',
       'function flusgrid:convert {x:0,y:64,z:0}']
for x in range(16):
 for y in range(64,80):
  for z in range(16):
   b='minecraft:air' if x%4 or y%4 or z%4 else ('minecraft:chest[facing=east]' if (x,y,z)==(0,64,0) else 'minecraft:stone')
   lines.append(f'execute unless block {x} {y} {z} {b} run scoreboard players add #fail fg_test 1')
lines+=['execute unless data block 0 64 0 Items[{id:"minecraft:diamond",count:7}] run scoreboard players add #fail fg_test 1',
        'setblock 1 65 1 minecraft:gold_block strict',
        'function flusgrid:convert {x:0,y:64,z:0}',
        'execute unless block 1 65 1 minecraft:gold_block run scoreboard players add #fail fg_test 1',
        'fill -16 64 -16 -1 79 -1 minecraft:stone strict',
        'function flusgrid:convert {x:-16,y:64,z:-16}']
for x in range(-16,0):
 for y in range(64,80):
  for z in range(-16,0):
   b='minecraft:air' if x%4 or y%4 or z%4 else 'minecraft:stone'
   lines.append(f'execute unless block {x} {y} {z} {b} run scoreboard players add #fail fg_test 1')
# Natural terrain comparison against a pre-conversion copy.
lines+=['clone 16 0 0 31 15 15 48 0 0 strict', 'function flusgrid:convert {x:16,y:0,z:0}']
for x in range(16,32):
 for y in range(16):
  for z in range(16):
   if x%4 or y%4 or z%4:
    lines.append(f'execute unless block {x} {y} {z} minecraft:air run scoreboard players add #fail fg_test 1')
   else:
    lines.append(f'execute unless blocks {x} {y} {z} {x} {y} {z} {x+32} {y} {z} all run scoreboard players add #fail fg_test 1')
lines += ['function flusgrid:convert {x:1,y:64,z:0}',
          'execute if data storage flusgrid:ledger regions."1,64,0" run scoreboard players add #fail fg_test 1',
          'execute in minecraft:the_nether run function flusgrid:convert {x:32,y:64,z:0}',
          'execute if data storage flusgrid:ledger regions."32,64,0" run scoreboard players add #fail fg_test 1',
          'function flusgrid:convert {x:100000,y:64,z:100000}',
          'execute if data storage flusgrid:ledger regions."100000,64,100000" run scoreboard players add #fail fg_test 1',
          'scoreboard players set #finished fg_test 1',
          'scoreboard players get #fail fg_test',
          'data get storage flusgrid:ledger']
(f/'run.mcfunction').write_text('\n'.join(lines)+'\n')
(f/'revisit.mcfunction').write_text('\n'.join([
 'function flusgrid:convert {x:0,y:64,z:0}',
 'execute unless block 1 65 1 minecraft:gold_block run scoreboard players add #fail fg_test 1',
 'execute unless data storage flusgrid:ledger regions{"0,64,0":"complete"} run scoreboard players add #fail fg_test 1',
 'scoreboard players get #fail fg_test'])+'\n')
print(p)
