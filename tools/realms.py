"""One-map campaign, conservative frontier expansion, and End fight exceptions.
All world mutation remains in the existing journaled cube worker.
"""
import json, math

DIMS=[('overworld','flusgrid','minecraft:overworld',304,-64,24),
      ('nether','flusgrid_nether','minecraft:the_nether',240,0,16),
      ('end','flusgrid_end','minecraft:the_end',240,0,16)]

def build_realms(pack,write,function):
    def emit(ns,name,lines):write(f'data/{ns}/function/{name}.mcfunction','\n'.join(lines))
    def read(ns,name):return (pack/f'data/{ns}/function/{name}.mcfunction').read_text().splitlines()
    def pred(name,position):
        write(f'data/flusgrid_end/predicate/{name}.json',json.dumps({'type':'minecraft:location_check','predicate':{'position':position}}))
    end_protection(pack,write,emit,read,pred)
    masked_end_worker(emit,read)
    # Point masks are invoked only by the bounded multi-tick worker.
    for name in ('carve','verify'):
        emit('flusgrid_end','internal/'+name,read('flusgrid_end','internal/'+name+'_fast'))
        for suffix in ('_fast','_protected'):
            (pack/f'data/flusgrid_end/function/internal/{name}{suffix}.mcfunction').unlink()
    campaign(pack,write,function,emit,read)


def end_protection(pack,write,emit,read,pred):
    ns='flusgrid_end'
    pred('arena_cube',{'x':{'min':-64,'max':64},'z':{'min':-64,'max':64}})
    pred('podium',{'x':{'min':-8,'max':8.999},'z':{'min':-8,'max':8.999}})
    pred('arrival',{'x':{'min':97,'max':103.999},'y':{'min':48,'max':51.999},'z':{'min':-3,'max':3.999}})
    # Snapshot caps before touching central terrain. Read all actual bedrock cap heights,
    # rather than assuming seed-dependent spike ordering/heights.
    scan=[]
    points=set()
    for i in range(10):
        angle=2*(-math.pi+math.pi/10*i)
        x,z=42*math.cos(angle),42*math.sin(angle)
        # Tolerate the game's float rounding at axial coordinates.
        for px in {math.floor(x),math.ceil(x),round(x)-1}:
            for pz in {math.floor(z),math.ceil(z),round(z)-1}:
                points.add((px,pz))
    for x,z in sorted(points):
        for y in range(64,129):
            scan.append(f'execute if block {x} {y} {z} minecraft:bedrock run summon minecraft:marker {x} {y} {z} {{Tags:["flusgrid_cap"]}}')
    emit(ns,'arena/scan',['kill @e[type=minecraft:marker,tag=flusgrid_cap]',*scan,
        'execute store result score #cap_count flusgrid if entity @e[type=minecraft:marker,tag=flusgrid_cap]',
        'execute unless score #cap_count flusgrid matches 10 run data modify storage flusgrid_end:job reason set value "Expected ten vanilla pylon caps; refusing unprotected arena conversion."',
        'execute unless score #cap_count flusgrid matches 10 run return run function flusgrid_end:pregen/fail',
        'data modify storage flusgrid_end:arena ready set value 1b'])
    acquire=['data modify storage flusgrid_end:arena tickets set value []','data modify storage flusgrid_end:arena wait set value 0']
    for x in range(-64,65,16):
        for z in range(-64,65,16):acquire.append(f'function flusgrid_end:arena/acquire_one {{x:{x},z:{z}}}')
    acquire += ['data modify storage flusgrid_end:arena acquiring set value 1b']
    emit(ns,'arena/acquire',acquire)
    emit(ns,'arena/acquire_one',[
        '$execute store success score #existing flusgrid run forceload query $(x) $(z)',
        'execute if score #existing flusgrid matches 1 run return 1',
        '$execute store success score #added flusgrid run forceload add $(x) $(z)',
        '$execute if score #added flusgrid matches 1 run data modify storage flusgrid_end:arena tickets append value {x:$(x),z:$(z)}',
    ])
    emit(ns,'arena/release',[
        'execute if data storage flusgrid_end:arena tickets[0] run function flusgrid_end:arena/release_one with storage flusgrid_end:arena tickets[0]',
        'data modify storage flusgrid_end:arena ready set value 0b',
        'data modify storage flusgrid_end:arena acquiring set value 0b',
    ])
    emit(ns,'arena/release_one',[
        '$forceload remove $(x) $(z)',
        'data remove storage flusgrid_end:arena tickets[0]',
        'execute if data storage flusgrid_end:arena tickets[0] run function flusgrid_end:arena/release_one with storage flusgrid_end:arena tickets[0]',
    ])
    ready=['scoreboard players set #arena_loaded flusgrid 1']
    for x in range(-64,65,16):
        for z in range(-64,65,16):ready.append(f'execute unless loaded {x} 80 {z} run scoreboard players set #arena_loaded flusgrid 0')
    emit(ns,'arena/tick',[
        'execute if data storage flusgrid_end:arena {ready:1b} run return 1',
        'execute unless data storage flusgrid_end:arena {acquiring:1b} run return run function flusgrid_end:arena/acquire',
        *ready,
        'execute if score #arena_loaded flusgrid matches 1 run return run function flusgrid_end:arena/scan',
        'execute store result score #arena_wait flusgrid run data get storage flusgrid_end:arena wait',
        'scoreboard players add #arena_wait flusgrid 1',
        'execute store result storage flusgrid_end:arena wait int 1 run scoreboard players get #arena_wait flusgrid',
        'execute if score #arena_wait flusgrid matches 1200.. run data modify storage flusgrid_end:job reason set value "End arena chunks did not load; check force-load capacity and resume."',
        'execute if score #arena_wait flusgrid matches 1200.. run function flusgrid_end:pregen/fail',
    ])
    # Only arena-overlapping jobs need these extra tickets. They survive between cubes,
    # but are released on pause, failure, load and completion.
    step=read(ns,'pregen/step')
    emit(ns,'pregen/step',[
        'execute store result score #eminx flusgrid run data get storage flusgrid_end:job min_x',
        'execute store result score #emaxx flusgrid run data get storage flusgrid_end:job max_x',
        'execute store result score #eminz flusgrid run data get storage flusgrid_end:job min_z',
        'execute store result score #emaxz flusgrid run data get storage flusgrid_end:job max_z',
        'execute if score #eminx flusgrid matches ..64 if score #emaxx flusgrid matches -64.. if score #eminz flusgrid matches ..64 if score #emaxz flusgrid matches -64.. unless data storage flusgrid_end:arena {ready:1b} run return run function flusgrid_end:arena/tick',
        *step])
    for name in ('pause','load','pregen/finish','pregen/fail'):
        emit(ns,name,['execute in minecraft:the_end run function flusgrid_end:arena/release',*read(ns,name)])
    # Migrate only the explicit untouched 0.5 protected records. Never unlock failed,
    # started or completed cubes.
    for name in ('pregen/process','internal/dispatch'):
        emit(ns,name,['$execute if data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"protected"} run data remove storage flusgrid_end:ledger regions."$(x),$(y),$(z)"',*read(ns,name)])
    run=read(ns,'internal/run')
    emit(ns,'internal/run',[
        'execute if predicate flusgrid_end:arena_cube unless data storage flusgrid_end:arena {ready:1b} run return run tellraw @a {text:"End arena protection is not initialized. Use the preparation job.",color:"red"}',
        *run])
    # Fast generic carving everywhere else. Slow mask only in the central 144 square
    # and arrival chunk. Bedrock / exit portal / gateways are progression exceptions.
    emit(ns,'internal/carve_fast',read(ns,'internal/carve'))
    emit(ns,'internal/verify_fast',read(ns,'internal/verify'))
    central='execute if predicate flusgrid_end:arena_cube run return run function flusgrid_end:internal/'
    arrival='execute positioned ~ ~48 ~ if predicate flusgrid_end:arrival run return run function flusgrid_end:internal/'
    # The vanilla arrival platform straddles chunks x96..111,z-16..15.
    pred('arrival_cube',{'x':{'min':96,'max':96},'z':{'min':-16,'max':0}})
    for name in ('carve','verify'):
        emit(ns,'internal/'+name,[central+name+'_protected',
            f'execute if predicate flusgrid_end:arrival_cube run return run function flusgrid_end:internal/{name}_protected',
            f'function flusgrid_end:internal/{name}_fast'])
    guards='unless predicate flusgrid_end:podium unless predicate flusgrid_end:arrival unless block ~ ~ ~ minecraft:bedrock unless block ~ ~ ~ minecraft:end_portal unless block ~ ~ ~ minecraft:end_gateway'
    # Cap markers are at actual bedrock heights. Keep a 13x11x13 neighborhood.
    emit(ns,'internal/carve_point',[
        f'execute {guards} positioned ~-6 ~-5 ~-6 unless entity @e[type=minecraft:marker,tag=flusgrid_cap,dx=12,dy=10,dz=12] positioned ~6 ~5 ~6 run setblock ~ ~ ~ minecraft:air strict'])
    emit(ns,'internal/verify_point',[
        f'execute {guards} unless block ~ ~ ~ minecraft:air positioned ~-6 ~-5 ~-6 unless entity @e[type=minecraft:marker,tag=flusgrid_cap,dx=12,dy=10,dz=12] run scoreboard players add #uncleared flusgrid 1'])
    for name in ('carve','verify'):
        emit(ns,'internal/'+name+'_protected',[
            f'execute positioned ~{x} ~{y} ~{z} run function flusgrid_end:internal/{name}_point'
            for x in range(16) for y in range(16) for z in range(16) if x%4 or y%4 or z%4])

def masked_end_worker(emit,read):
    ns='flusgrid_end'
    process=read(ns,'pregen/process')
    # First lines migrate old protected entries and check that the chunk is loaded.
    emit(ns,'pregen/process',process[:2]+[
        'data modify storage flusgrid_end:job wait set value 0',
        '$execute positioned $(x) $(y) $(z) if predicate flusgrid_end:arena_cube run return run function flusgrid_end:mask/process with storage flusgrid_end:job cursor',
        '$execute positioned $(x) $(y) $(z) if predicate flusgrid_end:arrival_cube run return run function flusgrid_end:mask/process with storage flusgrid_end:job cursor',
    ]+process[2:])
    emit(ns,'internal/run',[
        'execute if predicate flusgrid_end:arena_cube run return run tellraw @a {text:"Use an End preparation job for protected arena cubes.",color:"yellow"}',
        'execute if predicate flusgrid_end:arrival_cube run return 0',
        *read(ns,'internal/run'),
    ])
    emit(ns,'mask/process',[
        '$execute if data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_end:pregen/skip with storage flusgrid_end:job cursor',
        'execute unless data storage flusgrid_end:job mask run return run function flusgrid_end:mask/init with storage flusgrid_end:job cursor',
        '$execute unless data storage flusgrid_end:job mask{x:$(x),y:$(y),z:$(z)} run return run function flusgrid_end:pregen/blocked',
        '$execute unless data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"started"} run return run function flusgrid_end:pregen/blocked',
        'function flusgrid_end:mask/dispatch with storage flusgrid_end:job mask',
    ])
    emit(ns,'mask/init',[
        '$execute if data storage flusgrid_end:ledger regions."$(x),$(y),$(z)" run return run function flusgrid_end:pregen/blocked',
        '$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "started"',
        '$data modify storage flusgrid_end:job mask set value {x:$(x),y:$(y),z:$(z),phase:0,errors:0}',
    ])
    emit(ns,'mask/dispatch',['$function flusgrid_end:mask/phase_$(phase)'])
    for phase in range(8):
        verify=phase>=4
        y0=(phase%4)*4
        lines=[]
        if phase==0:lines.append('function flusgrid_end:internal/preserve_leaves')
        if verify:lines.append('scoreboard players set #uncleared flusgrid 0')
        lines += [f'execute positioned ~{x} ~{y} ~{z} run function flusgrid_end:internal/{"verify" if verify else "carve"}_point'
                  for x in range(16) for y in range(y0,y0+4) for z in range(16) if x%4 or y%4 or z%4]
        if verify:
            lines += ['execute store result score #errors flusgrid run data get storage flusgrid_end:job mask.errors',
                      'scoreboard players operation #errors flusgrid += #uncleared flusgrid',
                      'execute store result storage flusgrid_end:job mask.errors int 1 run scoreboard players get #errors flusgrid']
        lines.append(f'data modify storage flusgrid_end:job mask.phase set value {phase+1}')
        emit(ns,f'mask/phase_{phase}',lines)
    emit(ns,'mask/phase_8',['function flusgrid_end:mask/finish with storage flusgrid_end:job cursor'])
    emit(ns,'mask/finish',[
        '$execute unless data storage flusgrid_end:job mask{errors:0} run data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "failed"',
        'execute unless data storage flusgrid_end:job mask{errors:0} run return run function flusgrid_end:pregen/blocked',
        '$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "complete"',
        'data remove storage flusgrid_end:job mask',
        'function flusgrid_end:pregen/advance',
    ])


def campaign(pack,write,function,emit,read):
    def f(name,lines):function('realm/'+name,lines)
    S='flusgrid:realm'
    # Rectangle API used by the controller, with exact totals computed from aligned bounds.
    for short,ns,dim,top,low,sections in DIMS:
        emit(ns,'pregen/rectangle',[
            f'execute if data storage {ns}:job {{state:"running"}} run return 0',
            f'execute if data storage {ns}:job {{state:"paused"}} run return 0',
            f'execute in {dim} run function {ns}:pregen/release',
            f'$data merge storage {ns}:job {{kind:"pregen",state:"running",done:0,total:$(total),chunks:0,chunk_total:$(chunks),size:0,percent:0,wait:0,reason:"",min_x:$(x),max_x:$(ex),min_z:$(z),max_z:$(ez),cursor:{{x:$(x),y:{top},z:$(z)}}}}',
            f'data remove storage {ns}:job pending',
        ])
    objective_names=['fg_x','fg_y','fg_z','fg_sx','fg_sy','fg_sz','fg_sd']
    load=[*[f'scoreboard objectives add {v} dummy' for v in objective_names],
          'scoreboard players set #sixteen flusgrid 16',
          'scoreboard players set #scan_clock flusgrid 0',
          'scoreboard players set #scan_dim flusgrid 0',
          'execute unless data storage flusgrid:realm initialized run data merge storage flusgrid:realm {initialized:1b,state:"idle",manual_pause:0b,live:0b}',
          *[f'execute in {d} run function flusgrid:realm/fixture_release_{n}' for n,ns,d,top,low,sections in DIMS],
          'execute unless data storage flusgrid:realm {manual_pause:1b} run function flusgrid:realm/resume_owned']
    f('load',load)
    function('setup',[
        'execute unless data storage flusgrid:realm {state:"idle"} run return run function flusgrid:realm_status',
        'execute if entity @a[gamemode=survival] run return run tellraw @a {text:"Prepare before Survival players join; switch the preparation player to Creative/Spectator.",color:"red"}',
        'execute if entity @a[gamemode=adventure] run return 0',
        *[f'execute if data storage {ns}:job {{state:"{state}"}} run return run tellraw @a {{text:"Finish or resume your existing {short} job before setup.",color:"red"}}' for short,ns,dim,top,low,sections in DIMS for state in ['running','paused']],
        'data merge storage flusgrid:realm {state:"preparing",phase:"overworld",manual_pause:0b,live:0b,owner:"overworld"}',
        'execute unless data storage flusgrid:job {state:"complete",min_x:-1024,max_x:1008,min_z:-1024,max_z:1008,done:393216,chunks:16384} in minecraft:overworld run function flusgrid:pregen_2048_start {x:-1024,z:-1024}',
        'tellraw @a {text:"FlusGrid setup started: Overworld, then Nether, then End. Keep the world running. /function flusgrid:realm_status",color:"green"}',
    ])
    function('realm_pause',[
        'data modify storage flusgrid:realm manual_pause set value 1b',
        *[f'execute in {dim} run function {ns}:pause' for short,ns,dim,top,low,sections in DIMS],
        *[f'execute in {dim} run function flusgrid:realm/fixture_release_{short}' for short,ns,dim,top,low,sections in DIMS],
        'tellraw @a {text:"FlusGrid preparation paused. Finished-area travel guard remains active.",color:"yellow"}',
    ])
    function('realm_resume',[
        'data modify storage flusgrid:realm manual_pause set value 0b',
        'function flusgrid:realm/resume_owned',
        'function flusgrid:realm_status',
    ])
    f('resume_owned',[
        f'execute if data storage {S} {{owner:"{short}"}} in {dim} run function {ns}:resume'
        for short,ns,dim,top,low,sections in DIMS])
    function('realm_status',[
        'tellraw @a [{text:"FlusGrid controller: ",color:"yellow"},{nbt:"state",storage:"flusgrid:realm"},{text:" | phase "},{nbt:"phase",storage:"flusgrid:realm"},{text:" | paused "},{nbt:"manual_pause",storage:"flusgrid:realm"},{text:" | active "},{nbt:"owner",storage:"flusgrid:realm"},{text:" | expansion "},{nbt:"plan",storage:"flusgrid:realm"}]',
        *[f'execute if data storage {S} {{owner:"{short}"}} run function {ns}:status' for short,ns,dim,top,low,sections in DIMS],
        'tellraw @a [{text:"Finished bounds: "},{nbt:"bounds",storage:"flusgrid:realm"}]',
    ])
    function('play',[
        'execute unless data storage flusgrid:realm {state:"ready"} run return run function flusgrid:realm_status',
        'data modify storage flusgrid:realm live set value 1b',
        'tellraw @a {text:"FlusGrid automatic expansion and finished-area guard enabled.",color:"green"}',
    ])
    function('archive',[
        'function flusgrid:realm_pause',
        'data modify storage flusgrid:realm live set value 0b',
        'tellraw @a {text:"FlusGrid stopped for archival import: no automatic work or travel guard. Ordinary terrain remains beyond finished bounds.",color:"yellow"}',
    ])
    # Tick controller runs after worker ticks. Never moves a frontier on partial progress.
    f('tick',[
        'execute if data storage flusgrid:realm {state:"ready",live:1b} run function flusgrid:realm/players',
        'execute if data storage flusgrid:realm {manual_pause:1b} run return 0',
        *[f'execute if data storage {S} {{state:"preparing",phase:"{short}"}} if data storage {ns}:job {{state:"complete"}} run return run function flusgrid:realm/complete_{short}' for short,ns,dim,top,low,sections in DIMS],
        *[f'execute if data storage {S} {{state:"ready",owner:"{short}"}} if data storage {ns}:job {{state:"complete"}} run return run function flusgrid:realm/commit_{short}' for short,ns,dim,top,low,sections in DIMS],
    ])
    for i,(short,ns,dim,top,low,sections) in enumerate(DIMS):
        next_dim=DIMS[i+1] if i<2 else None
        minimum,maximum=(-2048,2047) if short=='end' else (-1024,1023)
        lines=[f'execute unless data storage flusgrid:fixtures {short}{{ready:1b}} in {dim} run return run function flusgrid:realm/fixture_tick_{short}',
               f'data modify storage {S} bounds.{short} set value {{min_x:{minimum},max_x:{maximum},min_z:{minimum},max_z:{maximum}}}',
               f'execute in {dim} run function flusgrid:realm/platform_{short}']
        if short=='overworld':lines.append('execute in minecraft:overworld run function flusgrid:realm/portal')
        lines.append(f'execute in {dim} run function flusgrid:realm/fixture_release_{short}')
        if next_dim:
            n,nns,ndim,*_=next_dim
            start=(f'execute in {ndim} run function {nns}:pregen/rectangle {{x:-2048,z:-2048,ex:2032,ez:2032,chunks:65536,total:1048576}}' if n=='end' else f'execute unless data storage {nns}:job {{state:"complete",min_x:-1024,max_x:1008,min_z:-1024,max_z:1008,done:262144,chunks:16384}} in {ndim} run function {nns}:pregen_2048_start {{x:-1024,z:-1024}}')
            lines += [f'data merge storage {S} {{phase:"{n}",owner:"{n}"}}',start]
        else:
            lines += [f'data merge storage {S} {{state:"ready",phase:"complete",live:1b}}',f'data remove storage {S} owner',
                      'tellraw @a {text:"FlusGrid: all three initial regions complete. Automatic expansion and finished-area guard are on. Back up and inspect before uploading to Realms.",color:"green"}']
        f('complete_'+short,lines)
        x,y,z=(100,49,0) if short=='end' else (0,81,0)
        f('platform_'+short,[
            f'execute if data storage {S} platforms{{{short}:1b}} run return 0',
            f'fill {x-3} {y-1} {z-3} {x+3} {y-1} {z+3} minecraft:obsidian strict',
            f'fill {x-3} {y} {z-3} {x+3} {y+3} {z+3} minecraft:air strict',
            *(['setworldspawn 0 81 0','gamerule minecraft:respawn_radius 0'] if short=='overworld' else []),
            f'data modify storage {S} platforms.{short} set value 1b',
        ])
        # Expansion completion commits only the proposed full rectangle.
        f('commit_'+short,[
            f'data modify storage {S} bounds.{short} set from storage {S} plan.bounds',
            f'data remove storage {S} owner',f'data remove storage {S} plan',
            f'tellraw @a {{text:"FlusGrid: {short} frontier expanded. New terrain is ready.",color:"green"}}',
        ])
    portal=[f'execute if data storage {S} {{portal_built:1b}} run return 0',
            'fill -3 -33 -3 3 -33 3 minecraft:obsidian strict',
            'fill -3 -32 -3 3 -29 3 minecraft:air strict']
    for t in range(-1,2):
        for x,z,d in [(-2,t,'east'),(2,t,'west'),(t,-2,'south'),(t,2,'north')]:
            portal.append(f'setblock {x} -32 {z} minecraft:end_portal_frame[facing={d},eye=false] strict')
    portal += [f'data modify storage {S} portal_built set value 1b']
    f('portal',portal)
    # A single global expansion job avoids multiplying load with player count.
    f('players',[
        'scoreboard players add #scan_clock flusgrid 1',
        *[f'execute as @a[sort=random,gamemode=!creative,gamemode=!spectator] at @s if dimension {dim} run function flusgrid:realm/player_{short}' for short,ns,dim,top,low,sections in DIMS],
        'execute if score #scan_clock flusgrid matches 10.. run function flusgrid:realm/scan_advance',
    ])
    f('scan_advance',['scoreboard players set #scan_clock flusgrid 0','scoreboard players add #scan_dim flusgrid 1','execute if score #scan_dim flusgrid matches 3.. run scoreboard players set #scan_dim flusgrid 0'])
    for index,(short,ns,dim,top,low,sections) in enumerate(DIMS):
        lines=[*[f'execute store result score @s fg_{a} run data get entity @s Pos[{j}] 1' for a,j in [('x',0),('y',1),('z',2)]],
               *[f'execute store result score #b{edge} flusgrid run data get storage {S} bounds.{short}.{edge}' for edge in ['min_x','max_x','min_z','max_z']],
               'scoreboard players set #outside flusgrid 0']
        # Request before guard so a distant portal/teleport can also request that direction.
        lines += [f'execute if score #scan_clock flusgrid matches 10.. if score #scan_dim flusgrid matches {index} unless data storage {S} owner unless data storage {S} {{manual_pause:1b}} run function flusgrid:realm/request_{short}']
        for a in 'xz':
            lines += [f'scoreboard players operation #smin_{a} flusgrid = #bmin_{a} flusgrid',f'scoreboard players operation #smax_{a} flusgrid = #bmax_{a} flusgrid',f'scoreboard players add #smin_{a} flusgrid 512',f'scoreboard players remove #smax_{a} flusgrid 512',
                      f'execute if score @s fg_{a} < #smin_{a} flusgrid run scoreboard players set #outside flusgrid 1',
                      f'execute if score @s fg_{a} > #smax_{a} flusgrid run scoreboard players set #outside flusgrid 1']
        lines += [f'execute if score #outside flusgrid matches 1 unless data storage {S} owner unless data storage {S} {{manual_pause:1b}} run function flusgrid:realm/request_{short}',
                  f'execute if score #outside flusgrid matches 1 run return run function flusgrid:realm/hold_{short}',
                  *[f'execute store result score @s fg_s{a} run data get entity @s Pos[{j}] 1000' for a,j in [('x',0),('y',1),('z',2)]],
                  f'scoreboard players set @s fg_sd {index+1}']
        f('player_'+short,lines)
        x,y,z=(100,50,0) if short=='end' else (0,81,0)
        f('hold_'+short,[
            f'execute unless score @s fg_sd matches {index+1} run tp @s {x} {y} {z}',
            *[f'execute if score @s fg_sd matches {index+1} store result storage {S} return.{a} double 0.001 run scoreboard players get @s fg_s{a}' for a in 'xyz'],
            f'execute if score @s fg_sd matches {index+1} run function flusgrid:realm/return with storage {S} return',
            'effect give @s minecraft:slow_falling 3 0 true',
            'title @s actionbar {text:"Preparing the next region. Stay inside the finished frontier.",color:"yellow"}',
        ])
        requests=[]
        for edge,a,sign in [('west','x','min'),('east','x','max'),('north','z','min'),('south','z','max')]:
            op='add' if sign=='min' else 'remove'
            cmp='<=' if sign=='min' else '>='
            requests += [f'scoreboard players operation #trigger flusgrid = #b{sign}_{a} flusgrid',
                         f'scoreboard players {op} #trigger flusgrid 768',
                         f'execute if score @s fg_{a} {cmp} #trigger flusgrid run return run function flusgrid:realm/expand_{short}_{edge}']
        f('request_'+short,requests)
        for edge,a,sign in [('west','x','min'),('east','x','max'),('north','z','min'),('south','z','max')]:
            # Plan holds the new full bounds; job covers only one 512-wide new strip.
            ls=[f'execute if data storage {ns}:job {{state:"running"}} run return 0',
                f'execute if data storage {ns}:job {{state:"paused"}} run return 0',
                f'data modify storage {S} plan set value {{dimension:"{short}",direction:"{edge}"}}',
                f'data modify storage {S} plan.bounds set from storage {S} bounds.{short}',
                *[f'scoreboard players operation #r{b} flusgrid = #bmin_{b} flusgrid' for b in 'xz'],
                *[f'scoreboard players operation #e{b} flusgrid = #bmax_{b} flusgrid' for b in 'xz']]
            if sign=='min':
                ls += [f'scoreboard players operation #e{a} flusgrid = #r{a} flusgrid',f'scoreboard players remove #e{a} flusgrid 1',f'scoreboard players remove #r{a} flusgrid 512',f'execute store result storage {S} plan.bounds.min_{a} int 1 run scoreboard players get #r{a} flusgrid']
            else:
                ls += [f'scoreboard players operation #r{a} flusgrid = #e{a} flusgrid',f'scoreboard players add #r{a} flusgrid 1',f'scoreboard players add #e{a} flusgrid 512',f'execute store result storage {S} plan.bounds.max_{a} int 1 run scoreboard players get #e{a} flusgrid']
            ls += [f'function flusgrid:realm/rectangle_{short}']
            f(f'expand_{short}_{edge}',ls)
        calc=[]
        for a in 'xz':
            calc += [f'execute unless score #r{a} flusgrid matches -29999984..29999968 run return 0',
                     f'execute unless score #e{a} flusgrid matches -29999969..29999983 run return 0',
                     f'scoreboard players operation #n{a} flusgrid = #e{a} flusgrid',f'scoreboard players operation #n{a} flusgrid -= #r{a} flusgrid',
                     f'scoreboard players add #n{a} flusgrid 1',f'scoreboard players operation #n{a} flusgrid /= #sixteen flusgrid',
                     f'scoreboard players remove #e{a} flusgrid 15',
                     f'execute store result storage {S} rectangle.{a} int 1 run scoreboard players get #r{a} flusgrid',
                     f'execute store result storage {S} rectangle.e{a} int 1 run scoreboard players get #e{a} flusgrid']
        calc += ['scoreboard players operation #nx flusgrid *= #nz flusgrid',
                 f'execute store result storage {S} rectangle.chunks int 1 run scoreboard players get #nx flusgrid',
                 f'scoreboard players set #sections flusgrid {sections}',
                 'scoreboard players operation #nx flusgrid *= #sections flusgrid',
                 f'execute store result storage {S} rectangle.total int 1 run scoreboard players get #nx flusgrid',
                 f'execute in {dim} run function {ns}:pregen/rectangle with storage {S} rectangle',
                 f'execute if data storage {ns}:job {{state:"running"}} run data modify storage {S} owner set value "{short}"',
                 f'tellraw @a {{text:"FlusGrid: preparing a new 512-block-wide {short} strip. The frontier opens when it finishes.",color:"yellow"}}']
        f('rectangle_'+short,calc)
    # Stage decorations are placed only after their chunks are ready. Owned tickets
    # are separate from the conversion worker and released before advancing stages.
    for short,ns,dim,top,low,sections in DIMS:
        chunks=[(x,z) for x in ([96] if short=='end' else [-16,0]) for z in [-16,0]]
        path=f'flusgrid:fixtures {short}'
        acq=[f'data modify storage {path} set value {{acquired:1b,ready:0b,wait:0,tickets:[]}}']
        for x,z in chunks:
            acq += [f'execute store success score #existing flusgrid run forceload query {x} {z}',
                    f'execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add {x} {z}',
                    f'execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage {path}.tickets append value {{x:{x},z:{z}}}']
        f('fixture_acquire_'+short,acq)
        f('fixture_tick_'+short,[
            f'execute unless data storage {path}{{acquired:1b}} run return run function flusgrid:realm/fixture_acquire_{short}',
            'scoreboard players set #fixtures_loaded flusgrid 1',
            *[f'execute unless loaded {x} 80 {z} run scoreboard players set #fixtures_loaded flusgrid 0' for x,z in chunks],
            f'execute if score #fixtures_loaded flusgrid matches 1 run return run data modify storage {path}.ready set value 1b',
            f'execute store result score #fixture_wait flusgrid run data get storage {path}.wait',
            'scoreboard players add #fixture_wait flusgrid 1',
            f'execute store result storage {path}.wait int 1 run scoreboard players get #fixture_wait flusgrid',
            f'execute if score #fixture_wait flusgrid matches 1200.. run function flusgrid:realm_pause',
        ])
        f('fixture_release_'+short,[
            f'execute if data storage {path}.tickets[0] run function flusgrid:realm/fixture_release_one_{short} with storage {path}.tickets[0]',
            f'data remove storage {path}',
        ])
        f('fixture_release_one_'+short,[
            '$forceload remove $(x) $(z)',
            f'data remove storage {path}.tickets[0]',
            f'execute if data storage {path}.tickets[0] run function flusgrid:realm/fixture_release_one_{short} with storage {path}.tickets[0]',
        ])
    f('return',['$tp @s $(x) $(y) $(z)'])
    function('help',['tellraw @a {text:"FlusGrid 0.6: /function flusgrid:setup prepares all dimensions. Controls: realm_status, realm_pause, realm_resume. Automatic expansion holds players inside finished terrain when behind. /function flusgrid:archive stops it for archival import.",color:"yellow"}'])
    load=json.loads((pack/'data/minecraft/tags/function/load.json').read_text())
    load['values'].append('flusgrid:realm/load')
    write('data/minecraft/tags/function/load.json',json.dumps(load))
    tick=json.loads((pack/'data/minecraft/tags/function/tick.json').read_text())
    tick['values'].append('flusgrid:realm/tick')
    write('data/minecraft/tags/function/tick.json',json.dumps(tick))
