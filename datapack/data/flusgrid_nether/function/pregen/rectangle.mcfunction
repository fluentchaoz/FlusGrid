execute if data storage flusgrid_nether:job {state:"running"} run return 0
execute if data storage flusgrid_nether:job {state:"paused"} run return 0
execute in minecraft:the_nether run function flusgrid_nether:pregen/release
$data merge storage flusgrid_nether:job {kind:"pregen",state:"running",done:0,total:$(total),chunks:0,chunk_total:$(chunks),size:0,percent:0,wait:0,reason:"",min_x:$(x),max_x:$(ex),min_z:$(z),max_z:$(ez),cursor:{x:$(x),y:240,z:$(z)}}
data remove storage flusgrid_nether:job pending
