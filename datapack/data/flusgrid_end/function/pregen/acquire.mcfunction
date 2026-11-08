$data modify storage flusgrid_end:job ticket set value {x:$(x),z:$(z),owned:0b}
$execute store success score #existing flusgrid run forceload query $(x) $(z)
execute if score #existing flusgrid matches 1 run return 1
data modify storage flusgrid_end:job ticket.owned set value 1b
$execute store success score #added flusgrid run forceload add $(x) $(z)
execute unless score #added flusgrid matches 1 run data modify storage flusgrid_end:job reason set value "Could not force-load the next chunk."
execute unless score #added flusgrid matches 1 run function flusgrid_end:pregen/fail
