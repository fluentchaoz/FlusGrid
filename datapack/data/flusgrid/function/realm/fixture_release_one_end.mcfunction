$forceload remove $(x) $(z)
data remove storage flusgrid:fixtures end.tickets[0]
execute if data storage flusgrid:fixtures end.tickets[0] run function flusgrid:realm/fixture_release_one_end with storage flusgrid:fixtures end.tickets[0]
