"""Bounded pre-generation: one owned force-load ticket and a compact cursor."""

def build_pregen(function):
    function('pregen_here', [
        'execute unless entity @s[type=minecraft:player] run return 0',
        'execute unless dimension minecraft:overworld run return 0',
        'execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] run return run tellraw @s {text:"Prepare a disposable world in Creative or Spectator first.",color:"red"}',
        'execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status',
        'execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status',
        *[line for axis,index in [('x',0),('z',2)] for line in [
            f'execute store result score #p{axis} flusgrid run data get entity @s Pos[{index}] 1',
            f'scoreboard players operation #mod flusgrid = #p{axis} flusgrid',
            'scoreboard players operation #mod flusgrid %= #sixteen flusgrid',
            f'scoreboard players operation #p{axis} flusgrid -= #mod flusgrid',
            f'scoreboard players remove #p{axis} flusgrid 256',
            f'execute store result storage flusgrid:work pregen.{axis} int 1 run scoreboard players get #p{axis} flusgrid',
        ]],
        'function flusgrid:pregen_start with storage flusgrid:work pregen',
    ])
    function('pregen_start', [
        '# Explicit minimum corner. Exactly 32x32 chunks; fixed 512-block side.',
        'execute unless dimension minecraft:overworld run return 0',
        'execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status',
        'execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status',
        '$scoreboard players set #px flusgrid $(x)',
        '$scoreboard players set #pz flusgrid $(z)',
        *[line for axis in 'xz' for line in [
            f'execute unless score #p{axis} flusgrid matches -29999984..29999472 run return 0',
            f'scoreboard players operation #mod flusgrid = #p{axis} flusgrid',
            'scoreboard players operation #mod flusgrid %= #sixteen flusgrid',
            'execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid: X and Z must be multiples of 16.",color:"red"}',
        ]],
        'execute in minecraft:overworld run function flusgrid:pregen/release',
        'data merge storage flusgrid:job {kind:"pregen",state:"preparing",done:0,total:24576,chunks:0,percent:0,wait:0,reason:"",cursor:{y:304}}',
        'data remove storage flusgrid:job pending',
        *[line for axis in 'xz' for line in [
            f'execute store result storage flusgrid:job cursor.{axis} int 1 run scoreboard players get #p{axis} flusgrid',
            f'execute store result storage flusgrid:job min_{axis} int 1 run scoreboard players get #p{axis} flusgrid',
            f'scoreboard players add #p{axis} flusgrid 496',
            f'execute store result storage flusgrid:job max_{axis} int 1 run scoreboard players get #p{axis} flusgrid',
        ]],
        'data modify storage flusgrid:job state set value "running"',
        'tellraw @a {text:"FlusGrid: preparing 512x512 blocks, full Overworld height. 1,024 chunks; at most one owned force-load ticket. Keep this local world running; do not play Survival yet. Controls: status, pause, resume.",color:"yellow"}',
        'function flusgrid:pregen/status',
    ])
    function('pregen/tick', [
        'execute unless data storage flusgrid:job {state:"running",kind:"pregen"} run return 0',
        'execute in minecraft:overworld run function flusgrid:pregen/step',
    ])
    function('pregen/step', [
        'execute if data storage flusgrid:job {done:24576} run return run function flusgrid:pregen/finish',
        'execute unless data storage flusgrid:job ticket run return run function flusgrid:pregen/acquire with storage flusgrid:job cursor',
        'function flusgrid:pregen/process with storage flusgrid:job cursor',
    ])
    function('pregen/acquire', [
        '$data modify storage flusgrid:job ticket set value {x:$(x),z:$(z),owned:0b}',
        '$execute store success score #existing flusgrid run forceload query $(x) $(z)',
        'execute if score #existing flusgrid matches 1 run return 1',
        'data modify storage flusgrid:job ticket.owned set value 1b',
        '$execute store success score #added flusgrid run forceload add $(x) $(z)',
        'execute unless score #added flusgrid matches 1 run data modify storage flusgrid:job reason set value "Could not force-load the next chunk."',
        'execute unless score #added flusgrid matches 1 run function flusgrid:pregen/fail',
    ])
    function('pregen/process', [
        '$execute positioned $(x) 0 $(z) unless loaded ~ ~ ~ run return run function flusgrid:pregen/wait',
        'data modify storage flusgrid:job wait set value 0',
        '$execute if data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:pregen/advance',
        '$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run function flusgrid:pregen/blocked',
        'data modify storage flusgrid:work origin set from storage flusgrid:job cursor',
        'scoreboard players set #quiet flusgrid 1',
        '$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin',
        'scoreboard players set #quiet flusgrid 0',
        '$execute unless data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:pregen/blocked',
        'function flusgrid:pregen/advance',
    ])
    function('pregen/wait', [
        'execute store result score #wait flusgrid run data get storage flusgrid:job wait',
        'scoreboard players add #wait flusgrid 1',
        'execute store result storage flusgrid:job wait int 1 run scoreboard players get #wait flusgrid',
        'execute if score #wait flusgrid matches 1200.. run data modify storage flusgrid:job reason set value "Chunk generation wait exceeded 1,200 ticks. Resume to try loading again."',
        'execute if score #wait flusgrid matches 1200.. run function flusgrid:pregen/fail',
    ])
    function('pregen/advance', [
        'execute store result score #done flusgrid run data get storage flusgrid:job done',
        'scoreboard players add #done flusgrid 1',
        'execute store result storage flusgrid:job done int 1 run scoreboard players get #done flusgrid',
        'execute store result score #py flusgrid run data get storage flusgrid:job cursor.y',
        'scoreboard players remove #py flusgrid 16',
        'execute store result storage flusgrid:job cursor.y int 1 run scoreboard players get #py flusgrid',
        'execute if score #py flusgrid matches ..-80 run function flusgrid:pregen/next_chunk',
    ])
    function('pregen/next_chunk', [
        'function flusgrid:pregen/release',
        'execute store result score #chunks flusgrid run data get storage flusgrid:job chunks',
        'scoreboard players add #chunks flusgrid 1',
        'execute store result storage flusgrid:job chunks int 1 run scoreboard players get #chunks flusgrid',
        'scoreboard players operation #percent flusgrid = #chunks flusgrid',
        'scoreboard players set #hundred flusgrid 100',
        'scoreboard players set #chunk_total flusgrid 1024',
        'scoreboard players operation #percent flusgrid *= #hundred flusgrid',
        'scoreboard players operation #percent flusgrid /= #chunk_total flusgrid',
        'execute store result storage flusgrid:job percent int 1 run scoreboard players get #percent flusgrid',
        'title @a actionbar [{text:"FlusGrid preparation: "},{nbt:"percent",storage:"flusgrid:job"},{text:"% | "},{nbt:"chunks",storage:"flusgrid:job"},{text:" / 1024 chunks"}]',
        'execute if score #chunks flusgrid matches 1024 run return run function flusgrid:pregen/finish',
        'data modify storage flusgrid:job cursor.y set value 304',
        'execute store result score #px flusgrid run data get storage flusgrid:job cursor.x',
        'execute store result score #max_x flusgrid run data get storage flusgrid:job max_x',
        'scoreboard players add #px flusgrid 16',
        'execute if score #px flusgrid > #max_x flusgrid run function flusgrid:pregen/next_row',
        'execute store result storage flusgrid:job cursor.x int 1 run scoreboard players get #px flusgrid',
    ])
    function('pregen/next_row', [
        'execute store result score #px flusgrid run data get storage flusgrid:job min_x',
        'execute store result score #pz flusgrid run data get storage flusgrid:job cursor.z',
        'scoreboard players add #pz flusgrid 16',
        'execute store result storage flusgrid:job cursor.z int 1 run scoreboard players get #pz flusgrid',
    ])
    function('pregen/release', [
        'execute if data storage flusgrid:job ticket{owned:1b} run function flusgrid:pregen/remove_ticket with storage flusgrid:job ticket',
        'data remove storage flusgrid:job ticket',
    ])
    function('pregen/remove_ticket', ['$forceload remove $(x) $(z)'])
    function('pregen/blocked', [
        'data modify storage flusgrid:job reason set value "Next cube is interrupted or failed. Restore your test backup; do not erase the ledger."',
        'function flusgrid:pregen/fail',
    ])
    function('pregen/fail', [
        'data modify storage flusgrid:job state set value "paused"',
        'execute in minecraft:overworld run function flusgrid:pregen/release',
        'function flusgrid:pregen/status',
    ])
    function('pregen/finish', [
        'execute in minecraft:overworld run function flusgrid:pregen/release',
        'data modify storage flusgrid:job state set value "complete"',
        'data modify storage flusgrid:job reason set value ""',
        'tellraw @a {text:"FlusGrid: 512x512 preparation complete! 1,024 chunks handled; owned force-load ticket released. Terrain beyond the prepared square remains normal.",color:"green"}',
    ])
    function('pregen/status', [
        'tellraw @a [{text:"FlusGrid pregen: ",color:"yellow"},{nbt:"state",storage:"flusgrid:job"},{text:" | "},{nbt:"percent",storage:"flusgrid:job"},{text:"% | chunks "},{nbt:"chunks",storage:"flusgrid:job"},{text:"/1024 | cubes "},{nbt:"done",storage:"flusgrid:job"},{text:"/24576 | next "},{nbt:"cursor",storage:"flusgrid:job"},{text:" | "},{nbt:"reason",storage:"flusgrid:job"}]',
    ])
