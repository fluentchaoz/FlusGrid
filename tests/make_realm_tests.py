"""Fixtures for a NEW disposable 26.3 world only; never install on a play save."""
from pathlib import Path
import json,sys
r=Path(sys.argv[1]);f=r/'data/fg6_test/function';f.mkdir(parents=True,exist_ok=True)
(r/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'FlusGrid 0.6 destructive fixtures','min_format':[121,0],'max_format':[121,0]}}))
def out(n,ls):(f/(n+'.mcfunction')).write_text('\n'.join(ls)+'\n')
base=['scoreboard objectives add fg_test dummy','scoreboard players set #fail fg_test 0']
out('end_fixture',base+[
 'execute in minecraft:the_end run setblock 1 60 1 minecraft:gold_block strict',
 'execute in minecraft:the_end run setblock 17 60 1 minecraft:gold_block strict',
 'execute in minecraft:the_end run setblock 16 60 0 minecraft:diamond_block strict',
])
out('end_check',base+[
 'execute in minecraft:the_end unless block 1 60 1 minecraft:gold_block run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end unless block 17 60 1 minecraft:air run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end unless block 16 60 0 minecraft:diamond_block run scoreboard players add #fail fg_test 1',
 'scoreboard players set #caps fg_test 0',
 'execute in minecraft:the_end as @e[type=marker,tag=flusgrid_cap] at @s run scoreboard players add #caps fg_test 1',
 'execute unless score #caps fg_test matches 10 run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end as @e[type=marker,tag=flusgrid_cap] at @s unless block ~ ~ ~ minecraft:bedrock run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end as @e[type=marker,tag=flusgrid_cap] at @s unless block ~ ~-1 ~ minecraft:obsidian run scoreboard players add #fail fg_test 1',
 'scoreboard players set #crystals fg_test 0',
 'execute in minecraft:the_end as @e[type=end_crystal] run scoreboard players add #crystals fg_test 1',
 'execute unless score #crystals fg_test matches 10 run scoreboard players add #fail fg_test 1',
 'scoreboard players get #caps fg_test','scoreboard players get #crystals fg_test','scoreboard players get #fail fg_test',
])
portal=base[:]
for t in range(-1,2):
 for x,z,d in [(-2,t,'east'),(2,t,'west'),(t,-2,'south'),(t,2,'north')]:
  portal.append(f'execute in minecraft:overworld unless block {x} -32 {z} minecraft:end_portal_frame[facing={d},eye=false] run scoreboard players add #fail fg_test 1')
for x in range(-1,2):
 for z in range(-1,2):portal.append(f'execute in minecraft:overworld unless block {x} -32 {z} minecraft:air run scoreboard players add #fail fg_test 1')
portal += ['execute in minecraft:overworld unless block 0 -33 0 minecraft:obsidian run scoreboard players add #fail fg_test 1','scoreboard players get #fail fg_test']
out('portal_check',portal)
out('guard',base+[
 'kill @e[type=marker,tag=fg6_player]',
 'summon marker 0.25 81 0.5 {Tags:["fg6_player"]}',
 'scoreboard players set #scan_clock flusgrid 0',
 'execute as @e[type=marker,tag=fg6_player,limit=1] at @s run function flusgrid:realm/player_overworld',
 'tp @e[type=marker,tag=fg6_player] 700 81 0',
 'execute as @e[type=marker,tag=fg6_player,limit=1] at @s run function flusgrid:realm/player_overworld',
 'execute as @e[type=marker,tag=fg6_player,limit=1] unless data entity @s {Pos:[0.25d,81.0d,0.5d]} run scoreboard players add #fail fg_test 1',
 # Request a strip at x300 before guard boundary 511.
 'tp @e[type=marker,tag=fg6_player] 300 81 0',
 'scoreboard players set #scan_clock flusgrid 10',
 'execute as @e[type=marker,tag=fg6_player,limit=1] at @s run function flusgrid:realm/player_overworld',
 'execute unless data storage flusgrid:realm {owner:"overworld",plan:{direction:"east"}} run scoreboard players add #fail fg_test 1',
 'execute unless data storage flusgrid:realm bounds.overworld{max_x:1023} run scoreboard players add #fail fg_test 1',
 'execute unless data storage flusgrid:job {min_x:1024,max_x:1520,min_z:-1024,max_z:1008,chunk_total:4096,total:98304} run scoreboard players add #fail fg_test 1',
 # Second request must not replace active work.
 'tp @e[type=marker,tag=fg6_player] -400 81 0',
 'execute as @e[type=marker,tag=fg6_player,limit=1] at @s run function flusgrid:realm/player_overworld',
 'execute unless data storage flusgrid:realm {owner:"overworld",plan:{direction:"east"}} run scoreboard players add #fail fg_test 1',
 'scoreboard players get #fail fg_test',
])

# Synthetic planner checks: no conversion ticks, all twelve dimension/direction cases.
planner=base[:]
for short,ns,span,sections in [('overworld','flusgrid',1024,24),('nether','flusgrid_nether',1024,16),('end','flusgrid_end',2048,16)]:
 for edge,axis,sign in [('west','x','min'),('east','x','max'),('north','z','min'),('south','z','max')]:
  planner += [f'data modify storage {ns}:job state set value "complete"','data remove storage flusgrid:realm owner']
  for a in 'xz':
   planner += [f'scoreboard players set #bmin_{a} flusgrid {-span}',f'scoreboard players set #bmax_{a} flusgrid {span-1}']
  planner.append(f'function flusgrid:realm/expand_{short}_{edge}')
  bounds={'min_x':-span,'max_x':span-16,'min_z':-span,'max_z':span-16}
  if sign=='min':bounds['min_'+axis]=-span-512;bounds['max_'+axis]=-span-16
  else:bounds['min_'+axis]=span;bounds['max_'+axis]=span+496
  chunks=32*(span*2//16)
  fields=','.join(f'{k}:{v}' for k,v in bounds.items())+f',chunk_total:{chunks},total:{chunks*sections}'
  planner.append(f'execute unless data storage {ns}:job {{{fields}}} run scoreboard players add #fail fg_test 1')
  planner.append(f'execute unless data storage flusgrid:realm bounds.{short}{{min_x:{-span},max_x:{span-1},min_z:{-span},max_z:{span-1}}} run scoreboard players add #fail fg_test 1')
  planner += [f'data modify storage {ns}:job state set value "complete"','data remove storage flusgrid:realm owner','data remove storage flusgrid:realm plan']
planner.append('scoreboard players get #fail fg_test')
out('planner',planner)

out('migration',base+[
 'execute in minecraft:the_end run fill 80 64 0 95 79 15 minecraft:end_stone strict',
 'data modify storage flusgrid_end:ledger regions."80,64,0" set value "protected"',
 'execute in minecraft:the_end run function flusgrid_end:convert {x:80,y:64,z:0}',
 'execute in minecraft:the_end unless block 81 65 1 minecraft:air run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end unless block 80 64 0 minecraft:end_stone run scoreboard players add #fail fg_test 1',
 'execute unless data storage flusgrid_end:ledger regions{"80,64,0":"complete"} run scoreboard players add #fail fg_test 1',
 'execute in minecraft:the_end run setblock 81 65 1 minecraft:gold_block strict',
 'execute in minecraft:the_end run function flusgrid_end:convert {x:80,y:64,z:0}',
 'execute in minecraft:the_end unless block 81 65 1 minecraft:gold_block run scoreboard players add #fail fg_test 1',
 'scoreboard players get #fail fg_test',
])
