"""Site par périmètres (profils) : construction du site chiffré et du jeu d'identifiants de la version locale.

Reconstruit le 26/11/2026 d'après claude/profils-mot-de-passe.md (le script d'origine avait été perdu).

Modes
  enc <dossier de travail> <sortie>   Site chiffré à publier : racine « proches » (mot de passe) + un dossier par périmètre (lien à clé).
  local-profils <dossier de travail>  Réécrit <travail>/zip/profils.js : listes d'identifiants recalculées d'après les données courantes.
  check <dossier de travail>          Calcule et contrôle les périmètres (disjonction, inclusion des anciens), sans rien écrire.

<dossier de travail> = celui de build.sh : bundle.json, out/*.html (pages recalculées), pages/*.html (autres pages du zip),
zip/ (planche-N.enc.js, profils.js). Il contient des données en clair : hors dépôt.

Secrets : PW_PROCHES (jamais enregistré) ; LIEN_SCHULZ, LIEN_BONHOMME, LIEN_LEFRANC = "<jeton12>/<clé20>" (sinon repris de liens.enc, scellé par PW_PROCHES ; sinon tirés au hasard). PERSIST_LIENS=1 écrit liens.enc.
Absents : liens tirés au hasard et affichés une seule fois ; mot de passe absent = erreur (sauf option --test : tiré au hasard).

Chiffrement : PBKDF2-SHA256 600 000 itérations, AES-256-GCM, gzip ; fichier = sel (16) + iv (12) + chiffré. Clé maître M aléatoire par dossier ;
tous les fichiers de contenu d'un dossier partagent le sel (clé dérivée une fois par le navigateur) avec un iv propre. acces-0.enc = {m, prof}
scellé avec le mot de passe (racine) ou la clé du lien (dossiers)."""
import sys, os, re, json, gzip, hashlib, secrets, subprocess, base64, collections, shutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, 'src'))
from metiers_gen import mingen          # générations minimales (ascendance)

ITER = 600000
TITRE_PROCHES = "L'Arbre d'Arsène et Lazare"
NEUTRE = 'Arbre généalogique'
ALPHA_CLE = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789'
ALPHA_JETON = 'abcdefghijklmnopqrstuvwxyz0123456789'

# ------------------------------------------------------------------ profils
def load_profils():
    return json.load(open(os.path.join(REPO, 'profils.json'), encoding='utf-8'))

def titre(p):
    if p['id'] == 'proches': return TITRE_PROCHES
    a, b = p['nom'].split(' et ', 1)
    return ("Les Ancêtres d'%s et %s" if a[0] in 'AEIOUÉH' else 'Les Ancêtres de %s et %s') % (a, b)

def perimetres(P, profils):
    """ids de chaque profil à racines : union des ascendances des deux racines. Contrôles : racines présentes, périmètres deux à deux disjoints."""
    out = {}
    for p in profils:
        if not p['racines']: continue
        for r in p['racines']: assert r in P, 'racine absente : ' + r
        s = set()
        for r in p['racines']: s |= set(mingen(P, r))
        out[p['id']] = s
    ks = list(out)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            c = out[ks[i]] & out[ks[j]]
            assert not c, 'périmètres %s et %s non disjoints : %s' % (ks[i], ks[j], sorted(c)[:5])
    return out

# ------------------------------------------------------------------ chiffrement
_kc = {}
def _key(secret, salt):
    k = (secret, salt)
    if k not in _kc: _kc[k] = hashlib.pbkdf2_hmac('sha256', secret.encode('utf-8'), salt, ITER, 32)
    return _kc[k]

def seal(plain, secret, salt=None):
    salt = salt or os.urandom(16)
    iv = os.urandom(12)
    return salt + iv + AESGCM(_key(secret, salt)).encrypt(iv, gzip.compress(plain, 9, mtime=0), None)

def unseal(buf, secret):
    salt, iv, ct = buf[:16], buf[16:28], buf[28:]
    return gzip.decompress(AESGCM(_key(secret, salt)).decrypt(iv, ct, None))

# ------------------------------------------------------------------ pré-filtrage des pages (blocs /*PT:BEGIN*/ … /*PT:END*/ exécutés avec node)
def run_pt(D, PROF, block):
    js = "const fs=require('fs');const I=JSON.parse(fs.readFileSync(0,'utf8'));const D=I.D,PROF=I.PROF;(new Function('D','PROF',I.block))(D,PROF);process.stdout.write(JSON.stringify(D));"
    r = subprocess.run(['node', '-e', js], input=json.dumps({'D': D, 'PROF': PROF, 'block': block}, ensure_ascii=False).encode('utf-8'), capture_output=True)
    assert r.returncode == 0, r.stderr.decode()[:600]
    return json.loads(r.stdout.decode('utf-8'))

def pt_block(t):
    assert t.count('/*PT:BEGIN*/') == 1 and t.count('/*PT:END*/') == 1, 'bloc PT absent ou multiple'
    return t[t.index('/*PT:BEGIN*/') + 12:t.index('/*PT:END*/')]

def dumps(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':'))

def prefilter_carte(t, PROF):
    a = t.index('const D={"W"') + len('const D=')
    D, e = json.JSONDecoder().raw_decode(t[a:])
    ids = set(PROF['ids'])
    for m in D.get('moves', []):              # aucune relocalisation partielle dans un périmètre
        n = sum(q['id'] in ids for q in m['p'])
        assert n in (0, len(m['p'])), 'relocalisation partielle (%s) dans %s' % (m.get('k'), PROF['id'])
    D = run_pt(D, PROF, pt_block(t))
    # liste des lieux réduite à ceux qu'utilisent les événements et relocalisations du périmètre (décision du 26/11/2026) ; indices renumérotés
    used = sorted({ev['p'] for ev in D['events']} | {m[k] for g in D['moves'] for m in g['mv'] for k in ('fi', 'ti')})
    nw = {o: n for n, o in enumerate(used)}
    D['places'] = [D['places'][o] for o in used]
    for ev in D['events']: ev['p'] = nw[ev['p']]
    for g in D['moves']:
        for m in g['mv']: m['fi'] = nw[m['fi']]; m['ti'] = nw[m['ti']]
    t = t[:a] + dumps(D) + t[a + e:]
    # note « Exception » : retirée si son entrée n'est pas dans le périmètre
    m = re.search(r'<details class="fq" id="rl-exc" data-pid="([^"]+)">.*?</details>', t, re.S)
    if m and m.group(1) not in ids: t = t.replace(m.group(0), '')
    return t, D

def prefilter_ages(t, PROF):
    m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', t, re.S)
    assert m, 'données Âges introuvables'
    D = run_pt(json.loads(m.group(2)), PROF, pt_block(t))
    return t[:m.start(2)] + dumps(D).replace('</', '<\\/') + t[m.end(2):], D

def prefilter_metiers(t, PROF):
    a = [x.start() for x in re.finditer(r'const D\s*=', t)][-1] + len('const D=')
    D, e = json.JSONDecoder().raw_decode(t[a:])
    X = D['profiles'][PROF['id']]
    ids = set(PROF['ids'])
    N = {k: X[k] for k in ('date', 'bands', 'series', 'emoji', 'branches', 'views', 'bviews')}
    N['nm'] = [r for r in D['nm'] if r[0] in ids]
    return t[:a] + dumps(N) + t[a + e:], N

# ------------------------------------------------------------------ libellés du propriétaire dans le code des pages des périmètres (jamais dans « proches »)
ARTHUR_C = ["'Arthur Schulz-Robellaz (1980–)'", "'Constance Fichet (1984–)'"]
SCRUB = {
    'carte': [("'Arthur Schulz-Robellaz (1980–)'", "'Ascendance A'"), ("'Constance Fichet (1984–)'", "'Ascendance B'")],
    'ages': [("'Arthur Schulz-Robellaz (1980–)'", "'Ascendance A'"), ("'Constance Fichet (1984–)'", "'Ascendance B'"),
             ('1 pour Arthur ou Constance, 2 pour leurs parents', '1 pour la personne de départ, 2 pour ses parents'),
             ('(grands-parents : Arthur, Constance et leurs parents ; arrière-grands-parents : jusqu’aux grands-parents). Au niveau des parents, Arthur et Constance ne sont dans aucune lignée',
              '(grands-parents : les deux personnes de départ et leurs parents ; arrière-grands-parents : jusqu’aux grands-parents). Au niveau des parents, les deux personnes de départ ne sont dans aucune lignée'),
             ("'Arthur : ' + D.meta.nA", "'Ascendance A : ' + D.meta.nA"), ("'), Constance : ' + D.meta.nC", "'), ascendance B : ' + D.meta.nC")],
    'metiers': [("'Arthur Schulz-Robellaz (1980–)'", "'Ascendance A'"), ("'Constance Fichet (1984–)'", "'Ascendance B'"),
                ("(bB.w==='a'?'Arthur':'Constance')", "(bB.w==='a'?'A':'B')"),
                ("who==='a'?'d’Arthur':who==='c'?'de Constance':'d’Arthur et de Constance'", "who==='a'?'de l’ascendance A':who==='c'?'de l’ascendance B':'de l’ascendance'"),
                ("who==='a'?'ascendance d’Arthur':who==='c'?'ascendance de Constance':'ascendance d’Arthur et de Constance'", "who==='a'?'ascendance A':who==='c'?'ascendance B':'ascendance'")],
    'aide': [("d'Arthur et de Constance, côte à côte", "des deux personnes de départ, côte à côte"),
             ("<title>Mode d'emploi — L'Arbre d'Arsène et Lazare</title>", "<title>Mode d'emploi</title>")],
    'arbre': [("<title>L'Arbre d'Arsène et Lazare</title>", '<title>' + NEUTRE + '</title>')],
}
INTERDITS = [r'\bArthur\b(?!\s+[A-ZÉÈ][\wÀ-ÿ\'’-]+)', r'\bConstance\b(?!\s+[A-ZÉÈ][\wÀ-ÿ\'’-]+)', r'arthur-schulz', r'constance-fichet', r'Fichet', r'1980–', r'1984–', r'Arsène et Lazare']

def scrub(name, t):
    for a, b in SCRUB.get(name, []):
        assert a in t, 'motif introuvable dans %s : %s' % (name, a[:60])
        t = t.replace(a, b)
    return t

def verifier_page(name, t, noms_perimetre):
    """Aucun libellé du propriétaire ni de sa conjointe dans le code d'une page de périmètre (hors homonymes : prénom suivi d'un nom, ou personne du périmètre)."""
    for rx in INTERDITS:
        for m in re.finditer(rx, t):
            ctx = t[max(0, m.start() - 25):m.end() + 25]
            if any(n in ctx for n in noms_perimetre): continue
            raise AssertionError('mention interdite dans %s : …%s…' % (name, ctx.replace('\n', ' ')))

# Notes de fiches : formules du propriétaire neutralisées dans les dossiers de périmètre (la base elle-même n'est pas modifiée). Toute autre mention fait échouer le contrôle.
NOTES_SUBST = [('ascendante de Constance', 'ascendante de la conjointe de l’auteur')]

# ------------------------------------------------------------------ données restreintes (même règle que restrict() de common.js)
def restreindre(B, ids):
    s = set(ids)
    o = {'people': {}, 'unions': {}, 'settings': B.get('settings') or {}, 'photos': {}, 'wiki': {}, 'wikifam': {}}
    for k, v in B['people'].items():
        if k in s:
            v = dict(v)
            for f, x in v.items():
                if isinstance(x, str):
                    for a, b in NOTES_SUBST: x = x.replace(a, b)
                    v[f] = x
            o['people'][k] = v
    for k, u in B['unions'].items():
        if u['a'] in s and u['b'] in s: o['unions'][k] = u
    for k, v in o['people'].items():
        ph = v.get('photo')
        if ph and ph in (B.get('photos') or {}): o['photos'][ph] = B['photos'][ph]
        if k in (B.get('wiki') or {}): o['wiki'][k] = B['wiki'][k]
        if k in (B.get('wikifam') or {}): o['wikifam'][k] = B['wikifam'][k]
    return o

# ------------------------------------------------------------------ construction
def lire(W, nom):
    for d in ('out', 'pages'):
        f = '%s/%s/%s.html' % (W, d, nom)
        if os.path.exists(f): return open(f, encoding='utf-8').read()
    raise SystemExit('page introuvable : ' + nom)

def planche(W, n):
    t = open('%s/zip/planche-%d.enc.js' % (W, n), encoding='ascii').read()
    return base64.b64decode(re.search(r'="([A-Za-z0-9+/=]+)";', t).group(1))

SHELL_INDEX = ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
               '<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><title>' + NEUTRE + '</title></head><body>'
               '<script src="common.js"></script><noscript>Cette page nécessite JavaScript.</noscript></body></html>')
HEADERS = '/*\n  X-Robots-Tag: noindex, nofollow\n  Referrer-Policy: no-referrer\n  X-Content-Type-Options: nosniff\n'
CONTACT = ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Formulaire</title></head><body>'
           '<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" hidden>'
           '<input type="hidden" name="form-name" value="contact"><input name="bot-field"><input name="objet"><textarea name="message"></textarea>'
           '<input name="nom"><input name="email" type="email"><input name="page"><input name="profil"></form></body></html>')

LIENS_FILE = os.path.join(REPO, 'liens.enc')

def liens_stockes():
    """Liens déjà attribués, scellés avec le mot de passe « proches » (fichier liens.enc du dépôt). {} si absent ou si le mot de passe manque."""
    pw = os.environ.get('PW_PROCHES')
    if not pw or not os.path.exists(LIENS_FILE): return {}
    try: return json.loads(unseal(open(LIENS_FILE, 'rb').read(), pw))
    except Exception: raise SystemExit('liens.enc : illisible avec ce mot de passe PW_PROCHES (mot de passe modifié ?). Fournir LIEN_* ou retirer liens.enc pour en générer de nouveaux.')

def secret_lien(p, test):
    v = os.environ.get(p['env']) or liens_stockes().get(p['id'])
    if v:
        assert re.fullmatch(r'[a-z0-9]{12}/[A-Za-z0-9]{20}', v), p['env'] + ' : format attendu <jeton12>/<clé20>'
        return v.split('/')
    return ''.join(secrets.choice(ALPHA_JETON) for _ in range(12)), ''.join(secrets.choice(ALPHA_CLE) for _ in range(20))

def build_enc(W, out, test=False):
    B = json.load(open(W + '/bundle.json', encoding='utf-8')); P = B['people']
    profils = load_profils(); per = perimetres(P, profils)
    shell = open(os.path.join(REPO, 'src/shell/common.js'), encoding='utf-8').read()
    assert shell.count("var MODE = 'mdp';") == 1
    pages = {n: lire(W, n) for n in ('arbre', 'carte', 'metiers', 'ages', 'aide', 'cjordan')}
    assert 'Arthur' not in pages['cjordan'], 'page C. Jordan non neutralisée (tools/patch_jordan_neutre.py)'
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    liens, resume = {}, []
    for p in profils:
        pid = p['id']; lien = p['acces'] == 'lien'
        if lien:
            jeton, cle = secret_lien(p, test); liens[pid] = (p['dossier'] + '-' + jeton, cle); d = '%s/%s' % (out, liens[pid][0]); secret = cle
        else:
            d = out; secret = os.environ.get(p['env'])
            if not secret:
                assert test, p['env'] + ' absent : mot de passe de la racine requis'
                secret = ''.join(secrets.choice(ALPHA_CLE) for _ in range(16)); liens[pid] = ('', secret)
        os.makedirs(d, exist_ok=True)
        ids = sorted(per[pid]) if lien else None
        prof = {'id': pid, 'nom': p['nom'], 'titre': titre(p), 'pages': list(p['pages']), 'racines': p['racines'], 'ids': ids, 'pre': bool(lien)}
        M = secrets.token_hex(24); salt = os.urandom(16)
        fich = {}
        if lien:
            PR = prof
            noms = {(v.get('first', '') + ' ' + v.get('last', '')).strip() for k, v in P.items() if k in set(ids)}
            noms |= {v.get('first', '') + ' ' + v.get('last', '') + ' ' for k, v in P.items() if k in set(ids)}
            noms = {n for n in noms if len(n) > 3}
            tc, Dc = prefilter_carte(pages['carte'], PR); ta, Da = prefilter_ages(pages['ages'], PR); tm, Dm = prefilter_metiers(pages['metiers'], PR)
            cont = {'carte': scrub('carte', tc), 'ages': scrub('ages', ta), 'metiers': scrub('metiers', tm), 'arbre': scrub('arbre', pages['arbre']), 'aide': scrub('aide', pages['aide'])}
            if 'cjordan' in p['pages']: cont['cjordan'] = pages['cjordan']
            for n, t in cont.items(): verifier_page(n, t, noms)
            data = restreindre(B, ids)
            verifier_page('data', json.dumps(data, ensure_ascii=False), noms)
            fich['common.js'] = shell.replace("var MODE = 'mdp';", "var MODE = 'lien';").replace(
                "nom: 'Arsène et Lazare', titre: \"L'Arbre d'Arsène et Lazare\"", "nom: '" + NEUTRE + "', titre: '" + NEUTRE + "'").encode('utf-8')
            assert 'Arsène' not in fich['common.js'].decode('utf-8')
            n_ev = len(Dc.get('moves', []))
            resume.append('%-9s %4d personnes ; %2d relocalisations ; %d ancêtres Métiers ; pages %s' % (pid, len(ids), n_ev, len(Dm['nm']), ','.join(p['pages'])))
        else:
            cont = {n: pages[n] for n in ('carte', 'ages', 'metiers', 'arbre', 'aide', 'cjordan')}
            data = {k: B.get(k) or {} for k in ('people', 'unions', 'settings', 'photos', 'wiki', 'wikifam')}
            fich['common.js'] = shell.encode('utf-8')
            fich['contact-form.html'] = CONTACT.encode('utf-8'); fich['_headers'] = HEADERS.encode('utf-8')
            resume.append('%-9s %4d personnes ; pages %s' % (pid, len(P), ','.join(p['pages'])))
        fich['index.html'] = SHELL_INDEX.encode('utf-8')
        fich['data.enc'] = seal(dumps(data).encode('utf-8'), M, salt)
        for n, t in cont.items(): fich[n + '.enc'] = seal(t.encode('utf-8'), M, salt)
        if 'cjordan' in p['pages']:
            for i in range(1, 11): fich['planche-%d.enc' % i] = seal(planche(W, i), M, salt)
        fich['acces-0.enc'] = seal(dumps({'m': M, 'prof': prof}).encode('utf-8'), secret)
        for k, v in fich.items(): open(os.path.join(d, k), 'wb').write(v)
    print('\n'.join(resume))
    if os.environ.get('PERSIST_LIENS') == '1' and not test:       # conserve les liens pour les constructions suivantes (scellés par le mot de passe « proches »)
        store = {pid: '%s/%s' % (liens[pid][0].split('-', 1)[1], liens[pid][1]) for pid in liens if pid != 'proches'}
        open(LIENS_FILE, 'wb').write(seal(json.dumps(store).encode('utf-8'), os.environ['PW_PROCHES']))
        print('liens enregistrés (chiffrés) dans liens.enc')
    print('--- accès (à conserver hors dépôt : affichés une seule fois) ---')
    for p in profils:
        if p['acces'] == 'lien': print('%s : /%s/index.html#k=%s' % (p['id'], liens[p['id']][0], liens[p['id']][1]))
        elif p['id'] in liens: print('%s : mot de passe de test = %s' % (p['id'], liens[p['id']][1]))
        else: print('%s : mot de passe fourni (%s)' % (p['id'], p['env']))

def local_profils(W):
    B = json.load(open(W + '/bundle.json', encoding='utf-8')); P = B['people']
    per = perimetres(P, load_profils())
    f = W + '/zip/profils.js'; s = open(f, encoding='utf-8').read()
    pre = s[:s.index('=') + 1]; PR = json.loads(s[len(pre):].rstrip().rstrip(';'))
    for k, ids in per.items():
        assert PR[k]['racines'] == next(p['racines'] for p in load_profils() if p['id'] == k)
        ancien = set(PR[k]['ids']); assert ancien <= ids, 'identifiants disparus du périmètre %s : %s' % (k, sorted(ancien - ids)[:5])
        PR[k]['ids'] = sorted(ids); print('%s : %d -> %d identifiants' % (k, len(ancien), len(ids)))
    open(f, 'w', encoding='utf-8').write(pre + dumps(PR) + ';')

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; test = '--test' in sys.argv
    mode = a[0] if a else ''
    if mode == 'enc' and len(a) == 3: build_enc(a[1], a[2], test)
    elif mode == 'local-profils' and len(a) == 2: local_profils(a[1])
    elif mode == 'check' and len(a) == 2:
        B = json.load(open(a[1] + '/bundle.json', encoding='utf-8')); per = perimetres(B['people'], load_profils())
        print({k: len(v) for k, v in per.items()})
    else: raise SystemExit(__doc__)
