# FamilyTree-build — générateurs de la version locale

Dépôt privé, **séparé du dépôt publié sur Netlify** (`FamilyTree`). Il ne contient ni donnée de l'arbre, ni page en clair, ni mot de passe (voir `.gitignore`).

## Usage
```
./build.sh <arbre_local.zip> <sortie.zip> [dossier de travail]
```
Le zip d'entrée sert à la fois de source de données (`data.enc.js`) et de gabarit pour les pages. Âges et Carte sont recalculés à partir de ces données ; les autres fichiers sont repris tels quels. Le dossier de travail (`/tmp/ft-build` par défaut) contient des données en clair : ne pas le placer dans le dépôt.

## Contenu
- `src/model.py` : chargement des données (`BUNDLE=...json`).
- `src/ages_gen.py`, `src/rebuild_ages.py` : page Âges.
- `src/rebuild_carte.py` : page Carte (nouveaux lieux avec coordonnées sourcées, rattachements de libellés, événements, branches, poids).
- `src/check_moves.py` : contrôle des relocalisations (règle de stats2).
- `tools/unpack.py`, `tools/pack.py` : décodage et reconstitution du zip.

## Limites
- **Métiers n'est pas régénéré** : le générateur d'origine (classification des métiers, poids fractionnaires) est perdu. La page du zip d'entrée est reprise telle quelle.
- La Carte conserve les relocalisations de la page d'entrée ; `check_moves.py` signale seulement les écarts avec la règle (26 éligibles contre 27 le 25/11/2026, cas d'Ami Merle d'Aubigné après le changement de lieu de naissance).
- Pour intégrer de nouvelles données, il faut d'abord les mettre dans le `data.enc.js` du zip d'entrée ; `build.sh` ne lit pas la base de l'artefact.
- Testé le 25/11/2026 sur le zip du jour : la page Âges est régénérée à l'identique ; la page Carte l'est à l'ordre près de la liste des lieux non localisés ; le contenu est identique.
- Reconstruit après une perte d'environnement ; les sources d'origine n'existent plus. Voir aussi `claude/sources-generateurs-2026-11-25.md` dans le projet Claude « Généalogie ».
