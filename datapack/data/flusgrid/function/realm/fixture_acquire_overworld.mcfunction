data modify storage flusgrid:fixtures overworld set value {acquired:1b,ready:0b,wait:0,tickets:[]}
execute store success score #existing flusgrid run forceload query -16 -16
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add -16 -16
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures overworld.tickets append value {x:-16,z:-16}
execute store success score #existing flusgrid run forceload query -16 0
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add -16 0
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures overworld.tickets append value {x:-16,z:0}
execute store success score #existing flusgrid run forceload query 0 -16
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add 0 -16
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures overworld.tickets append value {x:0,z:-16}
execute store success score #existing flusgrid run forceload query 0 0
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add 0 0
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures overworld.tickets append value {x:0,z:0}
