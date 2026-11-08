"""Destructive dimension-isolation fixtures for a NEW disposable 26.3 world."""
from pathlib import Path
import sys,json
r=Path(sys.argv[1]);r.mkdir(parents=True,exist_ok=True)
(r/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'Dimension isolation tests','min_format':[121,0],'max_format':[121,0]}}))
f=r/'data/fg_dimension_test/function';f.mkdir(parents=True,exist_ok=True)
lines=['scoreboard objectives add fg_dim dummy','scoreboard players set #fail fg_dim 0','scoreboard players set #finished fg_dim 0']
for d in ('overworld','the_nether','the_end'):
 lines += [f'execute in minecraft:{d} unless loaded 512 64 0 run return 0']
lines += [
 'execute in minecraft:overworld run fill 512 64 0 527 79 15 minecraft:emerald_block strict',
 'data modify storage flusgrid:ledger regions."512,64,0" set value "complete"',
 'execute in minecraft:the_nether run fill 512 64 0 527 79 15 minecraft:netherrack strict',
 'execute in minecraft:the_end run fill 512 64 0 527 79 15 minecraft:end_stone strict',
 'execute in minecraft:the_nether run function flusgrid_nether:convert {x:512,y:64,z:0}',
 'execute in minecraft:the_end run function flusgrid_end:convert {x:512,y:64,z:0}',
]
for d,b,grid in [('overworld','emerald_block',False),('the_nether','netherrack',True),('the_end','end_stone',True)]:
 for x in range(512,528):
  for y in range(64,80):
   for z in range(16):
    block='air' if grid and (x%4 or y%4 or z%4) else b
    lines.append(f'execute in minecraft:{d} unless block {x} {y} {z} minecraft:{block} run scoreboard players add #fail fg_dim 1')
for ns in ('flusgrid','flusgrid_nether','flusgrid_end'):
 lines.append(f'execute unless data storage {ns}:ledger regions{{"512,64,0":"complete"}} run scoreboard players add #fail fg_dim 1')
lines += [
 'execute in minecraft:the_end run setblock 1 64 1 minecraft:gold_block strict',
 'execute in minecraft:the_end run function flusgrid_end:convert {x:0,y:64,z:0}',
 'execute in minecraft:the_end unless block 1 64 1 minecraft:gold_block run scoreboard players add #fail fg_dim 1',
 'execute in minecraft:the_end positioned -256 0 -256 unless predicate flusgrid_end:protected_center run scoreboard players add #fail fg_dim 1',
 'execute in minecraft:the_end positioned 255 0 255 unless predicate flusgrid_end:protected_center run scoreboard players add #fail fg_dim 1',
 'execute in minecraft:the_end positioned 256 0 0 if predicate flusgrid_end:protected_center run scoreboard players add #fail fg_dim 1',
 'execute in minecraft:the_end positioned -257 0 0 if predicate flusgrid_end:protected_center run scoreboard players add #fail fg_dim 1',
 'scoreboard players set #finished fg_dim 1',
 'scoreboard players get #fail fg_dim',
]
(f/'run.mcfunction').write_text('\n'.join(lines)+'\n')

# Read-only recheck after long-running jobs (does not recreate the fixtures).
checks=['scoreboard players set #fail fg_dim 0','scoreboard players set #finished fg_dim 0']
checks += [line for line in lines if 'unless block ' in line or 'unless data storage ' in line or ' predicate ' in line]
checks += ['scoreboard players set #finished fg_dim 1','scoreboard players get #fail fg_dim']
(f/'check.mcfunction').write_text('\n'.join(checks)+'\n')
