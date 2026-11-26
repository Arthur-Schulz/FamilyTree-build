"""Carte, relocalisations : ajoute la lignée Bonhomme (8e couleur) à la légende, à la frise et aux flèches.
Contexte : seules 7 lignées (Schulz, Denis, Jordan, Hachette, Masson, Le Franc, Jacquey) étaient définies ; les entrées de la branche de Joseph Bonhomme
n'avaient aucune lignée (b = []) et n'apparaissaient donc pas dans la frise. Pendant : IDX/BN de src/rebuild_moves.py (8 = joseph-bonhomme).
usage : python3 -I tools/patch_carte_bonhomme.py <pages/carte.html>   (idempotent ; le gabarit vient du zip d'entrée)"""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
if '--c8:' in s: print('déjà appliqué'); sys.exit()
R=[('--c6:#9a7400;--c7:#0b7285}','--c6:#9a7400;--c7:#0b7285;--c8:#5f7f0f}',1),
   ('--c6:#e3c24f;--c7:#5cc9dd}}','--c6:#e3c24f;--c7:#5cc9dd;--c8:#a8d26a}}',1),
   ('--c6:#e3c24f;--c7:#5cc9dd}\n','--c6:#e3c24f;--c7:#5cc9dd;--c8:#a8d26a}\n',1),
   ('.b7{color:var(--c7)}','.b7{color:var(--c7)}.b8{color:var(--c8)}',1),
   ('<span data-b="7"><i class="rl-sw b7"></i>Jacquey</span>','<span data-b="7"><i class="rl-sw b7"></i>Jacquey</span><span data-b="8"><i class="rl-sw b8"></i>Bonhomme</span>',1),
   ("7:'Jacquey'}","7:'Jacquey',8:'Bonhomme'}",1),
   ('for(let q=1;q<=7;q++) s+=\'<pattern id="rlhz','for(let q=1;q<=8;q++) s+=\'<pattern id="rlhz',1)]
for a,b,n in R:
    assert s.count(a)==n,(a,s.count(a)); s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('ok')
