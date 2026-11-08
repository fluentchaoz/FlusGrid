execute unless data storage flusgrid:realm {state:"ready"} run return run function flusgrid:realm_status
data modify storage flusgrid:realm live set value 1b
tellraw @a {text:"FlusGrid automatic expansion and finished-area guard enabled.",color:"green"}
