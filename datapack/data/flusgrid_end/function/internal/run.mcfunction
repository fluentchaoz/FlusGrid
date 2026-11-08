execute if predicate flusgrid_end:protected_center run return 0
execute unless loaded ~ ~ ~ run return run tellraw @a {text:"FlusGrid End: target chunk is not loaded. Move closer and retry.",color:"red"}
execute unless loaded ~15 ~15 ~15 run return 0
$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "started"
function flusgrid_end:internal/preserve_leaves
function flusgrid_end:internal/carve
scoreboard players set #uncleared flusgrid 0
function flusgrid_end:internal/verify
$execute unless score #uncleared flusgrid matches 0 run data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "failed"
execute unless score #uncleared flusgrid matches 0 run return run tellraw @a {text:"FlusGrid End: verification FAILED. Region is locked; restore your disposable world backup. Do not retry by deleting the ledger.",color:"red"}
$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "complete"
$execute unless score #quiet flusgrid matches 1 run tellraw @a {text:"FlusGrid End: converted cube at $(x), $(y), $(z). Four-block spacing; 64 grid positions retained. Later physics can change blocks.",color:"green"}
