execute if data storage flusgrid:job {state:"running"} run return 0
execute if data storage flusgrid:job {state:"paused"} run return 0
execute in minecraft:overworld run function flusgrid:pregen/release
$data merge storage flusgrid:job {kind:"pregen",state:"running",done:0,total:$(total),chunks:0,chunk_total:$(chunks),size:0,percent:0,wait:0,reason:"",min_x:$(x),max_x:$(ex),min_z:$(z),max_z:$(ez),cursor:{x:$(x),y:304,z:$(z)}}
data remove storage flusgrid:job pending
