$forceload remove $(x) $(z)
data remove storage flusgrid_end:arena tickets[0]
execute if data storage flusgrid_end:arena tickets[0] run function flusgrid_end:arena/release_one with storage flusgrid_end:arena tickets[0]
