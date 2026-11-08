execute store result score #done flusgrid run data get storage flusgrid_nether:job done
execute store result score #target flusgrid run data get storage flusgrid_nether:job total
execute if score #done flusgrid >= #target flusgrid run return run function flusgrid_nether:pregen/finish
execute unless data storage flusgrid_nether:job ticket run return run function flusgrid_nether:pregen/acquire with storage flusgrid_nether:job cursor
function flusgrid_nether:pregen/process with storage flusgrid_nether:job cursor
