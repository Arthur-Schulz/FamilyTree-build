"""Carte, relocalisations : (1) ordre des lignées dans la frise et la légende = ordre de l'arbre (Schulz, Denis, Jordan, Bonhomme, Hachette, Masson, Le Franc, Jacquey) ;
(2) pictogramme ⏮ devant « Revenir au début », dans le style des flèches ◀ ▶ (classe .tri).
usage : python3 -I tools/patch_carte_ordre.py <pages/carte.html>   (idempotent ; à appliquer après patch_carte_reloc.py et patch_carte_bonhomme.py)"""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
O='[1,2,3,8,4,5,6,7]'
R=[('rows=[...new Set(items.map(i=>i.row))].sort((a,b)=>a-b);','rows=[...new Set(items.map(i=>i.row))].sort((a,b)=>'+O+'.indexOf(a)-'+O+'.indexOf(b));'),
   ('<span data-b="8"><i class="rl-sw b8"></i>Bonhomme</span>',''),
   ('<span data-b="3"><i class="rl-sw b3"></i>Jordan</span>','<span data-b="3"><i class="rl-sw b3"></i>Jordan</span><span data-b="8"><i class="rl-sw b8"></i>Bonhomme</span>'),
   ('aucun événement sélectionné">Revenir au début</button>','aucun événement sélectionné"><span class="tri" aria-hidden="true">&#x23EE;&#xFE0E;</span> Revenir au début</button>')]
if O in s: print('déjà appliqué'); sys.exit()
for a,b in R:
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('ok')
