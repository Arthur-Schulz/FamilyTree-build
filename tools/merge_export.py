"""Remplace people et unions du bundle (data.enc.js décodé) par ceux d'un export « Sauvegarde » de l'artifact.
usage : python3 -I tools/merge_export.py <export.json> <bundle.json>
Les autres clés du bundle (photos, wiki, wikifam, settings) sont conservées. Le champ `id` de l'export devient la clé."""
import sys, json
exp, bun = sys.argv[1:3]
E = json.load(open(exp, encoding='utf-8')); B = json.load(open(bun, encoding='utf-8'))
assert E.get('format') == 'arbre-genealogique', E.get('format')
def conv(lst): 
    out = {}
    for d in lst:
        d = dict(d); k = d.pop('id'); assert k not in out, k; out[k] = d
    return out
P, U = conv(E['people']), conv(E['unions'])
for k, p in P.items():
    for q in p.get('parents', []): assert q in P, ('parent inconnu', k, q)
for k, u in U.items():
    assert u['a'] in P and u['b'] in P, ('union', k)
B['people'], B['unions'] = P, U
json.dump(B, open(bun, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('people', len(P), 'unions', len(U), 'photos', len(B.get('photos', {})))
