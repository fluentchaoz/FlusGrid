data modify storage flusgrid:job state set value "paused"
tellraw @a {text:"FlusGrid paused: next chunk is unloaded. Stay near the area, let terrain load, then /function flusgrid:resume.",color:"yellow"}
