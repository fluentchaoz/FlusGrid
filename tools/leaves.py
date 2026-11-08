"""26.3 vanilla leaf species, extracted from its shipped block/leaves tag.
Only persistence changes; species, waterlogging and distance are preserved.
"""
LEAVES = ['jungle','oak','spruce','pale_oak','dark_oak','acacia','birch','azalea','flowering_azalea','mangrove','cherry','red_poplar','orange_poplar','yellow_poplar']

def build_leaves(function):
    function('internal/preserve_leaves',[
        f'execute positioned ~{x} ~{y} ~{z} if block ~ ~ ~ #minecraft:leaves[persistent=false] run function flusgrid:internal/persist_leaf'
        for x in range(0,16,4) for y in range(0,16,4) for z in range(0,16,4)
    ])
    function('internal/persist_leaf',[
        f'execute if block ~ ~ ~ minecraft:{leaf}_leaves[persistent=false,distance={distance},waterlogged={water}] run return run setblock ~ ~ ~ minecraft:{leaf}_leaves[persistent=true,distance={distance},waterlogged={water}] strict'
        for leaf in LEAVES for distance in range(1,8) for water in ['false','true']
    ])
