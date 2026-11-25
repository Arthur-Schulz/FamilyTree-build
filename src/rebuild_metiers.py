"""Régénère la page Métiers (reconstruction du 25/11/2026).
Usage : python3 -I src/rebuild_metiers.py <export.json | bundle.json> <metiers_gabarit.html> <sortie.html> [JJ/MM/AAAA]
Le gabarit fournit le code de la page, les séries, emoji, branches (noms) et profils ; les données sont recalculées."""
import sys, json, re, collections, datetime
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from metiers_gen import *
from canon import canon as CANON
A, C = 'arthur-schulz-robellaz', 'constance-fichet'

def load_people(path):
    j = json.load(open(path, encoding='utf-8'))
    if 'people' in j and isinstance(j['people'], list): return {p['id']: p for p in j['people']}
    return j['people']

def total(vs):
    cc = []
    for b in range(5):
        c = collections.Counter()
        for v in vs:
            for k, n in v['cc'][b].items(): c[k] += n
        cc.append(dict(sorted(c.items(), key=lambda t: int(t[0]))))
    counts = [[R6(sum(v['counts'][b][i] for v in vs)) for i in range(N)] for b in range(5)]
    un = collections.Counter()
    for v in vs:
        for j, n in v['unatt']: un[j] += n
    jf = [collections.defaultdict(list) for _ in range(N)]; uj = collections.defaultdict(list)
    for v in vs:
        for fi in range(N):
            for lab, xs in v['_jf'][fi].items(): jf[fi][lab] += xs
        for lab, xs in v['_uj'].items(): uj[lab] += xs
    return dict(counts=counts, persons=[sum(v['persons'][b] for v in vs) for b in range(5)], known=[sum(v['known'][b] for v in vs) for b in range(5)],
                labels=[R6(sum(r)) for r in counts], beyond={'p': sum(v['beyond']['p'] for v in vs), 'k': sum(v['beyond']['k'] for v in vs)},
                unatt=[[j, n] for j, n in sorted(un.items(), key=lambda t: (-t[1], t[0]))], cc=cc, ny=[sum(v['ny'][b] for v in vs) for b in range(5)],
                _jf=[dict(d) for d in jf], _uj=dict(uj))

def names(P, ids):
    out = {}
    for x in ids:
        p = P[x]; n = ' '.join(t for t in ((p.get('first') or '').strip(), ((p.get('last') or '').strip() or (p.get('birthName') or '').strip())) if t)
        b, d = year(p.get('birth')), year(p.get('death'))
        life = (str(b) + ('–' + str(d) if d else '')) if b else (str(d) if d else '')
        out[x] = [x, n + (' (' + life + ')' if life else ''), b]
    return out

def finish(D, P, views_list):
    """Remplace les listes brutes (_jf/_uj) par des indices dans D['nm'] (tous les ids cités, triés par identifiant)."""
    ids = set()
    for v in views_list:
        for fi in range(N):
            for xs in v['_jf'][fi].values(): ids.update(xs)
        for xs in v['_uj'].values(): ids.update(xs)
    order = sorted(ids); idx = {x: i for i, x in enumerate(order)}
    nmap = names(P, order); D['nm'] = [nmap[x] for x in order]
    for v in views_list:
        v['jf'] = [[[lab, sorted(idx[x] for x in set(xs))] for lab, xs in sorted(v['_jf'][fi].items(), key=lambda t: (-len(set(t[1])), t[0]))] for fi in range(N)]
        v['uj'] = [[lab, sorted(idx[x] for x in set(xs))] for lab, xs in sorted(v['_uj'].items(), key=lambda t: (-len(set(t[1])), t[0]))]
        v.pop('_jf'); v.pop('_uj')

def scope(P, roots):
    s = set()
    for r in roots: s |= set(mingen(P, r))
    return s

def main_D(P, T):
    ga, gc = mingen(P, A), mingen(P, C)
    va, vc = matrix(P, A, 0, None, CANON), matrix(P, C, 0, None, CANON)
    D = dict(T)
    D['views'] = {'a': va, 'c': vc, 'both': total([va, vc])}
    bv = {b['id']: matrix(P, b['id'], b['g'], ga if b['w'] == 'a' else gc, CANON) for b in T['branches']}
    D['bviews'] = bv
    finish(D, P, [va, vc, D['views']['both']] + list(bv.values()))
    for v in [va, vc, D['views']['both']] + list(bv.values()): v.pop('unatt', None) if False else None
    return D

def profile_D(P, T, racines):
    ids = scope(P, racines); shift = min(b['g'] for b in T['branches'] if b['id'] in racines) - 1
    glob = {}
    for r in racines:
        for x, g in mingen(P, r).items(): glob[x] = min(glob.get(x, 99), g + 1)
    br = [dict(b, g=b['g'] - shift, w='a', c=[x for x in (b.get('c') or []) if x in ids]) for b in T['branches'] if b['id'] in ids and b['g'] - shift >= 1]
    bv = {b['id']: matrix(P, b['id'], b['g'], glob, CANON) for b in br}
    both = total([bv[r] for r in racines])
    N_ = {k: T[k] for k in ('date', 'bands', 'series', 'emoji')}
    N_['branches'] = br; N_['bviews'] = bv; N_['views'] = {'a': both, 'c': both, 'both': both}
    # a, c, both partagent le même objet : indices calculés une fois
    finish(N_, P, [both] + list(bv.values()))
    return N_

PROFILS = {'schulz': ['henri-schulz-robellaz', 'corinne-denis'], 'bonhomme': ['jean-claude-bonhomme', 'brigitte-masson'], 'lefranc': ['jean-daniel-le-franc', 'jackie-patry']}

def build(P, template_html, date):
    i = template_html.index('const D=') + len('const D=')
    T, e = json.JSONDecoder().raw_decode(template_html[i:])
    T = dict(T); T['date'] = date
    D = main_D(P, T)
    D['profiles'] = {k: profile_D(P, T, r) for k, r in PROFILS.items()}
    D.pop('profiles_', None)
    # ordre des clés identique à la page d'origine
    keys = ['date', 'bands', 'series', 'emoji', 'branches', 'views', 'bviews', 'nm', 'profiles']
    D = {k: D[k] for k in keys}
    return template_html[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + template_html[i + e:], D

if __name__ == '__main__':
    src, tpl, out = sys.argv[1:4]
    date = sys.argv[4] if len(sys.argv) > 4 else datetime.date.today().strftime('%d/%m/%Y')
    P = load_people(src)
    html, D = build(P, open(tpl, encoding='utf-8').read(), date)
    open(out, 'w', encoding='utf-8').write(html)
    print('ok', out, len(html), 'nm', len(D['nm']))
