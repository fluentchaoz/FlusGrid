execute if data storage flusgrid:realm {state:"ready",live:1b,model:10000} run function flusgrid:realm/players10
execute if data storage flusgrid:realm {state:"ready",live:1b} unless data storage flusgrid:realm {model:10000} run function flusgrid:realm/tick_legacy_players
execute if data storage flusgrid:realm {manual_pause:1b} run return 0
execute if data storage flusgrid:realm {state:"preparing",model:10000,phase:"overworld"} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/complete_overworld
execute if data storage flusgrid:realm {state:"preparing",model:10000,phase:"nether"} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/complete_nether
execute if data storage flusgrid:realm {state:"preparing",model:10000,phase:"end"} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/complete_end
execute if data storage flusgrid:realm {state:"preparing",phase:"overworld"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/legacy_complete_overworld
execute if data storage flusgrid:realm {state:"preparing",phase:"nether"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/legacy_complete_nether
execute if data storage flusgrid:realm {state:"preparing",phase:"end"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/legacy_complete_end
execute if data storage flusgrid:realm {state:"ready",model:10000,owner:"overworld"} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/tile_complete_overworld
execute if data storage flusgrid:realm {state:"ready",model:10000,owner:"nether"} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/tile_complete_nether
execute if data storage flusgrid:realm {state:"ready",model:10000,owner:"end"} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/tile_complete_end
execute if data storage flusgrid:realm {state:"ready",owner:"overworld"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/commit_overworld
execute if data storage flusgrid:realm {state:"ready",owner:"nether"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/commit_nether
execute if data storage flusgrid:realm {state:"ready",owner:"end"} unless data storage flusgrid:realm {model:10000} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/commit_end
execute if data storage flusgrid:realm {state:"ready",live:1b,model:10000} unless data storage flusgrid:realm owner if data storage flusgrid:realm queue[0] run function flusgrid:realm/tile_start with storage flusgrid:realm queue[0]
