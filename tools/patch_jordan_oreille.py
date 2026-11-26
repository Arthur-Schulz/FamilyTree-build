"""Page C. Jordan 1917 : le cartouche de droite (frise, légende) se replie par une « oreille » qui dépasse de son bord gauche, en haut
(au lieu du bouton ≫ en haut à droite du cartouche). Replié, le cartouche est masqué et l'oreille reste visible au bord droit de la carte.
usage : python3 -I tools/patch_jordan_oreille.py <pages/cjordan.html>   (idempotent ; à appliquer avant patch_jordan_neutre.py)"""
import sys,re
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
if 'oreille-cartouche' in s: print('déjà appliqué'); sys.exit()
a=s.index("  const repli = document.createElement('button');"); e="d.appendChild(repli);"; b=s.index(e,a)+len(e)
JS = r"""  /* oreille-cartouche : languette sur le bord gauche du cartouche (en haut) ; ≫ déplié, ≪ replié */
  const oreille = document.createElement('button');
  oreille.type = 'button'; oreille.className = 'oreille-cartouche'; oreille.textContent = '≫'; oreille.title = 'Replier le cartouche';
  oreille.setAttribute('aria-label', 'Replier le cartouche'); oreille.setAttribute('aria-expanded', 'true');
  const placerOreille = () => {
    const mc = map.getContainer(), mr = mc.getBoundingClientRect(), replie = d.classList.contains('replie');
    const bord = replie ? mr.right - 10 : d.getBoundingClientRect().left;
    oreille.style.left = Math.round(bord - mr.left - oreille.offsetWidth + (replie ? 0 : 1)) + 'px';
    oreille.style.top = '18px';
  };
  oreille.addEventListener('click', e => {
    e.stopPropagation();
    const r = d.classList.toggle('replie');
    oreille.textContent = r ? '≪' : '≫'; oreille.title = r ? 'Déplier le cartouche' : 'Replier le cartouche';
    oreille.setAttribute('aria-label', oreille.title); oreille.setAttribute('aria-expanded', String(!r));
    placerOreille();
  });
  L.DomEvent.disableClickPropagation(oreille);
  map.getContainer().appendChild(oreille);
  if (window.ResizeObserver) { const ro = new ResizeObserver(placerOreille); ro.observe(d); ro.observe(map.getContainer()); }
  window.addEventListener('resize', placerOreille); map.on('resize', placerOreille); setTimeout(placerOreille, 0); setTimeout(placerOreille, 400);"""
s=s[:a]+JS+s[b:]
CSS="""
  /* oreille-cartouche */
  .legend.replie { display: none !important; }
  .oreille-cartouche { position: absolute; z-index: 1001; width: 22px; height: 44px; padding: 0; border: 1px solid #aaa; border-right: none; border-radius: 8px 0 0 8px; background: #fff; color: #333; font: 700 15px/1 system-ui, sans-serif; cursor: pointer; box-shadow: -1px 1px 3px rgba(0,0,0,.3); }
  .oreille-cartouche:hover, .oreille-cartouche:focus-visible { background: #e6f1ec; }
  .legend .repli { display: none !important; }
"""
k='.legend .repli:hover { background: #e6f1ec; }'; assert s.count(k)==1
s=s.replace(k,k+CSS)
open(p,'w',encoding='utf-8').write(s); print('ok')
