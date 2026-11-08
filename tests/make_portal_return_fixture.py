"""Destructive pig/real-portal fixture ONLY for a disposable vanilla test world.
Pigs exercise real portal transport, but are not a replacement for client/player testing.
"""
from pathlib import Path
import json,sys
r=Path(sys.argv[1]);f=r/'data/fpt_fixture/function';f.mkdir(parents=True,exist_ok=True)
(r/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'Disposable portal test fixture','min_format':[121,0],'max_format':[121,0]}}))
t=r/'data/minecraft/tags/function/tick.json';t.parent.mkdir(parents=True,exist_ok=True);t.write_text(json.dumps({'values':['fpt_fixture:tick']}))
def out(n,ls):(f/(n+'.mcfunction')).write_text('\n'.join(ls)+'\n')
setup=['scoreboard objectives add fpt_test dummy',*[f'execute in minecraft:{d} run kill @e[tag=fpt_mock]' for d in ['overworld','the_nether','the_end']]]
for d in ['overworld','the_nether']:
 for command in ['fill -8 80 -8 8 80 8 minecraft:obsidian','fill -8 81 -8 8 86 8 minecraft:air','fill -1 80 5 2 84 5 minecraft:obsidian','fill 0 81 5 1 83 5 minecraft:nether_portal[axis=x]']:
  setup.append(f'execute in minecraft:{d} run {command}')
setup += ['execute in minecraft:overworld run summon pig 0.5 81 0.5 {NoAI:1b,Invulnerable:1b,Tags:["fpt_mock"]}',
          'execute in minecraft:overworld as @e[tag=fpt_mock] at @s run function fpt_fixture:arm']
out('setup',setup)
out('arm',[
 'function fg_portal_test:dimension','function fg_portal_test:save',
 'scoreboard players operation @s fpt_prev = @s fpt_dim',
 'scoreboard players operation @s fpt_last = #clock fpt_tick',
 'scoreboard players operation @s fpt_epoch = #epoch fpt_tick',
 'scoreboard players set @s fpt_seen 0','scoreboard players set @s fpt_blocks 0','scoreboard players set @s fpt_notice 0','scoreboard players set @s fpt_allow 0','tag @s add fpt_enabled',
])
out('tick',[f'execute in minecraft:{d} as @e[tag=fpt_mock,tag=fpt_enabled] at @s run function fpt_fixture:tick_entity' for d in ['overworld','the_nether','the_end']])
for label,dim,target in [('ow','overworld',2),('nether','the_nether',1)]:
 out('check_'+label,[
  'scoreboard players set #fail fpt_test 0',
  f'execute in minecraft:{dim} unless entity @e[tag=fpt_mock,tag=fpt_enabled] run scoreboard players add #fail fpt_test 1',
  f'execute in minecraft:{dim} as @e[tag=fpt_mock] unless score @s fpt_blocks matches 1.. run scoreboard players add #fail fpt_test 1',
  f'execute in minecraft:{dim} as @e[tag=fpt_mock] unless score @s fpt_dd matches {target} run scoreboard players add #fail fpt_test 1',
  f'execute in minecraft:{dim} as @e[tag=fpt_mock] unless data entity @s {{Pos:[0.5d,81.0d,0.5d]}} run scoreboard players add #fail fpt_test 1',
  'scoreboard players get #fail fpt_test',
 ])

out('tick_entity',['scoreboard players operation @s fpt_last = #previous fpt_tick','function fg_portal_test:player'])
