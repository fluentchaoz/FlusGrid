function flusgrid:realm_pause
data modify storage flusgrid:realm live set value 0b
tellraw @a {text:"FlusGrid stopped for archival import: no automatic work or travel guard. Ordinary terrain remains beyond finished bounds.",color:"yellow"}
