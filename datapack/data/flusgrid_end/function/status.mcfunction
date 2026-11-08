execute if data storage flusgrid_end:job {kind:"pregen"} run return run function flusgrid_end:pregen/status
tellraw @a [{text:"FlusGrid job: ",color:"yellow"},{nbt:"state",storage:"flusgrid_end:job"},{text:" | cubes: "},{nbt:"done",storage:"flusgrid_end:job"},{text:" / "},{nbt:"total",storage:"flusgrid_end:job"},{text:" | next: "},{nbt:"pending[0]",storage:"flusgrid_end:job"}]
