#!/bin/sh
# Régénère Âges, Carte et Métiers à partir d'un zip local existant. Usage : ./build.sh <arbre_local.zip> <sortie.zip> [dossier de travail] [export.json] [artifact_index.html]
# Sans export : les données du zip sont reprises. Avec export (bouton « Sauvegarde ») : people et unions sont remplacés avant le calcul et écrits dans le zip (data.enc.js).
# Aucun mot de passe. Le dossier de travail contient des données en clair : hors dépôt (/tmp par défaut).
set -e
IN="$1"; OUT="$2"; W="${3:-/tmp/ft-build}"; EXPORT="$4"; ARBRE="$5"
[ -n "$IN" ] && [ -n "$OUT" ] || { echo "usage: $0 <arbre_local.zip> <sortie.zip> [dossier] [export.json]"; exit 1; }
cd "$(dirname "$0")"
rm -rf "$W"; mkdir -p "$W/out"
python3 -I tools/unpack.py "$IN" "$W"
cp "$W/bundle.json" "$W/bundle_ref.json"   # snapshot de la page d'origine (correspondance libellé de lieu -> lieu de la carte)
if [ -n "$EXPORT" ]; then python3 -I tools/merge_export.py "$EXPORT" "$W/bundle.json"; export PACK_DATA=1; fi
export BUNDLE="$W/bundle.json" BUNDLE_REF="$W/bundle_ref.json"
python3 -I src/rebuild_ages.py  "$W/pages/ages.html"  "$W/out/ages.html"
python3 -I src/rebuild_carte.py "$W/pages/carte.html" "$W/out/carte.html"
python3 -I src/rebuild_moves.py "$W/out/carte.html"   # liste des relocalisations (rayon 10 km, variable MOVES_RADIUS)
python3 -I src/rebuild_metiers.py "$W/bundle.json" "$W/pages/metiers.html" "$W/out/metiers.html"
[ -n "$ARBRE" ] && python3 -I src/rebuild_arbre.py "$ARBRE" "$W/pages/arbre.html" "$W/out/arbre.html"   # page Arbre = artifact (version courante) + adaptations zip
python3 -I src/check_moves.py   "$W/out/carte.html"
python3 -I tools/pack.py "$W" "$OUT"
