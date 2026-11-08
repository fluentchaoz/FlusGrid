execute unless data storage flusgrid:realm {state:"idle"} run return run function flusgrid:realm_status
execute if entity @a[gamemode=survival] run return run tellraw @a {text:"Finish setup before Survival joins.",color:"red"}
execute if entity @a[gamemode=adventure] run return 0
execute if data storage flusgrid:job {state:"running"} run return run tellraw @a {text:"Finish the existing overworld preparation before setup.",color:"red"}
execute if data storage flusgrid:job {state:"paused"} run return run tellraw @a {text:"Finish the existing overworld preparation before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"running"} run return run tellraw @a {text:"Finish the existing nether preparation before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"paused"} run return run tellraw @a {text:"Finish the existing nether preparation before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"running"} run return run tellraw @a {text:"Finish the existing end preparation before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"paused"} run return run tellraw @a {text:"Finish the existing end preparation before setup.",color:"red"}
data merge storage flusgrid:realm {model:10000,state:"preparing",phase:"overworld",manual_pause:0b,live:0b,owner:"overworld"}
execute in minecraft:overworld run function flusgrid:pregen/rectangle {x:-5008,z:-5008,ex:4976,ez:4976,chunks:390625,total:9375000}
tellraw @a {text:"FlusGrid 10K setup started. Three 10,000-block-wide squares, one dimension at a time. This can require many days; status/pause/resume remain available.",color:"yellow"}
