"""Generate isolated vanilla Nether and End workers from the tested converter.
Overworld storage is retained verbatim for upgrades from 0.4.
"""
from pathlib import Path
import json

DIMENSIONS={'nether':('minecraft:the_nether','Nether'), 'end':('minecraft:the_end','End')}

def build_dimensions(pack,write,function):
    base=pack/'data/flusgrid/function'
    # Snapshot before adding aliases/context-aware controls to avoid recursion.
    selected={p.relative_to(base).as_posix()[:-11]:p.read_text() for p in base.rglob('*.mcfunction')
              if p.relative_to(base).parts[0] in ('pregen','internal')
              or p.stem in ('load','pause','resume','status','convert','pregen_here','pregen_start','pregen_2048_here','pregen_2048_start')}
    for short,(dimension,label) in DIMENSIONS.items():
        ns=f'flusgrid_{short}'
        def emit(name,lines):
            write(f'data/{ns}/function/{name}.mcfunction','\n'.join(lines))
        for name,text in selected.items():
            text=(text.replace('flusgrid:',ns+':').replace('minecraft:overworld',dimension)
                  .replace('Overworld',label).replace('-64..304','0..240')
                  .replace('y:304','y:240').replace('set value 304','set value 240')
                  .replace('matches ..-80','matches ..-16')
                  .replace('total:24576','total:16384').replace('total:393216','total:262144')
                  .replace('FlusGrid:',f'FlusGrid {label}:').replace('FlusGrid pregen:',f'FlusGrid {label} pregen:')
                  .replace('FlusGrid preparation:',f'FlusGrid {label} preparation:'))
            emit(name,text.splitlines())
        for name in ('pregen_here','pregen_2048_here'):
            function(f'{short}_{name}',[f'function {ns}:{name}'])
        for name in ('pregen_start','pregen_2048_start'):
            function(f'{short}_{name}',[f'$function {ns}:{name} {{x:$(x),z:$(z)}}'])
        for name in ('pause','resume','status'):
            function(f'{short}_{name}',[f'execute in {dimension} run function {ns}:{name}'])
        if short=='end':
            write(f'data/{ns}/predicate/protected_center.json',json.dumps({
                'type':'minecraft:location_check','predicate':{'position':{
                    'x':{'min':-256,'max':255.999},'z':{'min':-256,'max':255.999}}}},indent=2))
            # Never acquire generation tickets for the protected central square.
            step_path=pack/f'data/{ns}/function/pregen/step.mcfunction'
            step=step_path.read_text().splitlines()
            emit('pregen/step',step[:3]+[f'function {ns}:pregen/step_at with storage {ns}:job cursor'])
            emit('pregen/step_at',[
                f'$execute positioned $(x) 0 $(z) if predicate {ns}:protected_center run return run function {ns}:pregen/protect with storage {ns}:job cursor',
                *step[3:],
            ])
            emit('pregen/protect',[
                f'$data modify storage {ns}:ledger regions."$(x),$(y),$(z)" set value "protected"',
                f'function {ns}:pregen/advance',
            ])
            # Single-cube entry and direct run also preserve the center.
            path=pack/f'data/{ns}/function/internal/run.mcfunction'
            emit('internal/run',[
                f'execute if predicate {ns}:protected_center run return 0',
                *path.read_text().splitlines(),
            ])
    # Existing commands follow the caller's dimension; explicit aliases work anywhere.
    for name in ('pause','resume','status'):
        original=selected[name].splitlines()
        function(name,[
            *[f'execute if dimension {dim} run return run function flusgrid_{short}:{name}' for short,(dim,label) in DIMENSIONS.items()],
            *original,
        ])
    write('data/minecraft/tags/function/load.json',json.dumps({'values':['flusgrid:load','flusgrid_nether:load','flusgrid_end:load']}))
    write('data/minecraft/tags/function/tick.json',json.dumps({'values':['flusgrid:area/tick','flusgrid_nether:pregen/tick','flusgrid_end:pregen/tick']}))
