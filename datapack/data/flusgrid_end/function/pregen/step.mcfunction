execute store result score #done flusgrid run data get storage flusgrid_end:job done
execute store result score #target flusgrid run data get storage flusgrid_end:job total
execute if score #done flusgrid >= #target flusgrid run return run function flusgrid_end:pregen/finish
function flusgrid_end:pregen/step_at with storage flusgrid_end:job cursor
