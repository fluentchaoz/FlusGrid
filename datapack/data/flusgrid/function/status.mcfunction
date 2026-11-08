execute if dimension minecraft:the_nether run return run function flusgrid_nether:status
execute if dimension minecraft:the_end run return run function flusgrid_end:status
execute if data storage flusgrid:job {kind:"pregen"} run return run function flusgrid:pregen/status
tellraw @a [{text:"FlusGrid job: ",color:"yellow"},{nbt:"state",storage:"flusgrid:job"},{text:" | cubes: "},{nbt:"done",storage:"flusgrid:job"},{text:" / "},{nbt:"total",storage:"flusgrid:job"},{text:" | next: "},{nbt:"pending[0]",storage:"flusgrid:job"}]
