"""Experimental 10K initial campaign and resumable 512-block remote tiles.

Runs after the 0.6 generator and deliberately retains its legacy functions
for worlds already on 0.6. All terrain changes use the existing journaled
per-dimension rectangle worker. No world generation occurs on a player tick.
"""
import json
from realms import DIMS

S = 'flusgrid:realm'
MIN, MAX, END_ORIGIN = -5008, 4991, 4976
TILE = 512
DIM_INDEX = {'overworld': 1, 'nether': 2, 'end': 3}

def build_10k(pack, write, function):
    def f(name, lines):
        function('realm/' + name, lines)
    def ef(name, lines):
        function(name, lines)
    def read(name):
        return (pack / ('data/flusgrid/function/realm/' + name + '.mcfunction')).read_text().splitlines()
    def emit(name, lines):
        write('data/flusgrid/function/realm/' + name + '.mcfunction', '\n'.join(lines))

    # Keep 0.6's guard available for saves that have not opted into the new model.
    f('tick_legacy_players', read('players'))
    f('load', read('load') + [
        'scoreboard objectives add fg_yaw dummy',
        'scoreboard objectives add fg_pitch dummy',
        'scoreboard players set #tile_size flusgrid 512',
        'execute unless data storage flusgrid:realm tiles run data modify storage flusgrid:realm tiles set value {overworld:{},nether:{},end:{}}',
        'execute unless data storage flusgrid:realm pending run data modify storage flusgrid:realm pending set value {overworld:{},nether:{},end:{}}',
        'execute unless data storage flusgrid:realm queue run data modify storage flusgrid:realm queue set value []',
    ])
    # Setup never migrates or overwrites an active 0.6 world.
    ef('setup', [
        'execute unless data storage flusgrid:realm {state:"idle"} run return run function flusgrid:realm_status',
        'execute if entity @a[gamemode=survival] run return run tellraw @a {text:"Finish setup before Survival joins.",color:"red"}',
        'execute if entity @a[gamemode=adventure] run return 0',
        *[f'execute if data storage {ns}:job {{state:"{state}"}} run return run tellraw @a {{text:"Finish the existing {short} preparation before setup.",color:"red"}}'
          for short, ns, dim, top, low, sections in DIMS for state in ('running', 'paused')],
        'data merge storage flusgrid:realm {model:10000,state:"preparing",phase:"overworld",manual_pause:0b,live:0b,owner:"overworld"}',
        'execute in minecraft:overworld run function flusgrid:pregen/rectangle {x:-5008,z:-5008,ex:4976,ez:4976,chunks:390625,total:9375000}',
        'tellraw @a {text:"FlusGrid 10K setup started. Three 10,000-block-wide squares, one dimension at a time. This can require many days; status/pause/resume remain available.",color:"yellow"}',
    ])
    for i,(short, ns, dim, top, low, sections) in enumerate(DIMS):
        lines = [
            f'execute unless data storage flusgrid:fixtures {short}{{ready:1b}} in {dim} run return run function flusgrid:realm/fixture_tick_{short}',
            f'data modify storage {S} bounds.{short} set value {{min_x:{MIN},max_x:{MAX},min_z:{MIN},max_z:{MAX}}}',
            f'execute in {dim} run function flusgrid:realm/platform_{short}',
        ]
        if short == 'overworld':
            lines.append('execute in minecraft:overworld run function flusgrid:realm/portal')
        lines.append(f'execute in {dim} run function flusgrid:realm/fixture_release_{short}')
        if i < 2:
            n,nns,ndim,ntop,nlow,nsections = DIMS[i+1]
            lines += [
                f'data merge storage {S} {{phase:"{n}",owner:"{n}"}}',
                f'execute in {ndim} run function {nns}:pregen/rectangle {{x:{MIN},z:{MIN},ex:{END_ORIGIN},ez:{END_ORIGIN},chunks:390625,total:{390625*nsections}}}',
            ]
        else:
            lines += [
                f'data merge storage {S} {{state:"ready",phase:"complete",live:1b}}',
                f'data remove storage {S} owner',
                'tellraw @a {text:"FlusGrid 10K initial campaign completed. Inspect and back up the world before multiplayer.",color:"green"}',
            ]
        f('complete_'+short,lines)

    f('tick', [
        f'execute if data storage {S} {{state:"ready",live:1b,model:10000}} run function flusgrid:realm/players10',
        f'execute if data storage {S} {{state:"ready",live:1b}} unless data storage {S} {{model:10000}} run function flusgrid:realm/tick_legacy_players',
        f'execute if data storage {S} {{manual_pause:1b}} run return 0',
        *[f'execute if data storage {S} {{state:"preparing",model:10000,phase:"{short}"}} if data storage {ns}:job {{state:"complete"}} run return run function flusgrid:realm/complete_{short}'
          for short,ns,dim,top,low,sections in DIMS],
        *[f'execute if data storage {S} {{state:"ready",model:10000,owner:"{short}"}} if data storage {ns}:job {{state:"complete"}} run return run function flusgrid:realm/tile_complete_{short}'
          for short,ns,dim,top,low,sections in DIMS],
        *[f'execute if data storage {S} {{state:"ready",owner:"{short}"}} unless data storage {S} {{model:10000}} if data storage {ns}:job {{state:"complete"}} run return run function flusgrid:realm/commit_{short}'
          for short,ns,dim,top,low,sections in DIMS],
        f'execute if data storage {S} {{state:"ready",live:1b,model:10000}} unless data storage {S} owner if data storage {S} queue[0] run function flusgrid:realm/tile_start with storage flusgrid:realm queue[0]',
    ])
    f('players10', [
        *[f'execute as @a[gamemode=!creative,gamemode=!spectator] at @s if dimension {dim} run function flusgrid:realm/player10_{short}'
          for short,ns,dim,top,low,sections in DIMS],
    ])
    # Save only verified clear approach points, never a portal tile.
    write('data/flusgrid/tags/block/safe_floor.json',json.dumps({'values':[
        'minecraft:stone','minecraft:cobblestone','minecraft:obsidian','minecraft:crying_obsidian',
        'minecraft:grass_block','minecraft:dirt','minecraft:netherrack','minecraft:end_stone',
        'minecraft:deepslate','minecraft:cobbled_deepslate','minecraft:bedrock','#minecraft:planks']}))
    safe=['scoreboard players set #safe flusgrid 1',
          'execute unless block ~ ~-1 ~ #flusgrid:safe_floor run scoreboard players set #safe flusgrid 0']
    for x in range(-1,2):
        for z in range(-1,2):
            for y in (0,1):
                safe.append(f'execute unless block ~{x} ~{y} ~{z} minecraft:air run scoreboard players set #safe flusgrid 0')
    for x in range(-2,3):
        for z in range(-2,3):
            for y in (-1,0,1):
                for block in ('nether_portal','end_portal','end_gateway'):
                    safe.append(f'execute if block ~{x} ~{y} ~{z} minecraft:{block} run scoreboard players set #safe flusgrid 0')
    f('checkpoint_safe',safe)
    f('checkpoint',[
        *[f'execute store result score @s fg_s{a} run data get entity @s Pos[{i}] 16' for a,i in [('x',0),('y',1),('z',2)]],
        'execute store result score @s fg_yaw run data get entity @s Rotation[0] 1000',
        'execute store result score @s fg_pitch run data get entity @s Rotation[1] 1000',
        'scoreboard players operation @s fg_sd = #current flusgrid',
    ])
    f('tile_coords',[
        *[line for a in 'xz' for line in [
            f'scoreboard players operation #tile_{a} flusgrid = @s fg_{a}',
            f'scoreboard players operation #mod flusgrid = #tile_{a} flusgrid',
            'scoreboard players operation #mod flusgrid %= #tile_size flusgrid',
            f'scoreboard players operation #tile_{a} flusgrid -= #mod flusgrid',
            f'execute store result storage {S} scratch.tile.{a} int 1 run scoreboard players get #tile_{a} flusgrid',
        ]],
    ])
    f('target_to_tile',[
        *[line for a in 'xz' for line in [
            f'scoreboard players operation #r{a} flusgrid = #target_{a} flusgrid',
            f'scoreboard players operation #mod flusgrid = #r{a} flusgrid',
            'scoreboard players operation #mod flusgrid %= #tile_size flusgrid',
            f'scoreboard players operation #r{a} flusgrid -= #mod flusgrid',
            f'execute unless score #r{a} flusgrid matches -29999984..29999472 run return 0',
            f'execute store result storage {S} scratch.request.{a} int 1 run scoreboard players get #r{a} flusgrid',
        ]],
    ])
    # A single queue, persistent across save/reload, with per-dimension dedupe.
    f('tile_start', ['$function flusgrid:realm/tile_start_$(dimension) with storage flusgrid:realm queue[0]'])
    for short,ns,dim,top,low,sections in DIMS:
        idx=DIM_INDEX[short]
        f('tile_lookup_'+short,[
            f'$execute if data storage {S} tiles.{short}."$(x),$(z)" run scoreboard players set #inside flusgrid 1',
        ])
        f('tile_enqueue_'+short,[
            f'$execute if data storage {S} tiles.{short}."$(x),$(z)" run return 0',
            f'$execute if data storage {S} pending.{short}."$(x),$(z)" run return 0',
            f'execute store result score #queue_count flusgrid run data get storage {S} queue',
            'execute if score #queue_count flusgrid matches 64.. run return 0',
            f'$data modify storage {S} pending.{short}."$(x),$(z)" set value 1b',
            f'$data modify storage {S} queue append value {{dimension:"{short}",x:$(x),z:$(z)}}',
        ])
        f('enqueue_'+short,[
            'function flusgrid:realm/target_to_tile',
            f'function flusgrid:realm/tile_enqueue_{short} with storage {S} scratch.request',
        ])
        # Position is integer-block resolution, tile keys are 512-aligned.
        f('player10_'+short,[
            f'scoreboard players set #current flusgrid {idx}',
            *[f'execute store result score @s fg_{a} run data get entity @s Pos[{i}] 1' for a,i in [('x',0),('y',1),('z',2)]],
            'scoreboard players set #inside flusgrid 0',
            'scoreboard players set #main flusgrid 0',
            f'execute if score @s fg_x matches {MIN}..{MAX} if score @s fg_z matches {MIN}..{MAX} run scoreboard players set #main flusgrid 1',
            'execute if score #main flusgrid matches 1 run scoreboard players set #inside flusgrid 1',
            'function flusgrid:realm/tile_coords',
            f'execute if score #inside flusgrid matches 0 run function flusgrid:realm/tile_lookup_{short} with storage {S} scratch.tile',
            f'execute if score #inside flusgrid matches 0 run function flusgrid:realm/request_here_{short}',
            f'execute if score #inside flusgrid matches 1 if score #main flusgrid matches 1 run function flusgrid:realm/request_main_{short}',
            f'execute if score #inside flusgrid matches 1 if score #main flusgrid matches 0 run function flusgrid:realm/request_neighbors_{short}',
            f'execute if score #inside flusgrid matches 0 run return run function flusgrid:realm/hold10_{short}',
            'function flusgrid:realm/checkpoint_safe',
            'execute if score #safe flusgrid matches 1 run function flusgrid:realm/checkpoint',
        ])
        f('request_here_'+short,[
            *[f'scoreboard players operation #target_{a} flusgrid = @s fg_{a}' for a in 'xz'],
            f'function flusgrid:realm/enqueue_{short}',
        ])
        main=[]
        for edge,axis,threshold,coord in [
            ('west','x',f'..{MIN+256}',MIN-1),
            ('east','x',f'{MAX-256}..',MAX+1),
            ('north','z',f'..{MIN+256}',MIN-1),
            ('south','z',f'{MAX-256}..',MAX+1),
        ]:
            main.append(f'execute if score @s fg_{axis} matches {threshold} run function flusgrid:realm/main_{short}_{edge}')
            side='z' if axis=='x' else 'x'
            f('main_'+short+'_'+edge,[
                f'scoreboard players set #target_{axis} flusgrid {coord}',
                f'scoreboard players operation #target_{side} flusgrid = @s fg_{side}',
                f'function flusgrid:realm/enqueue_{short}',
            ])
        f('request_main_'+short,main)
        near=[]
        for edge,axis,offset,compare in [
            ('west','x',-1,'<'),('east','x',512,'>'),
            ('north','z',-1,'<'),('south','z',512,'>'),
        ]:
            side='z' if axis=='x' else 'x'
            near += [
                f'scoreboard players operation #threshold flusgrid = #tile_{axis} flusgrid',
                f'scoreboard players add #threshold flusgrid {192 if offset==-1 else 319}',
                f'execute if score @s fg_{axis} {compare} #threshold flusgrid run function flusgrid:realm/neighbor_{short}_{edge}',
            ]
            f('neighbor_'+short+'_'+edge,[
                f'scoreboard players operation #target_{axis} flusgrid = #tile_{axis} flusgrid',
                (f'scoreboard players remove #target_{axis} flusgrid 1' if offset == -1 else f'scoreboard players add #target_{axis} flusgrid 512'),
                f'scoreboard players operation #target_{side} flusgrid = @s fg_{side}',
                f'function flusgrid:realm/enqueue_{short}',
            ])
        f('request_neighbors_'+short,near)
        f('hold10_'+short,[
            # Same-dimension walking and cross-dimension portal arrivals use the
            # same last verified checkpoint, with NO spawn/skybox fallback.
            *[f'execute store result storage {S} scratch.return.{a} double 0.0625 run scoreboard players get @s fg_s{a}' for a in 'xyz'],
            *[f'execute store result storage {S} scratch.return.{a} double 0.001 run scoreboard players get @s fg_{a}' for a in ('yaw','pitch')],
            *[f'execute if score @s fg_sd matches {n} in {d} run return run function flusgrid:realm/return10 with storage {S} scratch.return' for n,d in [(1,'minecraft:overworld'),(2,'minecraft:the_nether'),(3,'minecraft:the_end')]],
            'title @s actionbar {text:"Region not ready. No saved portal approach; ask an operator for help.",color:"red"}',
        ])
        f('tile_start_'+short,[
            '$scoreboard players set #rx flusgrid $(x)',
            '$scoreboard players set #rz flusgrid $(z)',
            'scoreboard players operation #ex flusgrid = #rx flusgrid',
            'scoreboard players operation #ez flusgrid = #rz flusgrid',
            'scoreboard players add #ex flusgrid 496',
            'scoreboard players add #ez flusgrid 496',
            *[f'execute store result storage {S} rectangle.{a} int 1 run scoreboard players get #{src} flusgrid'
              for a,src in [('x','rx'),('z','rz'),('ex','ex'),('ez','ez')]],
            f'data merge storage {S} rectangle {{chunks:1024,total:{1024*sections}}}',
            f'execute in {dim} run function {ns}:pregen/rectangle with storage {S} rectangle',
            f'execute if data storage {ns}:job {{state:"running"}} run function flusgrid:realm/tile_claim_{short}',
        ])
        f('tile_claim_'+short,[
            f'data modify storage {S} plan set from storage {S} queue[0]',
            f'data modify storage {S} owner set value "{short}"',
            f'data remove storage {S} queue[0]',
            f'tellraw @a {{text:"FlusGrid: queued 512x512 {short} tile started; finished terrain remains guarded.",color:"yellow"}}',
        ])
        f('tile_complete_'+short,[
            f'function flusgrid:realm/tile_mark_{short} with storage {S} plan',
            f'data remove storage {S} owner',
            f'data remove storage {S} plan',
            f'tellraw @a {{text:"FlusGrid: {short} tile finished; that destination is now usable.",color:"green"}}',
        ])
        f('tile_mark_'+short,[
            f'$data modify storage {S} tiles.{short}."$(x),$(z)" set value 1b',
            f'$data remove storage {S} pending.{short}."$(x),$(z)"',
        ])
    # Validation before teleport: loaded source and conservative 3x3 clear floor.
    f('return10', [
        '$execute positioned $(x) $(y) $(z) unless loaded ~ ~ ~ run return run function flusgrid:realm/return_failed',
        '$execute positioned $(x) $(y) $(z) run function flusgrid:realm/checkpoint_safe',
        'execute unless score #safe flusgrid matches 1 run return run function flusgrid:realm/return_failed',
        '$execute store success score #returned flusgrid run tp @s $(x) $(y) $(z) $(yaw) $(pitch)',
        'execute unless score #returned flusgrid matches 1 run return run function flusgrid:realm/return_failed',
        'title @s times 5 60 10',
        'title @s title {text:"Destination not ready",color:"yellow"}',
        'title @s subtitle {text:"Returned to your safe approach",color:"white"}',
        'title @s actionbar {text:"Gridding requested. Try again after the region finishes.",color:"yellow"}',
    ])
    f('return_failed',[
        'effect give @s minecraft:slowness 3 4 true',
        'title @s actionbar {text:"No loaded, clear checkpoint to return to. Contact an operator; no spawn teleport used.",color:"red"}',
    ])
    ef('help',[
        'tellraw @a {text:"FlusGrid 0.7 experimental: setup prepares 10K x 10K in every dimension; beyond that, queued 512x512 tiles are gridded automatically. Use realm_status, realm_pause, realm_resume; archive before importing to Flunkstar.",color:"yellow"}'
    ])
    # Existing source status remains intact; add a readable queue status line.
    ef('realm_status', (pack/'data/flusgrid/function/realm_status.mcfunction').read_text().splitlines() + [
        'tellraw @a [{text:"10K model: "},{nbt:"model",storage:"flusgrid:realm"},{text:" | queued tiles: "},{nbt:"queue",storage:"flusgrid:realm"}]',
    ])
