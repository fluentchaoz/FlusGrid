data modify storage flusgrid:fixtures end set value {acquired:1b,ready:0b,wait:0,tickets:[]}
execute store success score #existing flusgrid run forceload query 96 -16
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add 96 -16
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures end.tickets append value {x:96,z:-16}
execute store success score #existing flusgrid run forceload query 96 0
execute unless score #existing flusgrid matches 1 store success score #added flusgrid run forceload add 96 0
execute unless score #existing flusgrid matches 1 if score #added flusgrid matches 1 run data modify storage flusgrid:fixtures end.tickets append value {x:96,z:0}
