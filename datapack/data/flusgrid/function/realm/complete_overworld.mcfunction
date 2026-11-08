execute unless data storage flusgrid:fixtures overworld{ready:1b} in minecraft:overworld run return run function flusgrid:realm/fixture_tick_overworld
data modify storage flusgrid:realm bounds.overworld set from storage flusgrid:realm start_bounds
execute in minecraft:overworld run function flusgrid:realm/platform_overworld
execute in minecraft:overworld run function flusgrid:realm/portal
execute in minecraft:overworld run function flusgrid:realm/fixture_release_overworld
data merge storage flusgrid:realm {phase:"nether",owner:"nether"}
function flusgrid:realm/initial_start_nether
