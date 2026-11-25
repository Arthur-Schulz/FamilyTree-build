"""Carte : régénère les données D de pages/carte.html (événements, lieux, non-localisés, branches) d'après le snapshot.
usage : BUNDLE=work/bundle1.json BUNDLE_REF=work/bundle0.json python3 -I src/rebuild_carte.py pages/carte.html out/carte.html
BUNDLE_REF = snapshot proche de la page d'origine, pour retrouver la correspondance « libellé de lieu -> lieu de la carte »."""
import sys,os,re,json,collections,datetime,copy
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from model import P,U,ARTHUR,CONST,VERNAGE
REF=json.load(open(os.environ.get('BUNDLE_REF','work/bundle0.json'),encoding='utf-8'))['people']
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
i0=s.index('const D={"W"')+8
D,e=json.JSONDecoder().raw_decode(s[i0:])
TODAY=datetime.date.today().isoformat()
def yr(t):
    m=re.search(r'(?<!\d)(\d{3,4})(?!\d)',t or ''); return int(m.group(1)) if m else None
def nm(p): return (p['first']+' '+p['birthName']).strip()
def life(p):
    b=yr(p['birth']); d=yr(p['death']); return (str(b) if b else '?')+'–'+(str(d) if d else '')
def weights(root):
    u=collections.defaultdict(float); h=collections.defaultdict(float)
    st=[(root,0)]
    while st:
        x,g=st.pop(); u[x]+=0.5**g; h[x]+=0.5**(g/2)
        for par in P[x].get('parents',[]): st.append((par,g+1))
    return u,h
WA=weights(ARTHUR); WC=weights(CONST)
assert not (set(WA[0])&set(WC[0]))
places=copy.deepcopy(D['places'])
byname={p['name']:k for k,p in enumerate(places)}
# --- correspondance libellé -> lieu (d'après l'ancienne page et le snapshot de référence)
rawmap={}; oldev={}; rawnote={}
for ev in D['events']:
    rp=REF[ev['i']]; raw=(rp['birthPlace'] if ev['t']=='b' else rp['deathPlace']).strip()
    rawmap[raw]=ev['p']; oldev[(ev['i'],ev['t'])]=(ev,raw)
    if ev.get('a') or ev.get('q'): rawnote.setdefault(raw,(ev.get('a'),ev.get('q')))
def newplace(name,lat,lon,src_,loc):
    places.append({'k':name,'name':name,'lat':lat,'lon':lon,'x':None,'y':None,'src':src_,'loc':loc}); byname[name]=len(places)-1; return len(places)-1
# lieux ajoutés le 25/11/2026 (Bungener) : coordonnées GeoNames (Calvisson, Saint-Jean-du-Bruel, Saint-Sulpice NE) ou Wikipédia (les autres)
NEWP={
 'Calvisson':(43.787,4.1963,'Calvisson (GeoNames)','30'),
 'Saint-Jean-du-Bruel':(44.0227,3.3601,'Saint-Jean-du-Bruel (GeoNames)','12'),
 'Saint-Sulpice (Neuchâtel)':(46.9111,6.5622,'Saint-Sulpice (GeoNames)','Suisse'),
 'Cologny':(46.2158,6.1811,'Cologny (Wikipédia)','Suisse'),
 'Renan':(47.133,6.933,'Renan (Wikipédia)','Suisse'),
 'Le Pont-de-Montvert':(44.3642,3.7444,'Le Pont-de-Montvert (Wikipédia)','48'),
 'Nancray-sur-Rimarde':(48.069,2.334,'Nancray-sur-Rimarde (Wikipédia)','45'),
 # ajoutés le 25/11/2026 (planches Cranney / Franceschi-Fleury)
 'Besançon':(47.2488,6.0182,'Besançon (GeoNames)','25'),
 'Bourbonne-les-Bains':(47.953,5.748,'Bourbonne-les-Bains (GeoNames)','52'),
 'Voujeaucourt':(47.4751,6.7743,'Voujeaucourt (GeoNames)','25'),
 'Corsagna':(43.9775,10.5639,'Corsagna (GeoNames)','Italie'),
 'Mersuay':(47.782,6.139,'Mersuay (cartesfrance.fr ; Wikipédia 47°47′N 6°08′E)','70'),
 'Auxon':(47.6828,6.1658,'Auxon, Haute-Saône (Wikipédia)','70'),
 # ajoutés le 25/11/2026 (demande d'Arthur : localiser systématiquement les lieux manquants)
 'Le Crozet':(46.1706,3.8550,'Le Crozet, Loire (Wikipédia 46°10′17″N 3°51′20″E)','42'),
}
# libellé brut -> (nom du lieu, note ou None)
NEWM={
 "Calvisson (Languedoc, aujourd'hui Gard)":('Calvisson',None),
 'Cologny (Genève, Suisse)':('Cologny',None),
 'Genève (Suisse), Grand Rue de la Boucherie':('Genève','adresse non distinguée : placé sur Genève'),
 'Genève (Suisse), rue Basse de la Fusterie':('Genève','adresse non distinguée : placé sur Genève'),
 'Genève (Suisse), rue de la Boulangerie':('Genève','adresse non distinguée : placé sur Genève'),
 'Hôtel Saint-Maury, près de Pons (Charente-Maritime)':('Pons','lieu-dit « près de Pons » placé sur Pons'),
 'La Graveline, Eaux-Vives (Genève, Suisse)':('Genève','lieu-dit des Eaux-Vives (Genève) placé sur Genève'),
 'Nancray, près de Pithiviers (Gâtinais)':('Nancray-sur-Rimarde','« Nancray, près de Pithiviers » identifié à Nancray-sur-Rimarde (Loiret), à 13 km de Pithiviers : identification non confirmée'),
 'Nîmes (Gard)':('Nîmes',None),
 'Paris (16e), 57 rue Boissière':('Paris','arrondissement non distingué : placé sur Paris'),
 'Paris (17e), 5 rue Viète':('Paris','arrondissement non distingué : placé sur Paris'),
 'Pont-de-Montvert':('Le Pont-de-Montvert',None),
 'Renan':('Renan',None),
 'Besançon':('Besançon',None),
 'Bourbonne-les-Bains':('Bourbonne-les-Bains',None),
 'Voujeaucourt (Doubs)':('Voujeaucourt',None),
 'Corsagna (Italie)':('Corsagna',None),
 'Mersuay':('Mersuay',None),
 'Le Crozet (Loire)':('Le Crozet',None),
 'Mersuay (70)':('Mersuay',None),
 'Auxon (70)':('Auxon',None),
 'Auxon les Vesoul':('Auxon','« Auxon-lès-Vesoul » identifié à Auxon (Haute-Saône)'),
 'La Villette':('Paris','« La Villette » (ancienne commune de la Seine, rattachée à Paris en 1860) : identification non confirmée ; placé sur Paris'),
 'Paris 5e':('Paris','arrondissement non distingué : placé sur Paris'),
 'Paris 7e':('Paris','arrondissement non distingué : placé sur Paris'),
 'Paris 9e':('Paris','arrondissement non distingué : placé sur Paris'),
 'Paris 10e':('Paris','arrondissement non distingué : placé sur Paris'),
 'Paris 17e':('Paris','arrondissement non distingué : placé sur Paris'),
 "St-Jean-du-Bruel (Rouergue, aujourd'hui Aveyron)":('Saint-Jean-du-Bruel',None),
 'St-Sulpice (Neuchâtel, Suisse)':('Saint-Sulpice (Neuchâtel)',None),
}
UNP={'Reclus (42)':('Reclus (42)','lieu non identifié (commune non précisée)',True),
 'Vanel':('Vanel','lieu non identifié (sans département)',True),
 'Picardie':('Picardie','région, pas un lieu précis',True)}
oldun={u['label']:u for u in D['unplaced']}
for lab,(l,why,eu) in UNP.items():
    if lab in oldun: assert oldun[lab]['reason']==why,(lab,oldun[lab]['reason'])
# --- ordre des personnes : ordre de l'ancienne page, puis les nouvelles
order=[]; seen=set()
for ev in D['events']:
    if ev['i'] not in seen: seen.add(ev['i']); order.append(ev['i'])
for u in D['unplaced']:
    for x in u['ids']:
        if x not in seen: seen.add(x); order.append(x)
for who,W in (('a',WA),('c',WC)):
    for x in sorted(W[0]):
        if x not in seen: seen.add(x); order.append(x)
rep=collections.defaultdict(list); events=[]; unplaced=collections.OrderedDict()
def fmt(x): return float(f'{x:.6g}')
for x in order:
    w='a' if x in WA[0] else ('c' if x in WC[0] else None)
    if w is None: rep['hors_ascendance'].append(x); continue
    p=P[x]; U_,H_=(WA if w=='a' else WC); evs=[]
    for t,f,df in (('b','birthPlace','birth'),('d','deathPlace','death')):
        raw=p[f].strip()
        if not raw: continue
        o=oldev.get((x,t)); keep=o and o[1]==raw
        a=q=None
        if keep: pi=o[0]['p']; a=o[0].get('a'); q=o[0].get('q')
        elif raw in rawmap: pi=rawmap[raw]; a,q=rawnote.get(raw,(None,None))
        elif raw in NEWM:
            name,a=NEWM[raw]
            if name in byname: pi=byname[name]
            else: la,lo,sr,loc=NEWP[name]; pi=newplace(name,la,lo,sr,loc)
        elif raw in UNP:
            lab,why,eu=UNP[raw]; u=unplaced.setdefault(lab,{'label':lab,'reason':why,'eu':eu,'n':[],'ids':[],'w':[]})
            u['n'].append(nm(p)); u['ids'].append(x); u['w'].append(w); continue
        else: rep['NON_RESOLU'].append((x,t,raw)); continue
        if o and not keep: rep['lieu_modifie'].append((x,t,D['places'][o[0]['p']]['name'],raw,places[pi]['name']))
        ev={'p':pi,'i':x,'t':t,'y':yr(p[df]),'n':(o[0]['n'] if o else nm(p)),'v':life(p)}
        if (('l' in o[0]) if keep else (not (w=='a' and raw==places[pi]['name']))): ev['l']=raw
        if a: ev['a']=a
        if q: ev['q']=q
        ev.update({'w':w,'u':fmt(U_[x]),'h':fmt(H_[x])}); evs.append(ev)
    for ev in evs: ev['k']=len(evs)
    events+=evs
# --- branches : mêmes racines, membres recalculés (ascendance sans limite, Vernage incluse)
branches=[]
for b in D['branches']:
    assert b['id'] in P
    mem=sorted(weights(b['id'])[0].keys())
    if set(b['members'])-set(mem): rep['membres_perdus'].append((b['id'],sorted(set(b['members'])-set(mem))[:5]))
    nb=dict(b); nb['v']=life(P[b['id']]); nb['members']=mem; branches.append(nb)
    if len(mem)!=len(b['members']): rep['branche_taille'].append((b['id'],len(b['members']),len(mem)))
N=dict(D)
N['places']=places; N['events']=events; N['unplaced']=list(unplaced.values()); N['branches']=branches
N['persons']=len(WA[0])-1; N['nC']=len(WC[0])-1; N['gen']={'a':TODAY,'c':TODAY}
out=s[:i0]+json.dumps(N,ensure_ascii=False,separators=(',',':'))+s[i0+e:]
os.makedirs(os.path.dirname(dst) or '.',exist_ok=True); open(dst,'w',encoding='utf-8').write(out)
print('events',len(D['events']),'->',len(events),'| lieux',len(D['places']),'->',len(places),'| non localisés',[ (u['label'],len(u['n'])) for u in N['unplaced']])
print({k:len(v) for k,v in rep.items()}); print('NR',rep.get('NON_RESOLU'))
json.dump(dict(rep),open(dst+'.rapport.json','w'),ensure_ascii=False,indent=1)
