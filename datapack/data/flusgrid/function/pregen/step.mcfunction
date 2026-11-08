execute store result score #done flusgrid run data get storage flusgrid:job done
execute store result score #target flusgrid run data get storage flusgrid:job total
execute if score #done flusgrid >= #target flusgrid run return run function flusgrid:pregen/finish
execute unless data storage flusgrid:job ticket run return run function flusgrid:pregen/acquire with storage flusgrid:job cursor
function flusgrid:pregen/process with storage flusgrid:job cursor
