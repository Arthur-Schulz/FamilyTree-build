"""Carte, onglet Relocalisations : bouton « Revenir au début » (remet la navigation à l'état initial, aucune flèche sélectionnée).
usage : python3 -I tools/patch_carte_reloc.py <pages/carte.html>   (idempotent ; le gabarit de la Carte vient du zip d'entrée)"""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
if 'id="rb-first"' in s: print('déjà appliqué'); sys.exit()
R=[('<button type="button" id="rb-next">Événement suivant <span class="tri" aria-hidden="true">&#x2BC8;</span></button></div>',
    '<button type="button" id="rb-next">Événement suivant <span class="tri" aria-hidden="true">&#x2BC8;</span></button><button type="button" id="rb-first" title="Revenir à l\\\'état initial : aucun événement sélectionné">Revenir au début</button></div>'),
   ("rbP=$('#rb-prev'), rbN=$('#rb-next');","rbP=$('#rb-prev'), rbN=$('#rb-next'), rbF=$('#rb-first');"),
   ("rbP.addEventListener('click',()=>rStep(-1)); rbN.addEventListener('click',()=>rStep(1));",
    "rbP.addEventListener('click',()=>rStep(-1)); rbN.addEventListener('click',()=>rStep(1)); rbF.addEventListener('click',()=>{ R.nav=0; R.hov=null; render(); });"),
   ("rbP.disabled=R.nav<1;","rbP.disabled=R.nav<1; rbF.disabled=R.nav<1;")]
for a,b in R:
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('ok')
