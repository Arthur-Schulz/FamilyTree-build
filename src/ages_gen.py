import sys,json,re,datetime,collections,math,itertools,os
sys.path.insert(0,os.path.dirname(__file__))
from model import P,U,ARTHUR,CONST,VERNAGE
VERN=VERNAGE
def mingen(root):
    best={root:1}; q=collections.deque([root])
    while q:
        x=q.popleft()
        for par in P[x].get('parents',[]):
            if par in P and (par not in best or best[par]>best[x]+1):
                best[par]=best[x]+1; q.append(par)
    return best
GA,GC=mingen(ARTHUR),mingen(CONST)
def parse(txt,qual=''):
    t=(txt or '').strip()
    m=re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{1,4})',t)
    try:
        if m: return datetime.date(int(m[3]),int(m[2]),int(m[1])),True,qual
        m=re.fullmatch(r'(\d{1,2})/(\d{1,4})',t)
        if m: return datetime.date(int(m[2]),int(m[1]),15),False,qual
        m=re.fullmatch(r'(\d{1,4})',t)
        if m: return datetime.date(int(m[1]),7,2),False,qual
    except ValueError: return None
    return None
def pdate(p,k): return parse(p.get(k),p.get(k+'Qual','') or '')
def udate(u):
    t=(u.get('date') or '').strip(); q=''
    m=re.match(r'(vers|avant|apr[eè]s)\s+',t)
    if m: q={'vers':'vers','avant':'avant'}.get(m[1],'apres'); t=t[m.end():]
    r=parse(t,q) if t else None
    return r
def age(d1,d2): return round((d2-d1).days/365.2425,2)
def flags(*ds):
    v=1 if any(d[2]=='vers' for d in ds) else 0
    p='j' if (not v and all(d[1] for d in ds)) else 'a'
    return p,v
def okq(*ds): return all(d is not None and d[2] not in('avant','apres') for d in ds)
def sexof(x): return P[x].get('sex') if P[x].get('sex') in('M','F') else None
def rows_longv(G,b):
    out=[]
    for x,g in G.items():
        p=P[x]; B=pdate(p,'birth'); Dd=pdate(p,'death')
        if not okq(B,Dd) or not sexof(x): continue
        pp,v=flags(B,Dd); out.append(dict(s=p['sex'],y=B[0].year,a=age(B[0],Dd[0]),p=pp,v=v,g=g,b=b,_id=x))
    return out
def couples():
    res=set()
    for x in set(GA)|set(GC):
        ps=[q for q in P[x].get('parents',[]) if q in P]
        if len(ps)==2: res.add(frozenset(ps))
    res.add(frozenset((ARTHUR,CONST)))
    return [(uid,u) for uid,u in U.items() if frozenset((u['a'],u['b'])) in res]
NUN=collections.Counter()
for u in U.values():
    for x in (u['a'],u['b']): NUN[x]+=1
def rows_marr():
    out=[]; skipped=0; tot=0
    for uid,u in couples():
        tot+=1
        d=udate(u)
        if d is None or d[2] in('avant','apres'): skipped+=1; continue
        for x in (u['a'],u['b']):
            b='A' if x in GA else 'C' if x in GC else None
            if not b: continue
            G=GA if b=='A' else GC
            B=pdate(P[x],'birth')
            if not okq(B) or not sexof(x): continue
            pp,v=flags(B,d); out.append(dict(s=P[x]['sex'],y=B[0].year,a=age(B[0],d[0]),p=pp,v=v,r=0 if NUN[x]>1 else 1,g=G[x],b=b,_id=x,_u=uid))
    return out,skipped,tot
def rows_parn():
    out=[]
    for b,G in (('A',GA),('C',GC)):
        for x,g in G.items():
            for q in P[x].get('parents',[]):
                if q not in P or not sexof(q): continue
                Bc=pdate(P[x],'birth'); Bp=pdate(P[q],'birth')
                if not okq(Bc,Bp): continue
                pp,v=flags(Bc,Bp); out.append(dict(s=P[q]['sex'],y=Bp[0].year,a=age(Bp[0],Bc[0]),p=pp,v=v,g=G[q],b=b,_id=q,_c=x))
    return out
def nm(x):
    p=P[x]; n=' '.join(t for t in ((p.get('first') or '').strip(),((p.get('last') or '').strip() or (p.get('birthName') or '').strip())) if t)
    m=re.search(r'(\d{4})',p.get('birth') or '')
    return n+(' ('+m[1]+')' if m else '')
def levels():
    return {lv:[(x,'A') for x,g in GA.items() if g==lv]+[(x,'C') for x,g in GC.items() if g==lv] for lv in (2,3,4)}
def ancself(x):
    seen={x}; st=[x]
    while st:
        for q in P[st.pop()].get('parents',[]):
            if q in P and q not in seen: seen.add(q); st.append(q)
    return seen
def scale(rows):
    ages=[r['a'] for r in rows]; lo=math.floor(min(ages)/5)*5; hi=math.ceil(max(ages)/5)*5
    mc=max(collections.Counter((r['s'],int((r['a']-lo)//5)) for r in rows).values()); pm=0
    for br,vers,ex in itertools.product(['AC','A','C'],[True,False],[True,False]):
        R=[r for r in rows if (br=='AC' or r['b']==br) and (vers or not r['v']) and (not ex or not r.get('x'))]
        n=collections.Counter(r['s'] for r in R); c=collections.Counter((r['s'],int((r['a']-lo)//5)) for r in R)
        for k,v in c.items(): pm=max(pm,100*v/n[k[0]])
    return {'lo':lo,'hi':hi,'mc':mc,'pm':round(pm,2)}

def build(OLD,today):
    """Régénère les données de la page Âges d'après le format actuel (lignes avec l = lignées, m = branches)."""
    B=OLD['branches']; AN=[ancself(b['id']) for b in B]
    lin={}; lid={}
    L=levels()
    for lv in (2,3,4):
        byname={nm(x):x for x,_ in L[lv]}
        ids=[]
        for m in OLD['meta']['lin'][str(lv)]:
            assert m['n'] in byname,(lv,m['n'],sorted(byname)[:5]); ids.append(byname[m['n']])
        assert set(ids)==set(x for x,_ in L[lv]),(lv,set(x for x,_ in L[lv])-set(ids))
        lin[str(lv)]=[{'n':nm(x),'t':('A' if x in GA else 'C')} for x in ids]; lid[lv]=ids
    cover={lv:[ancself(x) for x in lid[lv]] for lv in lid}
    def lineage(x):
        out=[]
        for lv in (2,3,4):
            hits=[i for i,S in enumerate(cover[lv]) if x in S]
            out.append(hits[0] if len(hits)==1 else (-2 if hits else -1))
        return out
    def fin(rows):
        R=[]
        for r in rows:
            r=dict(r); x=r.pop('_id'); r.pop('_u',None); r.pop('_c',None)
            r['l']=lineage(x); r['m']=[i for i,a in enumerate(AN) if x in a]
            R.append(r)
        return R
    lv=fin(rows_longv(GA,'A')+rows_longv(GC,'C'))
    rm,sk,tot=rows_marr(); mr=fin(rm)
    pn=fin(rows_parn())
    return lin,lv,mr,pn,sk,tot,rm
