"""Audit a stopped test world's completed pregen ledger (requires nbtlib).
Usage: python tests/audit_pregen_save.py /path/to/world [flusgrid|flusgrid_nether|flusgrid_end]
"""
from pathlib import Path
import sys
import nbtlib

world=Path(sys.argv[1])
namespace=sys.argv[2] if len(sys.argv)>2 else "flusgrid"
assert namespace in ("flusgrid","flusgrid_nether","flusgrid_end")
low,high=(-64,320) if namespace=="flusgrid" else (0,256)
sections=(high-low)//16
root=nbtlib.load(world/'data'/namespace/'command_storage.dat').unpack()
contents=root['data']['contents']
job=contents['job']; regions=contents['ledger']['regions']
assert job['kind']=='pregen' and job['state']=='complete',job
target=job.get('chunk_total',1024)
assert job['done']==target*sections and job['chunks']==target and job['percent']==100,job
assert 'ticket' not in job,'Pregen retained a force-load ticket'
expected={f'{x},{y},{z}' for x in range(job['min_x'],job['max_x']+1,16)
          for z in range(job['min_z'],job['max_z']+1,16) for y in range(low,high,16)}
assert len(expected)==target*sections
def wanted(k):
 x,y,z=map(int,k.split(','))
 return 'protected' if namespace=='flusgrid_end' and -256<=x<256 and -256<=z<256 else 'complete'
bad=[k for k in expected if regions.get(k)!=wanted(k)]
assert not bad, f'{len(bad)} missing/incomplete entries: {bad[:10]}'
print(f'PASS: all {len(expected)} distinct cubes correctly accounted for; {target} chunks; no owned ticket remains.')
print(f'Bounds: X {job["min_x"]}..{job["max_x"]+15}, Z {job["min_z"]}..{job["max_z"]+15}, Y {low}..{high-1}')
