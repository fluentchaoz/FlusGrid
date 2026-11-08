"""Build the bounded prototype using only Python's standard library."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'datapack'

def write(path, content):
    p = PACK / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + '\n', encoding='utf-8')

def function(name, lines):
    write(f'data/flusgrid/function/{name}.mcfunction', '\n'.join(lines))

def boxes():
    # Disjoint complement of x=y=z=0 (mod 4) in one 16-cube.
    for y in range(16):
        if y % 4:
            yield (0,y,0,15,y,15)
        else:
            for x in range(16):
                if x % 4:
                    yield (x,y,0,x,y,15)
                else:
                    for z in range(1,16,4):
                        yield (x,y,z,x,y,z+2)

def build():
    write('pack.mcmeta', json.dumps({'pack': {'description':'FlusGrid 0.5.0 — bounded experimental converter', 'min_format':[121,0], 'max_format':[121,0]}}, indent=2))
    write('data/minecraft/tags/function/load.json', json.dumps({'values':['flusgrid:load']}))
    function('load', [
        'scoreboard objectives add flusgrid dummy',
        'scoreboard players set #quiet flusgrid 0',
        'execute in minecraft:overworld run function flusgrid:pregen/release',
        'execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"',
        'scoreboard players set #sixteen flusgrid 16',
        'execute if data storage flusgrid:job {kind:"pregen"} unless data storage flusgrid:job chunk_total run data modify storage flusgrid:job chunk_total set value 1024',
        'execute if data storage flusgrid:job {kind:"pregen"} unless data storage flusgrid:job size run data modify storage flusgrid:job size set value 512',
        'execute unless data storage flusgrid:ledger regions run data modify storage flusgrid:ledger regions set value {}',
    ])
    from area import build_area
    build_area(write, function)
    from pregen import build_pregen
    build_pregen(function)
    from leaves import build_leaves
    build_leaves(function)
    function('help', ['tellraw @a {text:"FlusGrid 0.5.0: disposable Creative worlds only. /function flusgrid:pregen_2048_here prepares 2048x2048 terrain through full height. Controls: flusgrid:status, flusgrid:pause, flusgrid:resume. Nether/End: use dimension-specific prep commands.",color:"yellow"}'])
    function('convert', [
        '# Operator API. Explicit integer origins; no relative coordinates.',
        'execute if data storage flusgrid:job {state:"running"} run return 0',
        'execute if data storage flusgrid:job {state:"paused"} run return 0',
        'execute unless dimension minecraft:overworld run return run tellraw @a {text:"FlusGrid: Overworld only.",color:"red"}',
        '$scoreboard players set #x flusgrid $(x)',
        '$scoreboard players set #y flusgrid $(y)',
        '$scoreboard players set #z flusgrid $(z)',
        'execute unless score #x flusgrid matches -29999984..29999968 run return 0',
        'execute unless score #z flusgrid matches -29999984..29999968 run return 0',
        'execute unless score #y flusgrid matches -64..304 run return 0',
        *[line for axis in 'xyz' for line in [
            f'scoreboard players operation #mod flusgrid = #{axis} flusgrid',
            'scoreboard players operation #mod flusgrid %= #sixteen flusgrid',
            'execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid: origins must be multiples of 16.",color:"red"}',
        ]],
        *[f'execute store result storage flusgrid:work origin.{axis} int 1 run scoreboard players get #{axis} flusgrid' for axis in 'xyz'],
        'function flusgrid:internal/dispatch with storage flusgrid:work origin',
    ])
    function('internal/dispatch', [
        '$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run tellraw @a {text:"FlusGrid: region already recorded; refusing another conversion. Inspect /data get storage flusgrid:ledger",color:"yellow"}',
        '$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin',
    ])
    function('internal/run', [
        'execute unless loaded ~ ~ ~ run return run tellraw @a {text:"FlusGrid: target chunk is not loaded. Move closer and retry.",color:"red"}',
        'execute unless loaded ~15 ~15 ~15 run return 0',
        '$data modify storage flusgrid:ledger regions."$(x),$(y),$(z)" set value "started"',
        'function flusgrid:internal/preserve_leaves',
        'function flusgrid:internal/carve',
        'scoreboard players set #uncleared flusgrid 0',
        'function flusgrid:internal/verify',
        '$execute unless score #uncleared flusgrid matches 0 run data modify storage flusgrid:ledger regions."$(x),$(y),$(z)" set value "failed"',
        'execute unless score #uncleared flusgrid matches 0 run return run tellraw @a {text:"FlusGrid: verification FAILED. Region is locked; restore your disposable world backup. Do not retry by deleting the ledger.",color:"red"}',
        '$data modify storage flusgrid:ledger regions."$(x),$(y),$(z)" set value "complete"',
        '$execute unless score #quiet flusgrid matches 1 run tellraw @a {text:"FlusGrid: converted cube at $(x), $(y), $(z). Four-block spacing; 64 grid positions retained. Later physics can change blocks.",color:"green"}',
    ])
    function('internal/carve', ['# Generated; strict suppresses immediate neighbor/shape updates.'] + [
        'fill ' + ' '.join(f'~{v}' for v in box) + ' minecraft:air strict' for box in boxes()
    ])
    function('internal/verify', ['# Verify every removed position before marking complete.'] + [
        f'execute unless block ~{x} ~{y} ~{z} minecraft:air run scoreboard players add #uncleared flusgrid 1'
        for x in range(16) for y in range(16) for z in range(16)
        if x%4 or y%4 or z%4
    ])
    from dimensions import build_dimensions
    build_dimensions(PACK, write, function)
    out = ROOT / 'dist' / 'FlusGrid-0.5.0-experimental.zip'
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PACK.rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(PACK))
    print(out)

if __name__ == '__main__': build()
