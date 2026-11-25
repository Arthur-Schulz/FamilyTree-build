#!/bin/sh
# Régénère Âges et Carte à partir d'un zip local existant. Usage : ./build.sh <arbre_local.zip> <sortie.zip> [dossier de travail]
# Aucun mot de passe. Le dossier de travail contient des données en clair : hors dépôt (/tmp par défaut).
set -e
IN="$1"; OUT="$2"; W="${3:-/tmp/ft-build}"
[ -n "$IN" ] && [ -n "$OUT" ] || { echo "usage: $0 <arbre_local.zip> <sortie.zip> [dossier]"; exit 1; }
cd "$(dirname "$0")"
rm -rf "$W"; mkdir -p "$W/out"
python3 -I tools/unpack.py "$IN" "$W"
export BUNDLE="$W/bundle.json" BUNDLE_REF="$W/bundle.json"
python3 -I src/rebuild_ages.py  "$W/pages/ages.html"  "$W/out/ages.html"
python3 -I src/rebuild_carte.py "$W/pages/carte.html" "$W/out/carte.html"
python3 -I src/check_moves.py   "$W/out/carte.html"
python3 -I tools/pack.py "$W" "$OUT"
