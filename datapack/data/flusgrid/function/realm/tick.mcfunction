execute if data storage flusgrid:realm {state:"ready",live:1b} run function flusgrid:realm/players
execute if data storage flusgrid:realm {manual_pause:1b} run return 0
execute if data storage flusgrid:realm {state:"preparing",phase:"overworld"} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/complete_overworld
execute if data storage flusgrid:realm {state:"preparing",phase:"nether"} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/complete_nether
execute if data storage flusgrid:realm {state:"preparing",phase:"end"} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/complete_end
execute if data storage flusgrid:realm {state:"ready",owner:"overworld"} if data storage flusgrid:job {state:"complete"} run return run function flusgrid:realm/commit_overworld
execute if data storage flusgrid:realm {state:"ready",owner:"nether"} if data storage flusgrid_nether:job {state:"complete"} run return run function flusgrid:realm/commit_nether
execute if data storage flusgrid:realm {state:"ready",owner:"end"} if data storage flusgrid_end:job {state:"complete"} run return run function flusgrid:realm/commit_end
