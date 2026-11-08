execute unless data storage flusgrid:fixtures end{ready:1b} in minecraft:the_end run return run function flusgrid:realm/fixture_tick_end
data modify storage flusgrid:realm bounds.end set value {min_x:-2048,max_x:2047,min_z:-2048,max_z:2047}
execute in minecraft:the_end run function flusgrid:realm/platform_end
execute in minecraft:the_end run function flusgrid:realm/fixture_release_end
data merge storage flusgrid:realm {state:"ready",phase:"complete",live:1b}
data remove storage flusgrid:realm owner
tellraw @a {text:"FlusGrid: all three initial regions complete. Automatic expansion and finished-area guard are on. Back up and inspect before uploading to Realms.",color:"green"}
