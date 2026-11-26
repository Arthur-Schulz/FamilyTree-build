"""Carte, relocalisations : (1) ordre des lignées dans la frise et la légende = ordre de l'arbre (Schulz, Denis, Jordan, Bonhomme, Hachette, Masson, Le Franc, Jacquey) ;
(2) pictogramme ⏮ devant « Revenir au début », dans le style des flèches ◀ ▶ (classe .tri).
usage : python3 -I tools/patch_carte_ordre.py <pages/carte.html>   (idempotent ; à appliquer après patch_carte_reloc.py et patch_carte_bonhomme.py)"""
import sys,re
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
O='[1,2,3,8,4,5,6,7]'
R=[('rows=[...new Set(items.map(i=>i.row))].sort((a,b)=>a-b);','rows=[...new Set(items.map(i=>i.row))].sort((a,b)=>'+O+'.indexOf(a)-'+O+'.indexOf(b));'),
   ('<span data-b="8"><i class="rl-sw b8"></i>Bonhomme</span>',''),
   ('<span data-b="3"><i class="rl-sw b3"></i>Jordan</span>','<span data-b="3"><i class="rl-sw b3"></i>Jordan</span><span data-b="8"><i class="rl-sw b8"></i>Bonhomme</span>'),
   ('aucun événement sélectionné">Revenir au début</button>','aucun événement sélectionné"><span class="tri" aria-hidden="true">&#x23EE;&#xFE0E;</span> Revenir au début</button>')]
if O not in s:
    for a,b in R:
        assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
    open(p,'w',encoding='utf-8').write(s); print('ok')

# (3) 26/11/2026 : ⏮ forcé en emoji (U+FE0F) ; bouton « Revenir au début » placé en première position
s=open(p,encoding='utf-8').read()
if '&#x23EE;&#xFE0E;' in s: s=s.replace('&#x23EE;&#xFE0E;','&#x23EE;&#xFE0F;')
m=re.search(r'<button type="button" id="rb-first".*?</button>',s)
if m and s.index('id="rb-first"')>s.index('id="rb-prev"'):
    btn=m.group(0); s=s.replace(btn,'',1); a='<button type="button" id="rb-prev">'; assert s.count(a)==1; s=s.replace(a,btn+a)
open(p,'w',encoding='utf-8').write(s); print('ordre boutons ok')

# (4) 26/11/2026 (révisé) : emoji abandonnés. ◀ et ▶ reviennent aux symboles d'origine (U+2BC7 / U+2BC8) ; « Revenir au début » reçoit un pictogramme SVG noir et blanc
# (barre + double triangle, couleur du texte) à la taille des symboles.
s=open(p,encoding='utf-8').read()
s=s.replace('&#x25C0;&#xFE0F;','&#x2BC7;').replace('&#x25B6;&#xFE0F;','&#x2BC8;')
SVG=('<span class="tri tri-first" aria-hidden="true"><svg viewBox="0 0 22 12" width="22" height="12" fill="currentColor" focusable="false">'
     '<rect x="0" y="0" width="2.6" height="12"/><polygon points="12,0 12,12 3.6,6"/><polygon points="21.4,0 21.4,12 13,6"/></svg></span>')
for old in ('<span class="tri" aria-hidden="true">&#x23EE;&#xFE0F;</span>','<span class="tri" aria-hidden="true">&#x23EE;&#xFE0E;</span>'):
    s=s.replace(old,SVG)
if '.tri-first' not in s:
    a='.tri{font-size:17px;line-height:1;vertical-align:-1px;margin:0 3px}'; assert s.count(a)==1
    s=s.replace(a,a+'.tri-first svg{display:inline-block;vertical-align:-1px}')
open(p,'w',encoding='utf-8').write(s); print('picto ok')

# (5) 26/11/2026 : libellés courts des boutons de navigation
s=open(p,encoding='utf-8').read()
for a,b in (('</span> Revenir au début</button>','</span> Début</button>'),('Événement précédent</button>','Précédent</button>'),('>Événement suivant <span class="tri"','>Suivant <span class="tri"'),
            ('<span class="tri" aria-hidden="true">&#x2BC7;</span> Événement précédent','<span class="tri" aria-hidden="true">&#x2BC7;</span> Précédent')):
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('libellés ok')
