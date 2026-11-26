"""Contrôle de fuite sur un site chiffré construit : déchiffre chaque dossier de périmètre avec sa clé de lien et vérifie
 (1) qu'aucun identifiant de personne hors périmètre n'apparaît (« "id" » entre guillemets) dans aucun fichier,
 (2) qu'aucune mention du propriétaire ni de sa conjointe (libellés, prénoms isolés, identifiants) n'apparaît,
 (3) que la racine ne s'ouvre qu'avec le mot de passe, et que les dossiers ne s'ouvrent pas avec le mot de passe de la racine.
usage : PW_PROCHES=… LIEN_SCHULZ=… LIEN_BONHOMME=… LIEN_LEFRANC=… python3 -I tools/test_fuites.py <site> <dossier de travail>"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_profiles as bp
site, W = sys.argv[1:3]
B = json.load(open(W + '/bundle.json', encoding='utf-8')); P = B['people']
profils = bp.load_profils(); per = bp.perimetres(P, profils)
tout = set(P)
ok = True
def ouvrir(d, secret):
    return json.loads(bp.unseal(open(d + '/acces-0.enc', 'rb').read(), secret))
# racine
r = ouvrir(site, os.environ['PW_PROCHES']); assert r['prof']['id'] == 'proches' and r['prof']['ids'] is None
try: ouvrir(site, 'mauvais-mot-de-passe'); print('ECHEC : mauvais mot de passe accepté'); ok = False
except Exception: print('racine : mauvais mot de passe refusé')
for p in profils:
    if p['acces'] != 'lien': continue
    jeton, cle = os.environ[p['env']].split('/')
    d = '%s/%s-%s' % (site, p['dossier'], jeton)
    a = ouvrir(d, cle); M, prof = a['m'], a['prof']
    assert prof['id'] == p['id'] and prof['pre'] and set(prof['ids']) == per[p['id']], 'profil incohérent'
    try: ouvrir(d, os.environ['PW_PROCHES']); print('ECHEC : %s s\'ouvre avec le mot de passe de la racine' % p['id']); ok = False
    except Exception: pass
    try: ouvrir(d, os.environ['LIEN_SCHULZ'].split('/')[1] if p['id'] != 'schulz' else 'x' * 20); print('ECHEC : clé d\'un autre périmètre acceptée'); ok = False
    except Exception: pass
    hors = tout - per[p['id']]
    n_f = 0; res = collections = None
    manque = []
    for f in sorted(os.listdir(d)):
        if not f.endswith('.enc') or f == 'acces-0.enc' or f.startswith('planche-'): continue
        t = bp.unseal(open(d + '/' + f, 'rb').read(), M).decode('utf-8'); n_f += 1
        if f == 'carte.enc':   # liste des lieux réduite aux lieux utilisés, indices valides
            a0 = t.index('const D={"W"') + 8; Dc, _ = json.JSONDecoder().raw_decode(t[a0:])
            u = {e['p'] for e in Dc['events']} | {m[k] for g in Dc['moves'] for m in g['mv'] for k in ('fi', 'ti')}
            assert u == set(range(len(Dc['places']))), 'lieux inutilisés ou indices invalides dans ' + p['id']
            print('%s : %d lieux (tous utilisés)' % (p['id'], len(Dc['places'])))
        ids_vus = set(re.findall(r'"([a-z0-9][a-z0-9.-]*)"', t)) & hors
        if ids_vus: print('ECHEC %s/%s : %d identifiants hors périmètre, ex. %s' % (p['id'], f, len(ids_vus), sorted(ids_vus)[:4])); ok = False
        for rx in bp.INTERDITS:
            for m in re.finditer(rx, t):
                ctx = t[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
                print('MENTION %s/%s [%s] …%s…' % (p['id'], f, rx[:18], ctx)); ok = False
    pl = sorted(f for f in os.listdir(d) if f.startswith('planche-'))
    print('%s : %d fichiers contrôlés, %d planches, pages=%s, jordan=%s' % (p['id'], n_f, len(pl), prof['pages'], 'cjordan.enc' in os.listdir(d)))
    assert ('cjordan.enc' in os.listdir(d)) == ('cjordan' in p['pages']) and bool(pl) == ('cjordan' in p['pages'])
    assert 'contact-form.html' not in os.listdir(d)
print('RESULTAT', 'OK' if ok else 'ECHEC'); sys.exit(0 if ok else 1)
