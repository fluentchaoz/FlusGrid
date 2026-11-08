$execute if data storage flusgrid:realm tiles.overworld."$(x),$(z)" run return 0
$execute if data storage flusgrid:realm pending.overworld."$(x),$(z)" run return 0
execute store result score #queue_count flusgrid run data get storage flusgrid:realm queue
execute if score #queue_count flusgrid matches 64.. run return 0
$data modify storage flusgrid:realm pending.overworld."$(x),$(z)" set value 1b
$data modify storage flusgrid:realm queue append value {dimension:"overworld",x:$(x),z:$(z)}
