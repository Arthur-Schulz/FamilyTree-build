"""Aligne le centre optique des pictogrammes du menu (common.js d'un zip local) sur celui de l'arbre.
usage : python3 -I tools/patch_nav_icons.py <common.js>   (idempotent)
Décalages mesurés sur les pixels le 26/11/2026 : Métiers +0,6 px, C. Jordan 1917 -1,1 px (les autres pictogrammes sont déjà à 10,9 px)."""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
a="mask:var(--i) center/contain no-repeat}',\n"
if 'data-p=\\"metiers\\"] .ft-ic' in s or 'data-p="metiers"] .ft-ic' in s: print('déjà appliqué'); sys.exit()
assert s.count(a)==1
s=s.replace(a,a+"    '.ft-nav a[data-p=\"metiers\"] .ft-ic{transform:translateY(.6px)}.ft-nav a[data-p=\"cjordan\"] .ft-ic{transform:translateY(-1.1px)}',\n")
open(p,'w',encoding='utf-8').write(s); print('ok')
