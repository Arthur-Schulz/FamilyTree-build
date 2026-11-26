"""Relocalisations : recalcule la liste D.moves de la page Carte d'après la règle (claude/generateur-relocalisations.md), avec un rayon de tolérance.
Règle : mort à plus de 100 km de la naissance ; au moins un ascendant a un événement (naissance ou décès) à moins de RAD km du lieu de naissance ;
au moins un descendant a un événement à moins de RAD km du lieu de décès (exception Jenny von Rosenbach : 50 km côté descendants). Lieux « ? » exclus.
RAD = 10 km par défaut (variable MOVES_RADIUS). Les groupes existants (couples, liens parent-enfant, dates y1/y2 données par Arthur) sont conservés ;
leurs chiffres sont recalculés. Une personne éligible absente de la page devient une nouvelle entrée, SANS DATE (y1/y2 = null : absente de la frise).
usage : BUNDLE=… python3 -I src/rebuild_moves.py out/carte.html"""
import sys,os,json,math,collections,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from model import P,U
# dates de relocalisation (frise), données par Arthur pour les entrées nouvelles : id -> (année début, année fin)
MOVE_DATES={'jean-francois-cranney-1708':(1725,1730),'joseph-bonhomme':(1920,1925)}   # monté à Paris peu avant son mariage du 20/05/1731 (Saint-Sulpice) — 25/11/2026
RAD=float(os.environ.get('MOVES_RADIUS','10')); EXC={'jenny-therese-von-rosenbach':50}
IDX={'pierre-schulz':1,'jean-denis-1894':2,'marie-therese-jordan':3,'claude-hachette':4,'georges-masson':5,'roger-rene-le-franc':6,'marie-therese-jacquey-de-baralle':7}
def hv(a,b):
    R=6371.0088; p1,p2=math.radians(a['lat']),math.radians(b['lat']); dl=math.radians(b['lon']-a['lon']); dp=p2-p1
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(x))
def closure(i,f):
    seen=set(); st=list(f(i))
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x); st+=f(x)
    return seen
def yr(s): m=re.search(r'(\d{4})',s or ''); return m[1] if m else ''
def fmt(t,n,m): return f'{t} (°{n} / †{m})'
def rel_word(d,sex):
    f=(sex=='F')
    if d==0: return 'elle-même' if f else 'lui-même'
    if d<0:
        n=-d; base='fille' if f else 'fils'
        return base if n==1 else ('petite-fille' if f else 'petit-fils') if n==2 else (('arr.-'*(n-2))+('petite-fille' if f else 'petit-fils'))
    gp='mère' if f else 'père'; ggp='grand-mère' if f else 'grand-père'
    if d==1: return gp
    if d==2: return ggp
    k=d-2
    return ('arr.-'*k if k<=3 else f'arr.×{k}-')+ggp
def depths(x):
    res={x:0}; fr=[x]
    while fr:
        n=fr.pop(0)
        for p in P.get(n,{}).get('parents',[]):
            if p in P and p not in res: res[p]=res[n]+1; fr.append(p)
    return res
def relation(pid,brs,BN):
    out=[]
    for b in brs:
        e=[k for k,v in IDX.items() if v==b][0]
        if pid in depths(e): out.append((b,rel_word(depths(e)[pid],P[pid].get('sex'))))
        elif e in depths(pid): out.append((b,rel_word(-depths(pid)[e],P[pid].get('sex'))))
    if len(out)==1 and out[0][1] in('lui-même','elle-même'): return 'éponyme de sa branche'
    ws={w for _,w in out}; nm=lambda b:BN[b]
    if not out: return ''
    if len(ws)==1: return out[0][1]+' de '+' et de '.join(nm(b) for b,_ in out)
    return ' / '.join(w+' de '+nm(b) for b,w in out)
def zoom(pa,pb):
    inFR=lambda q:41<=q['lat']<=51.5 and -5.5<=q['lon']<=9.8
    inEU=lambda q:34<=q['lat']<=71 and -25<=q['lon']<=45
    return 0 if inFR(pa) and inFR(pb) else 1 if inEU(pa) and inEU(pb) else 2
def main(path):
    s=open(path,encoding='utf-8').read(); i0=s.index('const D={"W"')+8; D,e=json.JSONDecoder().raw_decode(s[i0:])
    pl=D['places']; ev=collections.defaultdict(dict)
    for x in D['events']: ev[x['i']][x['t']]=x['p']
    kids=collections.defaultdict(list)
    for i,p in P.items():
        for q in p.get('parents',[]): kids[q].append(i)
    up=lambda x:[q for q in P[x].get('parents',[]) if q in P]; pls=lambda x:[ev[x].get('b'),ev[x].get('d')]
    near=lambda S,ref,R:[[r is not None and hv(pl[r],pl[ref])<R for r in pls(x)] for x in S]
    rows={}
    for i,p in P.items():
        if 'b' not in ev[i] or 'd' not in ev[i]: continue
        if p.get('birthPlace','').strip().endswith('?') or p.get('deathPlace','').strip().endswith('?'): continue
        pb,pd=ev[i]['b'],ev[i]['d']; km=hv(pl[pb],pl[pd])
        if km<=100: continue
        asc=closure(i,up); desc=closure(i,lambda x:kids[x]); rd=EXC.get(i,RAD)
        A=near(asc,pb,RAD); Dd=near(desc,pd,rd)
        if not any(any(a) for a in A) or not any(any(a) for a in Dd): continue
        rows[i]=dict(id=i,n=(p['first']+' '+p['birthName']).strip(),rel='',by=yr(p['birth']),bp=pl[pb]['name'],dy=yr(p['death']),dp=pl[pd]['name'],km=round(km),
            a=fmt(sum(any(a) for a in A),sum(a[0] for a in A),sum(a[1] for a in A)),ds=fmt(sum(any(a) for a in Dd),sum(a[0] for a in Dd),sum(a[1] for a in Dd)),dr=int(rd) if rd==int(rd) else rd,_b=pb,_d=pd)
    B3={b['id']:b for b in D['branches'] if str(b['g'])=='3'}
    BN={1:'Pierre Schulz',2:'Jean Denis',3:'Marie-Thérèse Jordan',4:'Claude Hachette',5:'Georges Masson',6:'Roger Le Franc',7:'Marie-Thérèse Jacquey de Baralle'}
    brs=lambda x:[IDX[b] for b in IDX if b in B3 and x in B3[b]['members']]
    out=[]; rep={'conservees':0,'retirees':[],'nouvelles':[]}; used=set()
    for g in D['moves']:
        ids=[p['id'] for p in g['p'] if p['id'] in rows]
        for p in g['p']:
            if p['id'] not in rows: rep['retirees'].append(p['id'])
        if not ids: continue
        ng=dict(g); old={p['id']:p for p in g['p']}; ng['p']=[]
        for x in ids:
            r=dict(rows[x]); r['rel']=old[x]['rel']; r.pop('_b'); r.pop('_d'); ng['p'].append(r); used.add(x)
        ng['mv']=[]
        for m in g['mv']:
            m=dict(m); m['ids']=[x for x in m['ids'] if x in rows]
            if not m['ids']: continue
            r=rows[m['ids'][0]]; m.update(f=r['bp'],t=r['dp'],fi=r['_b'],ti=r['_d'])
            if m.get('y1') is None and m['ids'][0] in MOVE_DATES: m['y1'],m['y2']=MOVE_DATES[m['ids'][0]]
            ng['mv'].append(m)
        out.append(ng); rep['conservees']+=1
    for x,r in sorted(rows.items(),key=lambda t:(int(t[1]['dy'] or 9999),t[0])):
        if x in used: continue
        bi=brs(x) or []; k=len(out)+1; r=dict(r); fi,ti=r.pop('_b'),r.pop('_d'); r['rel']=relation(x,bi,BN) if bi else ''
        out.append({'k':k,'lv':zoom(pl[fi],pl[ti]),'bi':bi,'n':r['n'],'mv':[{'l':str(k),'y1':MOVE_DATES.get(x,(None,None))[0],'y2':MOVE_DATES.get(x,(None,None))[1],'b':bi,'n':r['n'],'f':r['bp'],'t':r['dp'],'fi':fi,'ti':ti,'ids':[x]}],'p':[r]})
        rep['nouvelles'].append((x,r['n'],r['bp'],r['dp'],r['km'],bi))
    # ordre chronologique de la séquence (flèches « Événement précédent / suivant ») : date de début la plus ancienne, sans date en dernier ; tri stable
    out.sort(key=lambda g:min((m['y1'] if m['y1'] is not None else 99999) for m in g['mv']))
    for i,g in enumerate(out,1):
        g['k']=i
        for j,m in enumerate(g['mv']): m['l']=str(i)+('abcd'[j] if len(g['mv'])>1 else '')
    D['moves']=out
    t=s[:i0]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+s[i0+e:]
    a='avec au moins un ascendant né ou mort dans leur commune de naissance et au moins un descendant né ou mort dans leur commune de décès.'
    b='avec au moins un ascendant né ou mort à moins de %d km de leur lieu de naissance et au moins un descendant né ou mort à moins de %d km de leur lieu de décès.'%(RAD,RAD)
    if a in t: t=t.replace(a,b)
    else: assert b in t,'phrase de la règle introuvable dans la page'
    open(path,'w',encoding='utf-8').write(t)
    print('relocalisations',len(rows),'personnes ;',len(out),'entrées ;',rep)
if __name__=='__main__': main(sys.argv[1])
