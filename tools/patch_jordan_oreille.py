"""Page C. Jordan 1917 : le cartouche de droite (frise, légende) se replie par une « oreille » qui dépasse de son bord gauche, en haut
(au lieu du bouton ≫ en haut à droite du cartouche). Dépliée, l'oreille recouvre de 4 px le bord du cartouche (pas de coupure visible) ;
repliée, le cartouche est masqué et le bouton devient un carré aux bords arrondis, au coin haut droit de la carte.
usage : python3 -I tools/patch_jordan_oreille.py <pages/cjordan.html>   (idempotent ; gère la version v1 déjà présente dans le zip ; à appliquer avant patch_jordan_neutre.py)"""
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
if 'oreille-v2' in s: print('déjà appliqué'); sys.exit()
JS = r"""  /* oreille-cartouche oreille-v2 : languette sur le bord gauche du cartouche (en haut) ; ≫ déplié, ≪ replié (alors carré arrondi) */
  const oreille = document.createElement('button');
  oreille.type = 'button'; oreille.className = 'oreille-cartouche'; oreille.textContent = '≫'; oreille.title = 'Replier le cartouche';
  oreille.setAttribute('aria-label', 'Replier le cartouche'); oreille.setAttribute('aria-expanded', 'true');
  const placerOreille = () => {
    const mc = map.getContainer(), mr = mc.getBoundingClientRect(), replie = d.classList.contains('replie');
    oreille.classList.toggle('ferme', replie);
    if (replie) { oreille.style.left = Math.round(mr.width - 10 - oreille.offsetWidth) + 'px'; oreille.style.top = '10px'; }
    else { oreille.style.left = Math.round(d.getBoundingClientRect().left - mr.left - oreille.offsetWidth + 4) + 'px'; oreille.style.top = '18px'; }
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
CSS="""  /* oreille-cartouche oreille-v2 */
  .legend.replie { display: none !important; }
  .oreille-cartouche { position: absolute; z-index: 1001; width: 26px; height: 44px; padding: 0 4px 0 0; border: 1px solid #aaa; border-right: none; border-radius: 8px 0 0 8px; background: #fff; color: #333; font: 700 15px/1 system-ui, sans-serif; cursor: pointer; box-shadow: -2px 0 3px rgba(0,0,0,.25); }
  .oreille-cartouche.ferme { width: 36px; height: 36px; padding: 0; border: 1px solid #aaa; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,.3); }
  .oreille-cartouche:hover, .oreille-cartouche:focus-visible { background: #e6f1ec; }
  .legend .repli { display: none !important; }"""
if 'oreille-cartouche' in s:   # remplace la version v1
    a=s.index("  /* oreille-cartouche : languette"); e="setTimeout(placerOreille, 400);"; b=s.index(e,a)+len(e); s=s[:a]+JS+s[b:]
    a=s.index("  /* oreille-cartouche */"); e=".legend .repli { display: none !important; }"; b=s.index(e,a)+len(e); s=s[:a]+CSS+s[b:]
else:
    a=s.index("  const repli = document.createElement('button');"); e="d.appendChild(repli);"; b=s.index(e,a)+len(e); s=s[:a]+JS+s[b:]
    k='.legend .repli:hover { background: #e6f1ec; }'; assert s.count(k)==1; s=s.replace(k,k+'\n'+CSS)
open(p,'w',encoding='utf-8').write(s); print('ok')
