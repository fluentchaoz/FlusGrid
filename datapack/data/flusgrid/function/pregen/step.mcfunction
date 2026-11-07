execute if data storage flusgrid:job {done:24576} run return run function flusgrid:pregen/finish
execute unless data storage flusgrid:job ticket run return run function flusgrid:pregen/acquire with storage flusgrid:job cursor
function flusgrid:pregen/process with storage flusgrid:job cursor
