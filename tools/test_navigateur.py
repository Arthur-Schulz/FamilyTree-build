"""Test en navigateur (Playwright) d'un site chiffré construit : mot de passe de la racine, trois liens à clé, pages, fuites visibles, cas d'erreur.
usage : PW_PROCHES=… LIEN_SCHULZ=… LIEN_BONHOMME=… LIEN_LEFRANC=… python3 tools/test_navigateur.py <site>"""
import sys, os, re, json, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
site = sys.argv[1]
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site); H.log_message = lambda *a, **k: None
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); base = 'http://127.0.0.1:%d' % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
profils = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profils.json')))
INTERDITS = re.compile(r'\bArthur\b(?!\s+[A-ZÉÈ])|\bConstance\b(?!\s+[A-ZÉÈ])|Fichet|Arsène et Lazare|1980–|1984–')
res, fails, errs = {}, [], []
def ko(m): fails.append(m); print('ECHEC', m)
def tour(pg, ctx, pages, nom, interdit):
    for n in pages:
        pg.evaluate("location.hash='#/%s'" % n)
        lab = pg.eval_on_selector('#ft-nv a[data-p=%s] .ft-lb' % n, 'e=>e.dataset.t')
        fr, txt = None, ''
        for _ in range(240):                      # cadre isolé (sandbox) : lecture par l'API de cadre, pas par contentDocument
            el = pg.query_selector('iframe.ft-fr.on')
            if el and el.get_attribute('title') == lab:
                try:
                    fr = el.content_frame(); txt = fr.evaluate('document.body?document.body.innerText:""')
                    if len(txt) > 150: break
                except Exception: pass
            pg.wait_for_timeout(250)
        pg.wait_for_timeout(700); txt = fr.evaluate('document.body.innerText')
        res['%s/%s' % (nom, n)] = len(txt)
        if interdit and INTERDITS.search(txt): ko('%s/%s : texte visible interdit : %s' % (nom, n, INTERDITS.search(txt).group(0)))
        if n == 'carte':
            try: res[nom + '/relocalisations'] = fr.evaluate("document.querySelector('#rl-ne')&&document.querySelector('#rl-ne').textContent")
            except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch()
    # racine : mot de passe
    ctx = b.new_context(); pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'font' not in m.text.lower() and 'tile' not in m.text.lower() and 'ERR_' not in m.text and '404' not in m.text and 'Permissions policy' not in m.text else None)
    pg.goto(base + '/index.html'); pg.wait_for_selector('#ft-pw')
    pg.fill('#ft-pw', 'mauvais'); pg.click('#ft-gate button'); pg.wait_for_selector('.ft-err:not([hidden])', timeout=60000)
    if 'incorrect' not in pg.inner_text('.ft-err'): ko('racine : mot de passe faux non signalé')
    pg.fill('#ft-pw', os.environ['PW_PROCHES']); pg.click('#ft-gate button'); pg.wait_for_selector('.ft-nv a, #ft-nv a', timeout=60000)
    res['proches/titre'] = pg.inner_text('#ft-ti'); res['proches/menu'] = pg.eval_on_selector_all('#ft-nv a', 'e=>e.map(x=>x.dataset.p)')
    tour(pg, ctx, res['proches/menu'], 'proches', False); ctx.close()
    # liens
    for pr in profils:
        if pr['acces'] != 'lien': continue
        jeton, cle = os.environ[pr['env']].split('/'); url = '%s/%s-%s/index.html' % (base, pr['dossier'], jeton)
        ctx = b.new_context(); pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(url + '#k=' + cle); pg.wait_for_selector('#ft-nv a', timeout=60000)
        if pg.query_selector('#ft-gate'): ko(pr['id'] + ' : formulaire de saisie affiché')
        if 'k=' in pg.evaluate('location.href'): ko(pr['id'] + ' : clé restée dans l\'adresse')
        res[pr['id'] + '/titre'] = pg.inner_text('#ft-ti'); menu = pg.eval_on_selector_all('#ft-nv a', 'e=>e.map(x=>x.dataset.p)'); res[pr['id'] + '/menu'] = menu
        if menu != pr['pages']: ko('%s : menu %s != %s' % (pr['id'], menu, pr['pages']))
        tour(pg, ctx, menu, pr['id'], True)
        if 'cjordan' not in pr['pages']:
            pg.evaluate("location.hash='#/cjordan'"); pg.wait_for_selector('.ft-msg', timeout=15000)
            if 'pas disponible' not in pg.inner_text('.ft-msg'): ko(pr['id'] + ' : page Jordan non bloquée')
        pg2 = ctx.new_page(); pg2.goto(url); pg2.wait_for_selector('#ft-nv a', timeout=60000)   # réouverture sans clé
        ctx.close()
        for lab, u in (('sans clé', url), ('clé fausse', url + '#k=' + 'x' * 20)):
            c2 = b.new_context(); q = c2.new_page(); q.goto(u); q.wait_for_selector('#ft-gate', timeout=60000); q.wait_for_selector('.ft-err', timeout=60000)
            if 'incomplet' not in q.inner_text('.ft-err'): ko('%s %s : message attendu absent' % (pr['id'], lab))
            if q.query_selector('#ft-gate input'): ko('%s %s : champ de saisie présent' % (pr['id'], lab))
            c2.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('erreurs JS :', errs[:6])
if errs: fails.append('erreurs JS')
print('RESULTAT', 'ECHEC' if fails else 'OK'); sys.exit(1 if fails else 0)
