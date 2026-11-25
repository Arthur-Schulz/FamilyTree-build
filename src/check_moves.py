"""Contrôle des relocalisations (règle de claude/generateur-relocalisations.md, stats2.py) sur la page Carte régénérée.
usage : BUNDLE=work/bundle1.json python3 -I src/check_moves.py out/carte.html"""
import sys,os,json,math,collections,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from model import P
s=open(sys.argv[1],encoding='utf-8').read(); D=json.JSONDecoder().raw_decode(s[s.index('const D={"W"')+8:])[0]
pl=D['places']
ev=collections.defaultdict(dict)
for e in D['events']: ev[e['i']][e['t']]=e['p']
def hv(a,b):
    R=6371.0088; p1,p2=math.radians(a['lat']),math.radians(b['lat']); dl=math.radians(b['lon']-a['lon']); dp=p2-p1
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(x))
kids=collections.defaultdict(list)
for i,p in P.items():
    for q in p.get('parents',[]): kids[q].append(i)
def closure(i,f):
    seen=set(); st=list(f(i))
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x); st+=f(x)
    return seen
up=lambda x:[q for q in P[x].get('parents',[]) if q in P]
pls=lambda x:[ev[x].get('b'),ev[x].get('d')]
EXC={'jenny-therese-von-rosenbach':50}
rows=[]
for i,p in P.items():
    if 'b' not in ev[i] or 'd' not in ev[i]: continue
    if p.get('birthPlace','').strip().endswith('?') or p.get('deathPlace','').strip().endswith('?'): continue
    pb,pd=ev[i]['b'],ev[i]['d']; km=hv(pl[pb],pl[pd])
    if km<=100: continue
    asc=closure(i,up); desc=closure(i,lambda x:kids[x])
    if not any(pb in pls(x) for x in asc): continue
    rad=EXC.get(i,0)
    if rad:
        if not any(r is not None and hv(pl[r],pl[pd])<rad for x in desc for r in pls(x)): continue
    elif not any(pd in pls(x) for x in desc): continue
    rows.append((i,pl[pb]['name'],pl[pd]['name'],round(km)))
cur={p['id'] for m in D['moves'] for p in m['p']}
new={r[0] for r in rows}
print('relocalisations éligibles',len(new),'dans la page',len(cur))
print('nouvelles :',[r for r in rows if r[0] not in cur]); print('disparues :',sorted(cur-new))
