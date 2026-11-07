"""Generate the bounded, resumable 3x3-chunk preparation queue."""
import json

def build_area(write, function):
    write('data/minecraft/tags/function/tick.json', json.dumps({'values':['flusgrid:area/tick']}))
    function('area_here', [
        'execute unless entity @s[type=minecraft:player] run return 0',
        'execute unless dimension minecraft:overworld run return 0',
        'execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] run return run tellraw @s {text:"Use Creative or Spectator in your disposable test world.",color:"red"}',
        'execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status',
        'execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status',
        *[line for axis,index in [('x',0),('z',2)] for line in [
            f'execute store result score #a{axis} flusgrid run data get entity @s Pos[{index}] 1',
            f'scoreboard players operation #mod flusgrid = #a{axis} flusgrid',
            'scoreboard players operation #mod flusgrid %= #sixteen flusgrid',
            f'scoreboard players operation #a{axis} flusgrid -= #mod flusgrid',
            f'scoreboard players remove #a{axis} flusgrid 16',
            f'execute store result storage flusgrid:work area.{axis} int 1 run scoreboard players get #a{axis} flusgrid',
        ]],
        'function flusgrid:area_start with storage flusgrid:work area',
    ])
    function('area_start', [
        '# Explicit lower X/Z corner API. 48x48 blocks, Y -64..319.',
        'execute unless dimension minecraft:overworld run return 0',
        'execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status',
        'execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status',
        '$scoreboard players set #ax flusgrid $(x)',
        '$scoreboard players set #az flusgrid $(z)',
        *[line for axis in 'xz' for line in [
            f'execute unless score #a{axis} flusgrid matches -29999984..29999936 run return 0',
            f'scoreboard players operation #mod flusgrid = #a{axis} flusgrid',
            'scoreboard players operation #mod flusgrid %= #sixteen flusgrid',
            'execute unless score #mod flusgrid matches 0 run return 0',
        ]],
        'data merge storage flusgrid:job {kind:"area",state:"preparing",pending:[],done:0,total:216}',
        'function flusgrid:area/enqueue',
        'data modify storage flusgrid:job state set value "running"',
        'tellraw @a {text:"FlusGrid: preparing 48x48 terrain, Y -64 through 319. Stay nearby in Creative/Spectator. /function flusgrid:pause stops between cubes.",color:"yellow"}',
    ])
    lines=[]
    for dx in range(0,48,16):
        for dz in range(0,48,16):
            for y in range(304,-65,-16):
                lines += [
                    'scoreboard players operation #qx flusgrid = #ax flusgrid',
                    f'scoreboard players add #qx flusgrid {dx}',
                    'scoreboard players operation #qz flusgrid = #az flusgrid',
                    f'scoreboard players add #qz flusgrid {dz}',
                    'execute store result storage flusgrid:work next.x int 1 run scoreboard players get #qx flusgrid',
                    f'data modify storage flusgrid:work next.y set value {y}',
                    'execute store result storage flusgrid:work next.z int 1 run scoreboard players get #qz flusgrid',
                    'data modify storage flusgrid:job pending append from storage flusgrid:work next',
                ]
    function('area/enqueue',lines)
    function('area/tick', [
        'execute if data storage flusgrid:job {kind:"pregen"} run return run function flusgrid:pregen/tick',
        'execute unless data storage flusgrid:job {state:"running"} run return 0',
        'execute in minecraft:overworld run function flusgrid:area/step',
    ])
    function('area/step', [
        'execute unless data storage flusgrid:job pending[0] run return run function flusgrid:area/finish',
        'data modify storage flusgrid:work origin set from storage flusgrid:job pending[0]',
        'function flusgrid:area/process with storage flusgrid:work origin',
    ])
    function('area/process', [
        '$execute if data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:area/advance',
        '$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run function flusgrid:area/blocked',
        '$execute positioned $(x) $(y) $(z) unless loaded ~ ~ ~ run return run function flusgrid:area/unloaded',
        'scoreboard players set #quiet flusgrid 1',
        '$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin',
        'scoreboard players set #quiet flusgrid 0',
        '$execute unless data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:area/blocked',
        'function flusgrid:area/advance',
    ])
    function('area/advance', [
        'data remove storage flusgrid:job pending[0]',
        'execute store result score #done flusgrid run data get storage flusgrid:job done',
        'scoreboard players add #done flusgrid 1',
        'execute store result storage flusgrid:job done int 1 run scoreboard players get #done flusgrid',
        'execute unless data storage flusgrid:job pending[0] run function flusgrid:area/finish',
    ])
    function('area/finish', ['data modify storage flusgrid:job state set value "complete"',
        'tellraw @a {text:"FlusGrid: full-height 48x48 area complete (216 cubes). Original grid-position blocks retained. Surrounding terrain is unchanged.",color:"green"}'])
    function('area/blocked', ['data modify storage flusgrid:job state set value "paused"',
        'tellraw @a {text:"FlusGrid paused: a cube is failed or interrupted. Inspect /function flusgrid:status. Restore a backup; do not erase the region ledger to retry.",color:"red"}'])
    function('area/unloaded', ['data modify storage flusgrid:job state set value "paused"',
        'tellraw @a {text:"FlusGrid paused: next chunk is unloaded. Stay near the area, let terrain load, then /function flusgrid:resume.",color:"yellow"}'])
    function('pause', ['execute in minecraft:overworld run function flusgrid:pregen/release','execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"','function flusgrid:status'])
    function('resume', ['execute unless data storage flusgrid:job {state:"paused"} run return run function flusgrid:status','data modify storage flusgrid:job wait set value 0','data modify storage flusgrid:job reason set value ""','data modify storage flusgrid:job state set value "running"','tellraw @a {text:"FlusGrid resumed. Keep this preparation world running.",color:"yellow"}'])
    function('status', ['execute if data storage flusgrid:job {kind:"pregen"} run return run function flusgrid:pregen/status','tellraw @a [{text:"FlusGrid job: ",color:"yellow"},{nbt:"state",storage:"flusgrid:job"},{text:" | cubes: "},{nbt:"done",storage:"flusgrid:job"},{text:" / "},{nbt:"total",storage:"flusgrid:job"},{text:" | next: "},{nbt:"pending[0]",storage:"flusgrid:job"}]'])
