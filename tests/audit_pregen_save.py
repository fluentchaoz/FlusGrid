"""Audit a stopped test world's completed pregen ledger (requires nbtlib).
Usage: python tests/audit_pregen_save.py /path/to/world
"""
from pathlib import Path
import sys
import nbtlib

world=Path(sys.argv[1])
root=nbtlib.load(world/'data'/'flusgrid'/'command_storage.dat').unpack()
contents=root['data']['contents']
job=contents['job']; regions=contents['ledger']['regions']
assert job['kind']=='pregen' and job['state']=='complete',job
assert job['done']==24576 and job['chunks']==1024 and job['percent']==100,job
assert 'ticket' not in job,'Pregen retained a force-load ticket'
expected={f'{x},{y},{z}' for x in range(job['min_x'],job['max_x']+1,16)
          for z in range(job['min_z'],job['max_z']+1,16) for y in range(-64,320,16)}
assert len(expected)==24576
bad=[k for k in expected if regions.get(k)!='complete']
assert not bad, f'{len(bad)} missing/incomplete entries: {bad[:10]}'
print(f'PASS: all {len(expected)} distinct cubes complete; 1024 chunks; no owned ticket remains.')
print(f'Bounds: X {job["min_x"]}..{job["max_x"]+15}, Z {job["min_z"]}..{job["max_z"]+15}, Y -64..319')
