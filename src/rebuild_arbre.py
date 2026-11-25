"""Arbre : page de l'arbre du zip local = HTML de l'artifact (version live) + adaptations « zip » (lecture seule, données dans data.enc, coque).
usage : python3 -I src/rebuild_arbre.py <artifact_index.html> <pages/arbre.html du zip d'entrée> <sortie.html>
Les éléments propres au zip (début d'en-tête, CSS « lecture seule » et bouton Mode d'emploi, script de substitution de la base,
réglages mémorisés par la coque) sont repris de la page du zip d'entrée ; tout le reste vient de l'artifact. Chaque remplacement
exige une ancre unique : si l'artifact change à cet endroit, la construction échoue au lieu de produire une page fausse."""
import sys
art, old, out = sys.argv[1:4]
A = open(art, encoding='utf-8').read(); Z = open(old, encoding='utf-8').read()
def rep(s, o, n, what):
    assert s.count(o) == 1, ('ancre introuvable ou multiple', what, s.count(o)); return s.replace(o, n)
MAIN = "<script>\n(function(){\n'use strict';\n// ==LOGIC=="
# 1. en-tête : première ligne du zip ; titre, meta et ouverture de <style> de l'artifact retirés ; titre déplacé après le style
l0 = Z.split('\n', 1)[0]
a0, rest = A.split('\n', 1)
assert rest.startswith("<title>L&#39;Arbre d&#39;Arsène et Lazare</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n<style>\n"), rest[:200]
rest = rest.split('<style>\n', 1)[1]
rest = rep(rest, '</style>\n<link rel="preconnect"', '</style><title>L\'Arbre d\'Arsène et Lazare</title></head><body>\n<link rel="preconnect"', 'fin du style')
H = l0 + '\n' + rest
# 2. barre d'outils : titre retiré (il est dans l'en-tête commun), bouton Mode d'emploi
hb = Z[Z.index('    <a class="btn primary" id="b-help"'):]; hb = hb[:hb.index('</a>') + 4]
H = rep(H, "    <h1>L'Arbre d'Arsène et Lazare</h1>\n", "    \n" + hb + "\n", 'h1')
# 3. CSS lecture seule (zip) inséré en tête du dernier bloc <style> ; script de substitution de la base avant le script principal
k = H.index(MAIN); s0 = H.rindex('<style>\n', 0, k)
first = H[s0 + 8:].split('\n', 1)[0]
zi = Z.index('<style>\n/* Lecture seule'); zf = Z.index('\n' + first + '\n', zi)
css = Z[zi + 8:zf + 1]
H = H[:s0 + 8] + css + H[s0 + 8:]
shim = Z[Z.index("<script>\n(function(){\n'use strict';\ndocument.documentElement.classList.add('ro')"):]
shim = shim[:shim.index('</script>') + 9]
H = rep(H, "</style>\n\n" + MAIN, "</style>\n" + shim + "\n" + MAIN, 'script de substitution')
# 4. réglages (pas de localStorage dans le cadre isolé), focus, fiche demandée, photos, réglages wiki lus dans les données
H = rep(H, "try{ showJobs=localStorage.getItem('gen-jobs')==='1'; }catch(e){}",
        "showJobs=!!(window.__FT_STATE&&window.__FT_STATE.jobs==='1');   /* réglage mémorisé par la coque (pas de localStorage dans le cadre isolé) */", 'gen-jobs')
H = rep(H, "try{ const raw=localStorage.getItem('gen-collapsed-up2'); if(raw!==null){ const s=JSON.parse(raw); if(Array.isArray(s)){ collapsedUp=new Set(s); hasFoldPref=true; } } }catch(e){}\n"
           "const saveCollapsed=()=>{ try{ localStorage.setItem('gen-collapsed-up2',JSON.stringify([...collapsedUp])); }catch(e){} };\n",
        "\nconst saveCollapsed=()=>{};\n"
        "/* coque : ouverture d'une fiche demandée alors que la page est déjà chargée ; lien « Mode d'emploi » */\n"
        "window.addEventListener('message',ev=>{ if(ev.source===parent&&ev.data&&ev.data.ft==='locate'&&typeof ev.data.id==='string') setTimeout(()=>locate(ev.data.id),0); });\n"
        "{ const h=document.getElementById('b-help'); if(h) h.addEventListener('click',e=>{ e.preventDefault(); if(window.FTGO) window.FTGO('aide'); }); }\n", 'gen-collapsed-up2')
H = rep(H, "function pickFocus(){\n", "function pickFocus(){\n  if(window.__FT_FOCUS&&people.has(window.__FT_FOCUS)){ focus=window.__FT_FOCUS; return focus; }\n", 'pickFocus')
H = rep(H, "function render(){\n", "function render(){\n  if(window.__dl&&ready&&people.size){ const id=window.__dl; window.__dl=null; setTimeout(()=>locate(id),0); }\n", 'render')
H = rep(H, """(p.photo?'<img src="/_blob/'+esc(p.photo)+'" alt="">':'')""", """(p.photo?(window.__PHOTOS&&window.__PHOTOS[p.photo]?'<img src="'+window.__PHOTOS[p.photo]+'" alt="">':''):'')""", 'photo')
i = H.index("  db.doc('settings/wiki').onSnapshot("); j = H.index('\n', i)
H = H[:i] + H[j + 1:]
open(out, 'w', encoding='utf-8').write(H)
print('arbre', len(H))
