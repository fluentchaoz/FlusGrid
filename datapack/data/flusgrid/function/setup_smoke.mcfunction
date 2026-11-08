execute unless data storage flusgrid:realm {state:"idle"} run return run function flusgrid:realm_status
execute if entity @a[gamemode=survival] run return run tellraw @a {text:"Finish setup before Survival joins.",color:"red"}
execute if entity @a[gamemode=adventure] run return 0
execute if data storage flusgrid:job {state:"running"} run return run tellraw @a {text:"Finish the existing overworld preparation before setup.",color:"red"}
execute if data storage flusgrid:job {state:"paused"} run return run tellraw @a {text:"Finish the existing overworld preparation before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"running"} run return run tellraw @a {text:"Finish the existing nether preparation before setup.",color:"red"}
execute if data storage flusgrid_nether:job {state:"paused"} run return run tellraw @a {text:"Finish the existing nether preparation before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"running"} run return run tellraw @a {text:"Finish the existing end preparation before setup.",color:"red"}
execute if data storage flusgrid_end:job {state:"paused"} run return run tellraw @a {text:"Finish the existing end preparation before setup.",color:"red"}
data merge storage flusgrid:realm {model:10000,smoke:1b,edge_lead:64,state:"preparing",phase:"overworld",manual_pause:0b,live:0b,owner:"overworld",start_bounds:{min_x:-128,max_x:127,min_z:-128,max_z:127}}
function flusgrid:realm/initial_start_overworld
tellraw @a {text:"FlusGrid SMOKE setup started: 256x256 per dimension, then the real tile scheduler. Disposable test worlds only.",color:"yellow"}
