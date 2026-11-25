"""Âges : régénère les données de pages/ages.html d'après le snapshot (BUNDLE) ; usage : BUNDLE=work/bundle1.json python3 -I src/rebuild_ages.py pages/ages.html out/ages.html"""
import sys,os,json,re,datetime
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ages_gen as G
from ages_gen import P,U,GA,GC,nm
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
a0=s.index('id="data">')+10; a1=s.index('</script>',a0); OLD=json.loads(s[a0:a1])
lin,lv,mr,pn,sk,tot,rm=G.build(OLD,None)
def full(x):
    p=P[x]; return ' '.join(t for t in ((p.get('first') or '').strip(),((p.get('last') or '').strip() or (p.get('birthName') or '').strip())) if t)
an=[]
for r in sorted(rm,key=lambda r:-r['a']):
    if r['a']<12 or r['a']>60:
        x=r['_id']; u=U[r['_u']]
        an.append(['Âge au mariage atypique (<12 ou >60)',x,full(x),r['a'],'naissance %s (%s) ; union %s [%s]'%(P[x].get('birth'),P[x].get('birthQual') or '',u.get('date'),r['_u'])])
for r in sorted(G.rows_parn(),key=lambda r:-r['a']):
    if r['a']<15 or (r['s']=='F' and r['a']>45):
        x=r['_id']; c=r['_c']
        an.append(['Âge du parent à la naissance atypique (moins de 15 ans, ou mère de plus de 45 ans)',x,full(x),r['a'],'parent né %s (%s) ; enfant %s né %s (%s)'%(P[x].get('birth'),P[x].get('birthQual') or '',full(c),P[c].get('birth'),P[c].get('birthQual') or '')])
# branches : mêmes racines, durées de vie recalculées
def life(x):
    p=P[x]; b=re.search(r'(\d{4})',p.get('birth') or ''); d=re.search(r'(\d{4})',p.get('death') or '')
    return (b[1] if b else '?')+'–'+(d[1] if d else '')
B=[]
for b in OLD['branches']:
    assert b['id'] in P,b['id']
    B.append(dict(b,v=life(b['id'])))
meta={'lin':lin,'nA':len(GA),'nC':len(GC),'maxA':max(GA.values()),'maxC':max(GC.values()),'generated':datetime.date.today().isoformat(),
 'skipped':{'union sans date exploitable':sk},'total_people':len(GA)+len(GC),'total_unions':tot,
 'sc':{'longv':G.scale(lv),'marr':G.scale(mr),'parn':G.scale(pn)},'exN':len(G.ancself(G.VERN))}
D={'meta':meta,'branches':B,'longv':lv,'marr':mr,'parn':pn,'anom':an}
# ordre des clés d'origine
assert list(OLD.keys())==list(D.keys()),(list(OLD.keys()),list(D.keys()))
out=s[:a0]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+s[a1:]
os.makedirs(os.path.dirname(dst) or '.',exist_ok=True)
open(dst,'w',encoding='utf-8').write(out)
print({k:v for k,v in meta.items() if k not in('lin','sc')}); print('rows',len(lv),len(mr),len(pn),'anom',len(an),'(avant',len(OLD['anom']),')')
