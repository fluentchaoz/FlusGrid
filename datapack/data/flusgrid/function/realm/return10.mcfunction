$execute positioned $(x) $(y) $(z) unless loaded ~ ~ ~ run return run function flusgrid:realm/return_failed
$execute positioned $(x) $(y) $(z) run function flusgrid:realm/checkpoint_safe
execute unless score #safe flusgrid matches 1 run return run function flusgrid:realm/return_failed
$execute store success score #returned flusgrid run tp @s $(x) $(y) $(z) $(yaw) $(pitch)
execute unless score #returned flusgrid matches 1 run return run function flusgrid:realm/return_failed
title @s times 5 60 10
title @s title {text:"Destination not ready",color:"yellow"}
title @s subtitle {text:"Returned to your safe approach",color:"white"}
title @s actionbar {text:"Gridding requested. Try again after the region finishes.",color:"yellow"}
