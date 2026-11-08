execute if data storage flusgrid_nether:job {kind:"pregen"} run return run function flusgrid_nether:pregen/status
tellraw @a [{text:"FlusGrid job: ",color:"yellow"},{nbt:"state",storage:"flusgrid_nether:job"},{text:" | cubes: "},{nbt:"done",storage:"flusgrid_nether:job"},{text:" / "},{nbt:"total",storage:"flusgrid_nether:job"},{text:" | next: "},{nbt:"pending[0]",storage:"flusgrid_nether:job"}]
