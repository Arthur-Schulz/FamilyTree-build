"""Carte : « 1/2^g » devient 1/2<sup>G</sup> (G majuscule en exposant) dans le bouton, l'infobulle et le texte « À lire ».
usage : python3 -I tools/patch_carte_pond.py <pages/carte.html>   (idempotent ; le gabarit de la Carte vient du zip d'entrée, pas du dépôt)"""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
if '1/2<sup>G</sup>' in s: print('déjà appliqué'); sys.exit()
R=[('<b>1/2^g</b> : chaque ancêtre pèse 1/2^g (','<b>1/2<sup>G</sup></b> : chaque ancêtre pèse 1/2<sup>G</sup> ('),
('title="Chaque ancêtre pèse 1/2^g (g = génération)">1/2^g</button>','title="Chaque ancêtre pèse 1/2^G (G = génération)">1/2<sup>G</sup></button>'),
('<b>pondération 1/2^g</b>','<b>pondération 1/2<sup>G</sup></b>'),
('.wtip{position:absolute','#lab-wt sup,.seg sup,.wtip sup,.fb sup{font-size:.72em;line-height:0;vertical-align:baseline;position:relative;top:-.45em}\n.wtip{position:absolute')]
for a,b in R:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('ok')
