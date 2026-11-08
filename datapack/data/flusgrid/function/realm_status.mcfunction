tellraw @a [{text:"FlusGrid controller: ",color:"yellow"},{nbt:"state",storage:"flusgrid:realm"},{text:" | phase "},{nbt:"phase",storage:"flusgrid:realm"},{text:" | paused "},{nbt:"manual_pause",storage:"flusgrid:realm"},{text:" | active "},{nbt:"owner",storage:"flusgrid:realm"},{text:" | expansion "},{nbt:"plan",storage:"flusgrid:realm"}]
execute if data storage flusgrid:realm {owner:"overworld"} run function flusgrid:status
execute if data storage flusgrid:realm {owner:"nether"} run function flusgrid_nether:status
execute if data storage flusgrid:realm {owner:"end"} run function flusgrid_end:status
tellraw @a [{text:"Finished bounds: "},{nbt:"bounds",storage:"flusgrid:realm"}]
tellraw @a [{text:"10K model: "},{nbt:"model",storage:"flusgrid:realm"},{text:" | queued tiles: "},{nbt:"queue",storage:"flusgrid:realm"}]
