execute unless data storage flusgrid:job pending[0] run return run function flusgrid:area/finish
data modify storage flusgrid:work origin set from storage flusgrid:job pending[0]
function flusgrid:area/process with storage flusgrid:work origin
