"""Test en navigateur de la page Métiers d'un site chiffré : chaque famille de la légende ouvre sa fenêtre sans erreur JS (régression du 27/11/2026 : table des noms décalée dans les périmètres). L'appartenance des noms au périmètre est vérifiée à la construction (assertions de prefilter_metiers).
usage : PW_PROCHES=… python3 tools/test_metiers.py <site> [liens : schulz=/dossier-jeton/index.html#k=clé …]"""
import os, sys, threading, http.server, socketserver, functools, json
from playwright.sync_api import sync_playwright
site = sys.argv[1]
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site); H.log_message = lambda *a, **k: None
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); base = 'http://127.0.0.1:%d' % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
liens = {}
for p in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profils.json'))):
    if p['acces'] == 'lien': liens[p['id']] = '/%s-%s/index.html#k=%s' % ((p['dossier'],) + tuple(os.environ[p['env']].split('/')))
JS = """()=>{const out=[];document.querySelectorAll('#lg .lk').forEach((b,i)=>{b.click();const ov=document.querySelector('.ov');out.push([b.textContent.trim().slice(0,30),!ov.hidden,[...ov.querySelectorAll('li')].map(l=>l.textContent.trim()), [...ov.querySelectorAll('summary span')].map(l=>l.textContent.trim())]);ov.hidden=true;});return out}"""
ok = True
def run(pg, nom, errs):
    global ok
    pg.evaluate("location.hash='#/metiers'"); fr = None
    for _ in range(240):
        el = pg.query_selector('iframe.ft-fr.on')
        if el and 'tiers' in (el.get_attribute('title') or ''):
            try:
                fr = el.content_frame()
                if fr.evaluate("document.querySelectorAll('#lg .lk').length") > 0: break
            except Exception: pass
        pg.wait_for_timeout(250)
    res = fr.evaluate(JS)
    ferm = [r[0] for r in res if not r[1]]
    print('%s : %d familles, %d ne s\'ouvrent pas %s' % (nom, len(res), len(ferm), ferm)); ok &= not ferm
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(viewport={'width': 1400, 'height': 1000}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(base + '/index.html'); pg.wait_for_selector('#ft-pw'); pg.fill('#ft-pw', os.environ['PW_PROCHES']); pg.click('#ft-gate button'); pg.wait_for_selector('#ft-nv a', timeout=60000)
    run(pg, 'proches', errs)
    for n, u in liens.items():
        q = b.new_context().new_page(); q.on('pageerror', lambda e: errs.append(str(e))); q.goto(base + u); q.wait_for_selector('#ft-nv a', timeout=60000); run(q, n, errs)
    print('erreurs JS :', errs); ok &= not errs; b.close()
print('RESULTAT', 'OK' if ok else 'ECHEC'); sys.exit(0 if ok else 1)
