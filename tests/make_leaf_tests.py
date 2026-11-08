"""Destructive leaf fixture pack for a disposable runtime. Not distributed."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from leaves import LEAVES
p=Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=True)
(p/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'Leaf test fixtures','min_format':[121,0],'max_format':[121,0]}}))
f=p/'data/fg_test/function';f.mkdir(parents=True,exist_ok=True)
setup=['scoreboard objectives add fg_test dummy','scoreboard players set #fail fg_test 0','scoreboard players set #finished fg_test 0']
check=[]
for i,leaf in enumerate(LEAVES):
 x=(i%4)*4;z=(i//4)*4
 setup += [f'setblock {x} 96 {z} minecraft:{leaf}_leaves[persistent=false,distance=7,waterlogged=false] strict']
 check += [f'execute unless block {x} 96 {z} minecraft:{leaf}_leaves[persistent=true,distance=7,waterlogged=false] run scoreboard players add #fail fg_test 1']
setup+=['setblock 0 100 0 minecraft:oak_leaves[persistent=false,distance=3,waterlogged=true] strict','function flusgrid:convert {x:0,y:96,z:0}']
setup+=check+['execute unless block 0 100 0 minecraft:oak_leaves[persistent=true,distance=3,waterlogged=true] run scoreboard players add #fail fg_test 1','setblock 32 96 0 minecraft:oak_leaves[persistent=false,distance=7] strict','scoreboard players set #finished fg_test 1']
(f/'setup.mcfunction').write_text('\n'.join(setup)+'\n')
# Following accelerated random ticks, inspect dry persistent leaf species plus decayed control.
check2=['scoreboard players set #decay_fail fg_test 0']+[s.replace('#fail','#decay_fail') for s in check]+['execute unless block 32 96 0 minecraft:air run scoreboard players add #decay_fail fg_test 1','scoreboard players get #decay_fail fg_test']
(f/'after.mcfunction').write_text('\n'.join(check2)+'\n')
