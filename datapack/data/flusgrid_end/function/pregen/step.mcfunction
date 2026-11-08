execute store result score #eminx flusgrid run data get storage flusgrid_end:job min_x
execute store result score #emaxx flusgrid run data get storage flusgrid_end:job max_x
execute store result score #eminz flusgrid run data get storage flusgrid_end:job min_z
execute store result score #emaxz flusgrid run data get storage flusgrid_end:job max_z
execute if score #eminx flusgrid matches ..64 if score #emaxx flusgrid matches -64.. if score #eminz flusgrid matches ..64 if score #emaxz flusgrid matches -64.. unless data storage flusgrid_end:arena {ready:1b} run return run function flusgrid_end:arena/tick
execute store result score #done flusgrid run data get storage flusgrid_end:job done
execute store result score #target flusgrid run data get storage flusgrid_end:job total
execute if score #done flusgrid >= #target flusgrid run return run function flusgrid_end:pregen/finish
execute unless data storage flusgrid_end:job ticket run return run function flusgrid_end:pregen/acquire with storage flusgrid_end:job cursor
function flusgrid_end:pregen/process with storage flusgrid_end:job cursor
