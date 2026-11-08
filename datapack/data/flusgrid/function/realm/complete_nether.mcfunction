execute unless data storage flusgrid:fixtures nether{ready:1b} in minecraft:the_nether run return run function flusgrid:realm/fixture_tick_nether
data modify storage flusgrid:realm bounds.nether set from storage flusgrid:realm start_bounds
execute in minecraft:the_nether run function flusgrid:realm/platform_nether
execute in minecraft:the_nether run function flusgrid:realm/fixture_release_nether
data merge storage flusgrid:realm {phase:"end",owner:"end"}
function flusgrid:realm/initial_start_end
