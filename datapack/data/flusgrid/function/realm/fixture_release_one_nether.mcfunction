$forceload remove $(x) $(z)
data remove storage flusgrid:fixtures nether.tickets[0]
execute if data storage flusgrid:fixtures nether.tickets[0] run function flusgrid:realm/fixture_release_one_nether with storage flusgrid:fixtures nether.tickets[0]
