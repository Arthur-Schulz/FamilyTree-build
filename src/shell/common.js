/* En-tête et menu communs, saisie du mot de passe et déchiffrement. Ce fichier ne contient aucune donnée de l'arbre. */
(function () {
  'use strict';
  var ITER = 600000;
  var PAGE = '';                          // page affichée (route courante)
  var PAGE_JMO = 'cjordan';
  var ICONS = {"arbre": "data:image/png;base64,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", "carte": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAHg0lEQVR42u2bX4hVZRDAf+de13U1zcQlizYXUiOyRKOgMgzFBFfMh10lUFECEYV9tTfNByUwCUR9MhZ18Q8pIpYPPUiFiElIIv6pl6DMPy2Strru7r339LAzOA3fuXvueu/eXfPA4Z495/vm3zcz38x8s/DkquoVyV1VAgYLT0aeC0D8iOOGjQAycucC37JAjTz3AvnAmBEiiMJwE0DWMVQHzADeAqYBzwMvAA3y/XfgD+BP4BfgR+BnoKsIzCF5ZYwKA3wA7ALOAt2i0mnubpmzS2AkwR9SV9Y8vwccc0zlgQdG3ePA914Z478fE5ghXEPiGiG/M4B2t9rdwphnuFdUvKvIdw+nXXBYnFX3AWqbTcAe4FkhOGecHMBF4CfgO7H5m8AN+TZJ5jUAc4A3gOlmbq8wHMm8j4Gvq+0XIrMKq4H7ZuVUhQvAAWA+MKEE2BNkzgGzHeaNptwXnBjBVE3tNxg1zRmCvwHmBeZkxZFF7s7IN6/a8wSWCjRn8G0opzkMxOE1m9WxhH1ivHVkmC5lN8malc0ITCto1bLmwXaMysg7QIdTzX+A5WXesiyc5YLDmlqH0MJgbJGK4FXgulmNGPgbWGhWIypjLhCZFV4ouCzu60JTRYUQGRttN6tQADqBRTKuJgWMqMRvONiLBGfBaF+78TFRJe3+XdmTrR2uTeGMsgFm6uSu6WdsyPmudf6nW2irmD9QdT0uiHvk92TAaSWZTq3EC18Cl4Fbcl+Wd00yppgqW6d60tFyvFIptkp0vtnq9J7Tj9SVmKXA6RR5wGkZWyxQU1xzHC05obHsWqBqt9uEpTFwqAihNrff5GL+HhMv6P7e43KATUYToiKCPeRo2l3u2ECZeBq4YJxfDljgPHRolVpdJJd38X13ICHSMa1FVlNNboHQos7wgtBath1Bkb8tiYsS9yswMQGRzlliVtgyvgdoAV6Su0XeWUGohixJEILinCi06LwuobVsZuBXskt+9yYgUSf0FHDGaIzu22uK4Fpj9nadc0ZghZyb4t7raGstpwBU0jsdYasT1D9r9mq/TS01Y7KGqayZtzSwzS5KYEhhrHa07UxrAmlsROtxz5k5saS0caBwqeM/MgLIAm3AYdnzvUmoytfImDaT6sYCi0BtMHa0ZBythXIIQCXdYObkJS8PXbEwMsulzKf6qfbGhuBTLtWdJTCTqsQ3hSblp6Fc6q82N8rE/mpr9YEtMDJF0L/M+B4phvZXhNFv00xwEwusuiL46o39a24wKk3RJ1OCH6hNiA3SXKrmaROffIlnAp6W2rS8ZVIQjjiku+b9SKAxIGE7vsO8Gwm87uw0iZ5Yxo408DrM2UIc0IBGGa/X3YTxA9aAWLIvteEMMLnICvZKWVs9M8BiVw1KihyzMhbj1c/Kc5IGTZa56kM602pQWgHkgGvOszYmwNC/DxsnmAdWyXbV69JWm2b3yphVMked4OF+cDU62q4lnEYNSACRSPOS/J03Ug85mYK8+16CmMg4p93AskBIrCHwMpNvxDL3jMCKAtta5GhR2i6Z+SU5j6QtMAdccTY1xTisyLyPZU4n8DnwlbHtEcBB4H3gB+CczHmTvoOPtc7MIoHRGSiBW9xTHG1XHO1lyQS1EJI3W9PUIpqk7za6VS4USYYKTjs2poA/1Wy5eVcYKevhyXj6Djds6rmySDZo0+HWQDqc7+ddaz/psPqQlY6mi0JrWQ9/lcF9skoP5LethOCmuYSCSHMJcNscTfsqURBRYC1GVWPxtuNSlKGyJkBZDOwPlMT2y7faFAwovnFCg6WppRICUObGAFeN2sbAipQIy1UUtd9XOFquCo0V6X1Qe95ibK5A34Hn+JQHIY9aFrcHJeMFd8HY/5ZKng2o1F8Gbrua/LoBIh5IBVdxrHNnE7eFtooekyngHa4A8ZuUpird9aXwJwpOS8OOwTgjzJh09Y4rbGweBAIU9mZXSLlj0u1BOx/8zOT6ejw2o4JEZEwXSqcppcdCC4PVP6QBTr2UoAsuaxtbAVNQeGNdllkQGuqLBEwVVcWWQH/A9hJPiEs5Gd4e6A9oqVbjlKrbQUNUTiKypjLG4gqjSWDnjLAPDqbqhwQQAa9IDc5qwS1gZhmI07kzBaZd/euCO6pm76CuznqnBZqUjCmSLKUxs0hgXAzAX1+t/qCQQ6wDTgSIPNJPRpemufpIAO4JwZmpdre5L02fc4enMbB1AG0zqjFbDfO605xLKMlT7R5hgBdNsmRXbGNKTYgChRQL56rgYCj2DGdNA9WNQNPkp2ZcpkhrHDLWN0feMI1QQ65X2DvF6fy3kyvnhJB0wmOZz7kOtOlDwemVIoTZPDygsB2kXxgNsKfCGflmO0L1QGb2cGHeC2GuYd5Gb23AaDN+tLyzUaXOmTvcmPdC+NDYsd0dvqWvS3ySPHtv3ytzhyXz3jE2AfcSgqVQkHPPhNNZhvmlq/cacD7ArP/7vIwd1iufJIRngKNui7Nb5VEZ81gx74OlLLAt0Ce4ze0Ij+VlI8FV9J3hXZFnqp3ZVePfZWt4eCZQ9X+jrZZJ8H9Y9SfXUL3+BToE9NBQSzuuAAAAAElFTkSuQmCC", "metiers": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEw0lEQVR42u2bS4scVRTHf9VdPdGeERMxBiNGXIREovjYBBVFRFFc+RFEiV9A3ChuXblwFaLiQnERNyK4yUoxKqLoQsRnIvhCdEaJ2pke+1XlYv4Fx2tV9739mKmaqQOH6uq+99S5/zr3nHvOvQ011bSrKSrxs9KdAHBjTjKiqllAJE50vwTEgTKGQN/RM60CAJFR9FHgQeA24Gp9H3mYfgT8DHwCvAecypFdamoCL0jZefBpWVBEyR1qU+b+uhQfAgNNhdBBJ5oCfd2/ZMCNyuzwHpfCfWfgF4F1T76YA8QQeGSOznVhDvW0ASAFvgceAFbE7Qm8rHYPq28qK0qBN7YhfP/PsxcxQAv4WsqOxA/N8Mx79OYT8TlNMV99tjwG7wG6xnzXpwh/lmLJyOR19YyQl9aY9IBxnX3jeBae2jlhap8GERLCsrbLOSHyMuMIU491RDqubTRBgWuAZ4D7AuJ427nvzmiFofIyHX8CzgLPAd/KEpIQsz8GnJ8ybidThr5FyDsPXK9xNUK8+csS0JvzYLaKE+meAi8Whc+4wIRawJ0S0hIoXapFbemeAvfq82ASAJEB4JBBrAtcp2uZ1+PWGf9g/MdBA8B/9I8D8vGOTKoKNPKtLYTE6FhhpQoWEIcMKqRCk1agWpOG6Ndgl1NcwjpkulMBaJj1hG/bHQVANqDlMSBEyhuSMlZtm1P6jKzPIeXzvwKrwJrDv+m3M2rLDM9rzjo/204aum7atAJT5KxUdjZgGXtmirw+km4Zufq383yQL8KXAE8oOxyYjGu763ORkxoPlPg8KZ3nYgGJk1k9C1xboITPFOgU1Ac7Yp8pkPfMI8DzwI9OQjTWAkIA6BnBHeAkcPsY5YpAWZ5QDyySV1QWvxt4Fdgw+vUWAUAmeGDu/wHeBE4ANzlz0PqMWNemp7O1ffIi1zHgMeAtR5+BqQJ5ARCNyabWTIlrBPwBHDBt+6ZAmZWgzgEfsrmb8wXwpeNAp01rjwI3AseBu3TfMgungaPLKnCFscIusD8vm/UBIPOox2VuJ4BbTZ+e3or7djcEwHeStQr87lxX1fYq8ZXOdb+c2g1slsrdjG/oFEk/V/HjHeAjM6UKAQgJgw1TIL0feEVx24avkQDZ8Nz16Yr7HlWnjYLq1BrwGpvl9z3GeXqFwRAAVnLe8hHgKcX4To7SPaN4X6Y6Khhsot+yeWz7um3/Bt4FnpZ1uD5kxRcA3yngmlDGI9PvoMpodwC3aJ4emFO8/wX4BvgUeB/42FhfNmgL0CT901kBSJ04nbd2PwocBm5mc29gH7AXuFzXvfoO4ALwp/gvXS+IPwO+0hqkaI2RTKl/0BRoe+wlNDwSLLuLfKl4yWNVGUl2Y4IOQfrHC6jEJGaKuClw6uwbTnoRroxhVdJhC4aP000LiiLpolPj7agIleok2K6vCdYA1ADUAFDvC0xxRoiSn32OFgHAMHTbaRvD6nAeALgo+p7NKcv2uNduVFyA4EDFxcPqnO23U7EDEqnJJgd5i6+4AMUB8IHy/b7KT+2KAWBLZW/rs9eW2zwOSZWJxx6SWsQxuTK8ee9jcpHnuf+lEiROzPiHi7R0f1fZoqjQmNc/RqIKOsGaaqqppppqqqmY/gXn8XqEJIcxXQAAAABJRU5ErkJggg==", "ages": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAE0ElEQVR42u2bzYscRRjGf93bO0lGV1FBUEnUBBN0VdCDePIg/gGCiIKih4DizYPgxZy8iCzBCGr0FjyJx9yMEogJCaJECChoFPwikaBx4m6M2zvdOcxb+lB272Z6e6p73C5opujprnrrqfe73oaudW1Dt6ilY11Jy9sAYNzAwn3Q46Z2LZJd6AFJ4MWvAMsFtAQBIAYyYCfwEvAQsNWIiAKwfgT8BBwBFoBvhKYgbB8DtwOnjaAmr9NGS7xecRgHAID3jIC/DfnQC89s7txooQoAVdl1Fvga2C7jXAysA/oi998DdwLpuIMkFRXfLHCzAHgRuNV+owmaKDd2H/jBfjFaZg2AseZParTDfxpLhmjDunyCOk1XYmYpBAckdRJdp3nKA3hpeZ3jx2zw1gEwpcFQ1AYdkJcQFgVY/LAuPbAeAGY8otK6FdQqbYtHezAzmEskdga4zVzSzeaOvgwsGiDZBMQ1B24E9gObjBNiC4zSKmAkFVlwGThlQUhm3PAs8MSEIzLnhfbEIZoBPq/iBa5XAd0PfGcTpsYVoQIhlwvIga+8mCSoFr4L+ESisxX71auOqE/HUqCPmBg2kZL7RwleBbwuRA29BQyBc8CSBUtLa1zumXMFY+niF0SEZ9rgRzwDnBVCHfEXgOdMaW0B5iyKK7rm7JlN9s4FAdFZmZ+Bx+vKCdadGN0JHPVY1y3gXQlfo1XEqm/PDuVd1z8E7JBdj2hRc+x4jS0gFwXpgDgK7PJSa5rK2uUBqL7F3jaw/DjO0dPAH0b8ssjvWRMX33P0Rchp+V+F5Vu9+KJc/QPAyZIdXTB73rN+Ecd8BtwjHBYxRc3t1LXAO94CXf8ju4r+e1N0RgLTH20+DwyEG4aeqXS7fh7Y/X8K2dVK7ABOCAArYjIz4Li518GO3ZKAeiGXXfZ1Rdm9iJYcgtYhAruNvfMSF9ndG5i4TL0IOCV4NbDPc2fLAFBXd7/5FFOnBCNZ/L1myorMYFbSVzN40kzp1JhBdVIeMyfGD5d/Y3SiPJBFD+ze+QJHaCCO01R4gZuBN8TMpdI/Aczbc0sCwJJwzBcCgnLMWxZ5tg4ENVfbgY9LWP6AOUUuXvABcPJ+A/CBJxIOwOMWcLUmGFIN/aTl5q6EhfsFAPRlZyPgReAvASGVWOKpBmuT/sPyfeC1EiV2CnjQi/7cO4vyzqK4vfrcw4yOvnNxnNw7+yw/2IhIaErsUAnLvw1c5xGoMf8lifUvebkCtSRbgQ9L5viU0bF8I/nA+0qSor8DL6ziyLjFHZaFHC6RaX33FZlDRexL/q1ViEMCcFBi/UyU1N1rpKvcvW02xkHrs8rzbs5HRSQyAeFAaC7oMarQ0Ezw+6LlkwnqnG1iaZwIfSv6IMju90VD54wyub0xFx9X8Pfd2Neb3ihSolGo0+FhwYlNVFC+Utaykv5ac7qCrJU6TGFc8xF1iNA1r9MJiqe0eLkrkekAaGFKLGLyFSJRm0pkKChfn3SFiBZoNA6Avwtzop1DlMrWUjRVtUQmBX4E7rDJXe0uDRRL50ZL0BKZFDjG6DBz2ZygPuG/GUrNAz0WskTGBSfztOeDifmq0WC0Tlm8BdgDPALcFPiTmTMWFL0K/FJ19zf8R1PdZ3Pdh5Nd69qGbpcB/EReDstuBT4AAAAASUVORK5CYII=", "pistes": "data:image/png;base64,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", "cjordan": "data:image/png;base64,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"};
  var NAV_ALL = [['arbre', 'Arbre', '#/arbre'], ['carte', 'Carte', '#/carte'], ['metiers', 'Métiers', '#/metiers'], ['ages', 'Âges', '#/ages'], ['pistes', 'À compléter', '#/pistes'], ['cjordan', 'C. Jordan 1917', '#/cjordan']];
  var PAGE_NAMES = {};
  NAV_ALL.forEach(function (n) { PAGE_NAMES[n[0]] = n[1]; });
  PAGE_NAMES.aide = 'Mode d’emploi';
  var CLEAR = !!window.__FT_CLEAR;       // version locale en clair (aucun mot de passe)
  var NEUTRAL = 'Arbre généalogique';
  var MODE = 'mdp';                  // 'mdp' : mot de passe saisi ; 'lien' : clé contenue dans le lien (#k=…), sans saisie
  var BASE = location.pathname.replace(/[^\/]*$/, '');   // dossier du site : stockages séparés entre sites du même domaine
  var SK = function (n) { return n + '@' + BASE; };
  var KEY = null;
  if (MODE === 'lien' && !CLEAR) {
    try {
      var hm = /(?:^#|&)k=([A-Za-z0-9]+)/.exec(location.hash);
      if (hm) {
        KEY = hm[1]; localStorage.setItem(SK('ft-k'), KEY);
        var rest = location.hash.replace(/^#k=[A-Za-z0-9]+&?/, '#').replace(/&k=[A-Za-z0-9]+/, '');
        history.replaceState(null, '', location.pathname + location.search + (rest === '#' ? '' : rest));   // la clé ne reste pas dans la barre d'adresse
      } else KEY = localStorage.getItem(SK('ft-k'));
    } catch (_) {}
  }
  var frame = null;                       // cadre de la page affichée (pages hors Arbre)
  var PROF = null;                        // profil actif : { id, nom, titre, pages, racines, ids }
  var css = [
    ':root{--ft-bg:#eef1ee;--ft-surface:#fbfcfb;--ft-fg:#1b2420;--ft-muted:#5b6a62;--ft-border:#d1dbd5;--ft-accent:#2c6d5b;--ft-soft:#d9eae3;--ft-warn:#8f5405;--ft-warnbg:#f6e8d0;--ft-hh:52px}',
    '@media (prefers-color-scheme:dark){:root{--ft-bg:#111715;--ft-surface:#1a221f;--ft-fg:#e5ece8;--ft-muted:#92a39a;--ft-border:#2c3833;--ft-accent:#6cc2a5;--ft-soft:#1d3a30;--ft-warn:#e2a54a;--ft-warnbg:#3a2c12}}',
    '.ft-hd.ft-wait{visibility:hidden}',
    '.ft-hd{position:fixed;top:0;left:0;right:0;z-index:30;display:flex;flex-wrap:wrap;align-items:center;gap:6px 18px;box-sizing:border-box;',
    'padding:calc(8px + env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) 8px max(16px,env(safe-area-inset-left,0px));',
    'background:var(--ft-surface);border-bottom:1px solid var(--ft-border);font:14px/1.3 "IBM Plex Sans",-apple-system,BlinkMacSystemFont,system-ui,sans-serif}',
    '.ft-t{font:600 19px/1.2 Literata,Georgia,serif;color:var(--ft-fg);text-decoration:none;text-wrap:balance}',
    '.ft-nav{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(max-content,1fr);gap:4px;margin-left:auto}',
    '.ft-nav a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:5px 8px 6px;border-radius:7px;text-decoration:none;color:var(--ft-muted);font-weight:500;font-size:13px;line-height:1.2;white-space:nowrap}',
    '.ft-ic{display:block;width:22px;height:22px;background-color:currentColor;-webkit-mask:var(--i) center/contain no-repeat;mask:var(--i) center/contain no-repeat}',
    '.ft-nav a[data-p="metiers"] .ft-ic{transform:translateY(.6px)}.ft-nav a[data-p="cjordan"] .ft-ic{transform:translateY(-1.1px)}',   /* centre optique des pictogrammes aligné sur celui de l'arbre (mesuré sur les pixels, 25/11/2026) */
    '.ft-lb::after{content:attr(data-t);display:block;height:0;overflow:hidden;visibility:hidden;font-weight:600}',   /* réserve la largeur du gras : le libellé actif ne change pas la largeur des colonnes */
    '.ft-nav a:hover{background:var(--ft-soft);color:var(--ft-accent)}',
    '.ft-nav a[aria-current="page"]{background:var(--ft-soft);color:var(--ft-accent);font-weight:600}',
    '.ft-hd a:focus-visible{outline:2px solid var(--ft-accent);outline-offset:2px}',
    '.ft-nav button.ft-ct{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:2px;padding:5px 8px 6px;border:0;border-radius:7px;background:none;color:var(--ft-muted);font-family:inherit;font-weight:500;font-size:13px;line-height:1.2;white-space:nowrap;cursor:pointer}',
    '.ft-nav button.ft-ct:hover{background:var(--ft-soft);color:var(--ft-accent)}',
    '.ft-nav button.ft-ct:focus-visible{outline:2px solid var(--ft-accent);outline-offset:2px}',
    '@media (max-width:560px){.ft-nav button.ft-ct{padding:5px 7px 6px}}',
    '#ft-ct{position:fixed;inset:0;z-index:110;display:grid;place-items:center;background:rgba(0,0,0,.45);padding:16px;font:14px/1.45 "IBM Plex Sans",-apple-system,system-ui,sans-serif}',
    '#ft-ct[hidden]{display:none}',
    '#ft-ct form{display:flex;flex-direction:column;gap:12px;width:min(480px,100%);max-height:calc(100vh - 32px);overflow:auto;box-sizing:border-box;background:var(--ft-surface);border:1px solid var(--ft-border);border-radius:12px;padding:20px;color:var(--ft-fg);box-shadow:0 8px 28px rgba(0,0,0,.25)}',
    '#ft-ct h2{margin:0;font:600 20px/1.25 Literata,Georgia,serif}',
    '#ft-ct p{margin:0;color:var(--ft-muted);font-size:13px}',
    '#ft-ct label{display:flex;flex-direction:column;gap:3px}',
    '#ft-ct label span{font:500 11px "IBM Plex Sans",system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ft-muted)}',
    '#ft-ct input,#ft-ct select,#ft-ct textarea{width:100%;box-sizing:border-box;font:inherit;padding:9px 10px;border:1px solid var(--ft-border);border-radius:6px;background:var(--ft-bg);color:var(--ft-fg)}',
    '#ft-ct textarea{min-height:130px;resize:vertical}',
    '#ft-ct input:focus-visible,#ft-ct select:focus-visible,#ft-ct textarea:focus-visible,#ft-ct button:focus-visible{outline:2px solid var(--ft-accent);outline-offset:2px}',
    '#ft-ct .ft-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}',
    '#ft-ct .ft-st{padding:7px 10px;border-radius:6px;font-size:12.5px}',
    '#ft-ct .ft-st.err{background:var(--ft-warnbg);color:var(--ft-warn)}',
    '#ft-ct .ft-st.ok{background:var(--ft-soft);color:var(--ft-accent)}',
    '#ft-ct .ft-bt{display:flex;gap:8px;justify-content:flex-end}',
    '#ft-ct button{font:500 13px "IBM Plex Sans",system-ui,sans-serif;padding:8px 14px;border-radius:7px;border:1px solid var(--ft-border);background:var(--ft-surface);color:var(--ft-fg);cursor:pointer}',
    '#ft-ct button[type=submit]{border-color:var(--ft-accent);background:var(--ft-accent);color:#fff}',
    '#ft-ct button[disabled]{opacity:.6;cursor:default}',
    '@media (max-width:560px){.ft-hd{gap:4px 12px}.ft-t{font-size:17px}.ft-nav{margin-left:0;width:100%;overflow-x:auto;grid-auto-columns:minmax(max-content,1fr)}.ft-nav{gap:2px}.ft-nav a{padding:5px 7px 6px}.ft-ic{width:20px;height:20px}}',
    'html.ft-app body{padding-top:calc(var(--ft-hh,52px) + 12px);padding-bottom:calc(var(--ft-fh,0px) + 8px)!important}',
    '.ft-ft{position:fixed;left:0;right:0;bottom:0;z-index:30;box-sizing:border-box;padding:4px max(16px,env(safe-area-inset-right,0px)) calc(4px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));background:var(--ft-surface);border-top:1px solid var(--ft-border);color:var(--ft-muted);font:12px/1.4 "IBM Plex Sans",-apple-system,system-ui,sans-serif;text-align:center}',
    'html.ft-shell,html.ft-shell body{margin:0;height:100%;background:var(--ft-bg)}',
    '.ft-fr{position:fixed;left:0;right:0;bottom:0;top:var(--ft-hh,52px);width:100%;height:calc(100% - var(--ft-hh,52px) - var(--ft-fh,0px));border:0;background:var(--ft-bg);visibility:hidden;pointer-events:none}',
    '.ft-fr.on{visibility:visible;pointer-events:auto}',
    '.ft-msg{position:fixed;left:0;right:0;top:var(--ft-hh,52px);bottom:0;display:grid;place-items:center;padding:24px;text-align:center;color:var(--ft-muted);font:14px system-ui,sans-serif}',
    '#ft-gate{position:fixed;inset:0;z-index:100;display:grid;place-items:center;background:var(--ft-bg);padding:16px;font:14px/1.45 "IBM Plex Sans",-apple-system,system-ui,sans-serif}',
    '#ft-gate form{display:flex;flex-direction:column;gap:12px;width:min(380px,100%);box-sizing:border-box;background:var(--ft-surface);border:1px solid var(--ft-border);border-radius:12px;padding:20px;color:var(--ft-fg);box-shadow:0 1px 2px rgba(20,40,30,.08),0 4px 14px rgba(20,40,30,.06)}',
    '#ft-gate h2{margin:0;font:600 20px/1.25 Literata,Georgia,serif}',
    '#ft-gate p{margin:0;color:var(--ft-muted);font-size:13px}',
    '#ft-gate label{display:flex;flex-direction:column;gap:3px}',
    '#ft-gate label span{font:500 11px "IBM Plex Sans",system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ft-muted)}',
    '#ft-gate input{width:100%;box-sizing:border-box;font:inherit;padding:9px 10px;border:1px solid var(--ft-border);border-radius:6px;background:var(--ft-bg);color:var(--ft-fg)}',
    '#ft-gate input:focus-visible,#ft-gate button:focus-visible{outline:2px solid var(--ft-accent);outline-offset:2px}',
    '#ft-gate .ft-err{padding:7px 10px;border-radius:6px;background:var(--ft-warnbg);color:var(--ft-warn);font-size:12.5px}',
    '#ft-gate button{align-self:flex-end;font:500 13px "IBM Plex Sans",system-ui,sans-serif;padding:8px 14px;border-radius:7px;border:1px solid var(--ft-accent);background:var(--ft-accent);color:#fff;cursor:pointer}',
    '#ft-gate button:disabled{opacity:.6;cursor:default}'
  ].join('\n');

  var fonts = document.createElement('link');
  fonts.rel = 'stylesheet';
  fonts.href = 'https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap';
  document.head.appendChild(fonts);
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);
  document.documentElement.classList.add('ft', 'ft-shell');

  var hd = document.createElement('header');
  hd.className = 'ft-hd';
  hd.innerHTML = '<a class="ft-t" href="index.html">🌳 <span id="ft-ti">' + NEUTRAL + '</span></a><nav class="ft-nav" id="ft-nv" aria-label="Pages"></nav>';
  document.body.insertBefore(hd, document.body.firstChild);
  function setH() { document.documentElement.style.setProperty('--ft-hh', hd.offsetHeight + 'px'); }
  /* Polices web : l'en-tête reste invisible (mais en place) jusqu'au chargement de Literata et d'IBM Plex Sans, au plus 900 ms, pour que le titre et le menu ne changent pas de largeur à chaque changement de page. */
  hd.classList.add('ft-wait');
  var shown = false;
  function showHd() { if (shown) return; shown = true; hd.classList.remove('ft-wait'); setH(); }
  setTimeout(showHd, 900);
  fonts.addEventListener('error', showHd);
  fonts.addEventListener('load', function () {
    if (!document.fonts || !document.fonts.load) return showHd();
    Promise.all([document.fonts.load('600 19px Literata'), document.fonts.load('500 13px "IBM Plex Sans"'), document.fonts.load('600 13px "IBM Plex Sans"')]).then(showHd, showHd);
  });
  setH();
  if (window.ResizeObserver) new ResizeObserver(setH).observe(hd);
  window.addEventListener('resize', setH);

    /* Contact : formulaire Netlify Forms (définition en clair dans contact-form.html, à la racine du site). Le message arrive dans le tableau de bord Netlify
     et par notification e-mail à l'adresse de l'auteur, qui n'apparaît nulle part dans les pages. Nom et e-mail du lecteur sont facultatifs. */
  var CT_ICON = 'data:image/png;base64,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';
  var ctBox = null, ctFrom = null;
  function openContact() {
    ctFrom = document.activeElement;
    if (!ctBox) {
      ctBox = document.createElement('div');
      ctBox.id = 'ft-ct'; ctBox.hidden = true;
      ctBox.innerHTML = '<form name="contact" method="POST" novalidate aria-labelledby="ft-ct-h">' +
        '<h2 id="ft-ct-h">Écrire à l’auteur du site</h2>' +
        '<p>Une question, un commentaire, une rectification à proposer ? Votre message n’est lisible que par l’auteur du site.</p>' +
        '<input type="hidden" name="form-name" value="contact"><input type="hidden" name="page"><input type="hidden" name="profil">' +
        '<label class="ft-hp" aria-hidden="true">Ne pas remplir<input name="bot-field" tabindex="-1" autocomplete="off"></label>' +
        '<label><span>Objet</span><select name="objet"><option>Question, commentaire</option><option>Rectification, précision</option><option>Suggestion d’amélioration</option><option>Autre</option></select></label>' +
        '<label><span>Message</span><textarea name="message" required maxlength="5000"></textarea></label>' +
        '<label><span>Votre nom (facultatif)</span><input name="nom" maxlength="120" autocomplete="name"></label>' +
        '<label><span>Votre e-mail (facultatif, pour recevoir une réponse)</span><input name="email" type="email" maxlength="200" autocomplete="email"></label>' +
        '<p>Ces informations sont conservées par l’hébergeur du site (Netlify) et ne servent qu’à vous répondre.</p>' +
        '<div class="ft-st" role="status" hidden></div>' +
        '<div class="ft-bt"><button type="button" class="ft-cx">Fermer</button><button type="submit">Envoyer</button></div></form>';
      document.body.appendChild(ctBox);
      var form = ctBox.querySelector('form'), st = ctBox.querySelector('.ft-st'), sb = form.querySelector('[type=submit]');
      var say = function (t, k) { st.hidden = !t; st.textContent = t || ''; st.className = 'ft-st ' + (k || ''); };
      var close = function () { ctBox.hidden = true; if (ctFrom && ctFrom.focus) ctFrom.focus(); };
      ctBox.querySelector('.ft-cx').addEventListener('click', close);
      ctBox.addEventListener('mousedown', function (e) { if (e.target === ctBox) close(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !ctBox.hidden) close(); });
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var m = form.elements.message.value.trim();
        if (!m) { say('Le message est vide.', 'err'); form.elements.message.focus(); return; }
        if (form.elements.email.value && !form.elements.email.checkValidity()) { say('Cette adresse e-mail ne semble pas valide.', 'err'); form.elements.email.focus(); return; }
        form.elements.page.value = (PAGE_NAMES[PAGE] || PAGE || '');
        form.elements.profil.value = (PROF && PROF.id) || '';
        sb.disabled = true; say('Envoi en cours…', '');
        fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
          .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); form.elements.message.value = ''; say('Message envoyé. Merci.', 'ok'); sb.hidden = true; ctBox.querySelector('.ft-cx').textContent = 'Fermer'; })
          .catch(function () { sb.disabled = false; say(CLEAR ? 'L’envoi ne fonctionne que sur le site en ligne, pas dans cette version locale.' : 'L’envoi a échoué. Vous pouvez réessayer plus tard.', 'err'); });
      });
    }
    var f = ctBox.querySelector('form'); ctBox.querySelector('.ft-st').hidden = true; ctBox.querySelector('[type=submit]').hidden = false; ctBox.querySelector('[type=submit]').disabled = false;
    ctBox.hidden = false; f.elements.message.focus();
  }

  /* Profil : titre, menu et pages accessibles dépendent du mot de passe saisi (ou, en local, du profil choisi). */
  function applyProfile(p) {
    PROF = p;
    document.getElementById('ft-ti').textContent = p.titre;
    document.getElementById('ft-nv').innerHTML = NAV_ALL.filter(function (n) { return p.pages.indexOf(n[0]) >= 0; }).map(function (n) {
      return '<a href="' + n[2] + '" data-p="' + n[0] + '"' + (n[0] === PAGE ? ' aria-current="page"' : '') + '><span class="ft-ic" aria-hidden="true" style="--i:url(' + ICONS[n[0]] + ')"></span><span class="ft-lb" data-t="' + n[1] + '">' + n[1] + '</span></a>';
    }).join('') + '<button type="button" class="ft-ct" aria-haspopup="dialog"><span class="ft-ic" aria-hidden="true" style="--i:url(' + CT_ICON + ')"></span>Contact</button>';
    document.getElementById('ft-nv').querySelector('.ft-ct').addEventListener('click', openContact);
    syncPage();
    setH();
    return p;
  }
  /* Page active : titre de l'onglet et entrée du menu. */
  function syncPage() {
    var p = PROF; if (!p) return;
    document.title = (PAGE && PAGE !== 'arbre' && PAGE_NAMES[PAGE] ? PAGE_NAMES[PAGE] + ' — ' : '') + p.titre;
    var nv = document.getElementById('ft-nv'); if (!nv) return;
    Array.prototype.forEach.call(nv.querySelectorAll('a[data-p]'), function (a) {
      if (a.dataset.p === PAGE) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
  }
  function clearProfile() {
    var P = window.__FT_PROFILS || {}, k = 'proches';
    try {
      var m = /[?&]profil=([a-z0-9-]+)/.exec(location.search);
      if (m && P[m[1]]) { k = m[1]; sessionStorage.setItem('ft-prof-local', k); }
      else { var q = sessionStorage.getItem('ft-prof-local'); if (q && P[q]) k = q; }
    } catch (_) {}
    return P[k] || { id: 'proches', nom: 'Arsène et Lazare', titre: "L'Arbre d'Arsène et Lazare", pages: NAV_ALL.map(function (n) { return n[0]; }), racines: null, ids: null };
  }

  var kc = {};
  function hex(u) { return Array.prototype.map.call(u, function (b) { return (b < 16 ? '0' : '') + b.toString(16); }).join(''); }
  async function dec(buf, pw) {
    var salt = buf.slice(0, 16), iv = buf.slice(16, 28), ct = buf.slice(28), id = pw + '|' + hex(salt);
    if (!kc[id]) kc[id] = crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey']).then(function (km) {
      return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: salt, iterations: ITER, hash: 'SHA-256' }, km, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
    });
    var key = await kc[id];
    var pt;
    try { pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: iv }, key, ct); } catch (x) { throw x; }
    return new Uint8Array(await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
  }

  /* Fichiers d'accès : acces-0.enc, acces-1.enc… (un par mot de passe). Celui que le mot de passe ouvre donne le profil et la clé des fichiers de contenu. */
  async function openKeyring(pw) {
    var found = 0;
    for (var i = 0; i < 8; i++) {
      var r;
      try { r = await fetch('acces-' + i + '.enc', { cache: 'no-cache' }); } catch (_) { break; }
      if (!r.ok) break;
      found++;
      var buf = new Uint8Array(await r.arrayBuffer());
      try { return JSON.parse(new TextDecoder().decode(await dec(buf, pw))); }
      catch (x) { if (!x || x.name !== 'OperationError') throw x; }
    }
    if (!found) throw new Error('fichiers d’accès introuvables');
    return null;
  }

  /* Accès par lien : la clé du lien ouvre acces-0.enc ; aucune saisie. Lien absent ou périmé : message, sans formulaire. */
  async function linkAccess() {
    var why = 'Ce lien est incomplet ou n’est plus valable. Ouvrez le lien complet qui vous a été transmis.';
    if (KEY) {
      try {
        var o = await openKeyring(KEY);
        if (o) { try { sessionStorage.setItem(SK('ft-pw'), o.m); sessionStorage.setItem(SK('ft-prof'), JSON.stringify(o.prof)); } catch (_) {} return o.prof; }
        try { localStorage.removeItem(SK('ft-k')); } catch (_) {}
      } catch (x) { why = 'Ouverture impossible dans ce navigateur (' + ((x && x.message) || x) + ').'; }
    }
    var g = document.createElement('div');
    g.id = 'ft-gate';
    g.innerHTML = '<form onsubmit="return false"><h2>' + NEUTRAL + '</h2><p class="ft-err">' + why + '</p></form>';
    document.body.appendChild(g);
    return new Promise(function () {});
  }

  function login() {
    if (MODE === 'lien') return linkAccess();
    return new Promise(function (resolve) {
      var g = document.createElement('div');
      g.id = 'ft-gate';
      g.innerHTML = '<form autocomplete="on"><h2>' + NEUTRAL + '</h2><p>Accès réservé à la famille. Saisissez votre mot de passe.</p>' +
        '<label for="ft-pw"><span>Mot de passe</span><input id="ft-pw" type="password" autocomplete="current-password"></label>' +
        '<p class="ft-err" hidden></p><button type="submit">Ouvrir</button></form>';
      document.body.appendChild(g);
      var f = g.querySelector('form'), inp = g.querySelector('input'), err = g.querySelector('.ft-err'), btn = g.querySelector('button');
      inp.focus();
      f.addEventListener('submit', async function (e) {
        e.preventDefault();
        if (!inp.value) return;
        btn.disabled = true; btn.textContent = 'Déchiffrement…'; err.hidden = true;
        try {
          var o = await openKeyring(inp.value);
          if (!o) throw Object.assign(new Error('mot de passe'), { name: 'OperationError' });
          try { sessionStorage.setItem(SK('ft-pw'), o.m); sessionStorage.setItem(SK('ft-prof'), JSON.stringify(o.prof)); } catch (_) {}
          g.remove();
          resolve(o.prof);
        } catch (x) {
          btn.disabled = false; btn.textContent = 'Ouvrir';
          err.textContent = (x && x.name === 'OperationError') ? 'Mot de passe incorrect.' : 'Ouverture impossible dans ce navigateur (' + ((x && x.message) || x) + ').';
          err.hidden = false;
        }
      });
    });
  }

  function start() {
    if (CLEAR) return Promise.resolve(clearProfile());
    try { var s = sessionStorage.getItem(SK('ft-prof')); if (s && sessionStorage.getItem(SK('ft-pw'))) return Promise.resolve(JSON.parse(s)); } catch (_) {}
    return login();
  }
  var ready = start().then(applyProfile);
  var relog = null;
  function again() {
    if (!relog) relog = login().then(applyProfile).then(function (p) { relog = null; return p; });
    return relog;
  }

  /* Charge un fichier chiffré avec la clé du profil ; une seule saisie du mot de passe pour toutes les pages de l'onglet. */
  async function load(file) {
    /* Version locale en clair : données déjà chargées par <fichier>.js. */
    if (window.__FT_CLEAR) {
      if (!window.__FT_CLEAR[file]) await new Promise(function (ok, ko) {
        var sc = document.createElement('script'); sc.src = file + '.js'; sc.onload = ok; sc.onerror = function () { ko(new Error('fichier introuvable : ' + file)); }; document.head.appendChild(sc);
      });
      var b = atob(window.__FT_CLEAR[file]), u = new Uint8Array(b.length);
      for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i);
      return u;
    }
    var r = await fetch(file, { cache: 'no-cache' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    var buf = new Uint8Array(await r.arrayBuffer());
    await ready;
    var pw = null;
    try { pw = sessionStorage.getItem(SK('ft-pw')); } catch (_) {}
    if (pw) {
      try { return await dec(buf, pw); }
      catch (x) { if (!x || x.name !== 'OperationError') throw x; try { sessionStorage.removeItem(SK('ft-pw')); sessionStorage.removeItem(SK('ft-prof')); } catch (_) {} }
    }
    await again();
    return dec(buf, sessionStorage.getItem(SK('ft-pw')));
  }

  /* Restreint la base au périmètre du profil (personnes, unions entre membres du périmètre, photos). */
  function restrict(D) {
    if (!PROF || !PROF.ids) return D;
    var s = {}, o = { people: {}, unions: {}, settings: D.settings || {}, photos: {}, wiki: {}, wikifam: {} }, k;
    PROF.ids.forEach(function (i) { s[i] = 1; });
    for (k in D.people) if (s[k]) o.people[k] = D.people[k];
    for (k in D.unions) { var u = D.unions[k]; if (s[u.a] && s[u.b]) o.unions[k] = u; }
    for (k in o.people) { var ph = o.people[k].photo; if (ph && D.photos && D.photos[ph]) o.photos[ph] = D.photos[ph]; }
    for (k in o.people) { if (D.wiki && D.wiki[k]) o.wiki[k] = D.wiki[k]; if (D.wikifam && D.wikifam[k]) o.wikifam[k] = D.wikifam[k]; }
    return o;
  }
  window.FT = { load: load, ready: ready, profil: function () { return PROF; }, restrict: restrict };

  /* Pont des planches du JMO (page C. Jordan 1917 uniquement) : la page isolée demande une planche, le parent la fournit. En version locale en clair, le fichier planche-N.enc.js n'est chargé qu'à la première demande. */
  function planche(id) {
    var n = 'planche-' + id + '.enc';
    if (!window.__FT_CLEAR || window.__FT_CLEAR[n]) return load(n);
    return new Promise(function (ok, ko) {
      var s = document.createElement('script');
      s.src = n + '.js'; s.onload = ok; s.onerror = ko;
      document.head.appendChild(s);
    }).then(function () { return load(n); });
  }
  window.addEventListener('message', function (ev) {
    var d = ev.data, f = frameOf(ev.source);
    if (!f || f._page !== PAGE_JMO || !d || d.type !== 'planche') return;
    var id = +d.id; if (!(id >= 1 && id <= 10)) return;
    ev.source.postMessage({ type: 'planche-ack', id: id }, '*');
    planche(id).then(function (b) {
      var buf = b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
      ev.source.postMessage({ type: 'planche-reponse', id: id, buf: buf }, '*', [buf]);
    }).catch(function () { ev.source.postMessage({ type: 'planche-reponse', id: id, buf: null }, '*'); });
  });

  /* Réglage mémorisable : objet plat de valeurs simples, de taille bornée. */
  function clean(o) {
    if (!o || typeof o !== 'object' || Array.isArray(o)) return null;
    var r = {}, n = 0;
    for (var k in o) {
      if (!Object.prototype.hasOwnProperty.call(o, k)) continue;
      var v = o[k], ty = typeof v;
      if (ty === 'string' ? v.length > (k === 'done' ? 40000 : 200) : (ty !== 'number' && ty !== 'boolean')) return null;
      if (++n > 20) return null;
      r[k] = v;
    }
    return r;
  }

  /* ===== Coque : routeur par fragment (#/page ou #/arbre/<fiche>) ; chaque page vit dans son cadre isolé, créé à la première visite puis conservé ===== */
  var frames = {}, loaded = {}, pending = {};
  var ROUTEOK = { aide: 1 };
  NAV_ALL.forEach(function (n) { ROUTEOK[n[0]] = 1; });
  function frameOf(src) { for (var k in frames) if (frames[k].contentWindow === src) return frames[k]; return null; }
  function msgBox(t) { var m = document.createElement('div'); m.className = 'ft-msg'; m.textContent = t; document.body.appendChild(m); return m; }
  function clearMsgs() { Array.prototype.forEach.call(document.querySelectorAll('.ft-msg'), function (m) { m.remove(); }); }
  function esc(o) { return JSON.stringify(o).replace(/</g, '\\u003c'); }
  function dataText(p) {
    return load('data.enc').then(function (b) {
      var t = new TextDecoder().decode(b);
      if (p.ids && !p.pre) t = JSON.stringify(restrict(JSON.parse(t)));
      return t;
    });
  }
  /* Active le cadre de la page courante (une fois chargé) ; les autres restent en mémoire, masqués. */
  function activate() {
    if (!frames[PAGE] || !loaded[PAGE]) return;
    clearMsgs();
    for (var k in frames) frames[k].classList.toggle('on', k === PAGE);
    frame = frames[PAGE];
    try { frame.contentWindow.postMessage({ ft: 'show' }, '*'); } catch (_) {}
  }
  function mount(page, arg, p) {
    if (frames[page]) return Promise.resolve(false);
    if (pending[page]) return pending[page];
    var file = page + '.enc';
    pending[page] = Promise.all([load(file), page === 'arbre' ? dataText(p) : Promise.resolve(null)]).then(function (r) {
      var f = document.createElement('iframe');
      f.className = 'ft-fr'; f._page = page;
      f.setAttribute('sandbox', 'allow-scripts allow-popups allow-popups-to-escape-sandbox');
      f.title = PAGE_NAMES[page] || page;
      /* Passerelle avec la page isolée : profil, données de l'arbre, réglages mémorisés (localStorage de la coque), ouverture d'une fiche, changement de page. */
      var saved = null;
      try { saved = clean(JSON.parse(localStorage.getItem('ft-state-' + page + '-' + p.id))); } catch (_) {}
      var pf = p.ids ? { id: p.id, nom: p.nom, titre: p.titre, racines: p.racines, ids: p.ids, pre: !!p.pre } : null;
      var boot = '<script>window.__FT_STATE=' + esc(saved) + ';window.__FT_PROFIL=' + esc(pf) + (arg ? ';window.__FT_DL=' + esc(arg) : '') + (r[1] != null ? ';window.__FT_DATA=' + esc(r[1]) : '') +
        ';window.FT={ready:Promise.resolve(window.__FT_PROFIL),profil:function(){return window.__FT_PROFIL},load:function(){return Promise.resolve(window.__FT_DATA!=null?new TextEncoder().encode(window.__FT_DATA):null)},restrict:function(D){return D}}' +
        ';window.FTSAVE=function(s){try{parent.postMessage({ft:"save",state:s},"*")}catch(e){}}' +
        ';window.FTOPEN=function(id){try{parent.postMessage({ft:"open",id:id},"*")}catch(e){}}' +
        ';window.FTGO=function(to){try{parent.postMessage({ft:"go",to:to},"*")}catch(e){}}' +
        ';addEventListener("message",function(e){if(e.source===parent&&e.data&&e.data.ft==="show")dispatchEvent(new Event("resize"))});<\/script>';
      f.srcdoc = new TextDecoder().decode(r[0]).replace(/<head[^>]*>/i, function (m) { return m + boot; });
      frames[page] = f;
      f.addEventListener('load', function () { loaded[page] = true; if (PAGE === page) activate(); });
      document.body.appendChild(f);
      return true;
    });
    pending[page].catch(function () { delete pending[page]; });
    return pending[page];
  }
  function show(page, arg) {
    PAGE = page; syncPage(); clearMsgs();
    return ready.then(function (p) {
      if (page !== 'aide' && p.pages.indexOf(page) < 0) {
        for (var k in frames) frames[k].classList.remove('on');
        msgBox('Cette page n’est pas disponible avec votre accès.'); return;
      }
      return mount(page, arg, p).then(function (fresh) {
        if (PAGE !== page) return;
        if (!fresh && arg && page === 'arbre') { try { frames.arbre.contentWindow.postMessage({ ft: 'locate', id: arg }, '*'); } catch (_) {} }
        activate();
      });
    }).catch(function (e) { msgBox('Chargement impossible (' + ((e && e.message) || e) + '). Rechargez la page.'); });
  }
  function route() {
    var m = /^#\/([a-z0-9]+)(?:\/([A-Za-z0-9._%-]{1,200}))?/.exec(location.hash);
    var pg = m && ROUTEOK[m[1]] ? m[1] : 'arbre', arg = null;
    if (m && m[2]) { try { arg = decodeURIComponent(m[2]); } catch (_) {} if (!/^[A-Za-z0-9._-]{1,120}$/.test(arg || '')) arg = null; }
    if (pg === 'arbre' && arg) { show('arbre', arg); try { history.replaceState(history.state, '', '#/arbre'); } catch (_) {} }
    else show(pg, null);
  }
  function go(h) { if (location.hash === h) route(); else location.hash = h; }
  window.addEventListener('message', function (ev) {
    var f = frameOf(ev.source);
    if (!f || !ev.data || typeof ev.data !== 'object') return;
    if (ev.data.ft === 'save') {
      var s = clean(ev.data.state);
      if (s && PROF) { try { localStorage.setItem('ft-state-' + f._page + '-' + PROF.id, JSON.stringify(s)); } catch (_) {} }
    } else if (ev.data.ft === 'open' && typeof ev.data.id === 'string' && /^[A-Za-z0-9._-]{1,120}$/.test(ev.data.id)) {
      go('#/arbre/' + encodeURIComponent(ev.data.id));
    } else if (ev.data.ft === 'go' && typeof ev.data.to === 'string' && ROUTEOK[ev.data.to]) {
      go('#/' + ev.data.to);
    }
  });
  window.addEventListener('hashchange', route);
  ready.then(route);
})();
