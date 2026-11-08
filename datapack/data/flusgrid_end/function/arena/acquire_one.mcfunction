$execute store success score #existing flusgrid run forceload query $(x) $(z)
execute if score #existing flusgrid matches 1 run return 1
$execute store success score #added flusgrid run forceload add $(x) $(z)
$execute if score #added flusgrid matches 1 run data modify storage flusgrid_end:arena tickets append value {x:$(x),z:$(z)}
