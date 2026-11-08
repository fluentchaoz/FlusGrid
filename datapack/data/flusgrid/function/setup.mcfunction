execute unless data storage flusgrid:realm {state:"idle"} run return run function flusgrid:realm_status
execute if entity @a[gamemode=survival] run return run tellraw @a {text:"Prepare before Survival players join; switch the preparation player to Creative/Spectator.",color:"red"}
execute if entity @a[gamemode=adventure] run return 0
execute if data storage flusgrid:job {state:"running"} run return run tellraw @a {text:"Finish or resume your existing overworld job before setup.",color:"red"}
execute if data storage flusgrid:job {state:"paused"} run return run tellraw @a {text:"Finish or resume your existing overworld job before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"running"} run return run tellraw @a {text:"Finish or resume your existing nether job before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"paused"} run return run tellraw @a {text:"Finish or resume your existing nether job before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"running"} run return run tellraw @a {text:"Finish or resume your existing end job before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"paused"} run return run tellraw @a {text:"Finish or resume your existing end job before setup.",color:"red"}
data merge storage flusgrid:realm {state:"preparing",phase:"overworld",manual_pause:0b,live:0b,owner:"overworld"}
execute unless data storage flusgrid:job {state:"complete",min_x:-1024,max_x:1008,min_z:-1024,max_z:1008,done:393216,chunks:16384} in minecraft:overworld run function flusgrid:pregen_2048_start {x:-1024,z:-1024}
tellraw @a {text:"FlusGrid setup started: Overworld, then Nether, then End. Keep the world running. /function flusgrid:realm_status",color:"green"}
