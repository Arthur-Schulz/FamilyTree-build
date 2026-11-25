# FamilyTree-build — générateurs de la version locale

Dépôt privé, **séparé du dépôt publié sur Netlify** (`FamilyTree`). Il ne contient ni page en clair, ni donnée de l'arbre en clair, ni mot de passe (voir `.gitignore`, qui exclut aussi tout `*.json`). Les seules données de l'arbre sont des sauvegardes **chiffrées** dans `backups/`.

## Usage
```
./build.sh <arbre_local.zip> <sortie.zip> [dossier de travail] [export.json] [artifact_index.html]
```
Le zip d'entrée sert de gabarit pour les pages (et de source de données sans export). Avec `export.json` (bouton « Sauvegarde » de l'artifact), `people` et `unions` du zip sont remplacés par l'export (`tools/merge_export.py`) et écrits dans le zip ; photos, wiki et le reste sont conservés. Âges, Carte et Métiers sont recalculés ; les autres fichiers sont repris tels quels (la page Arbre du zip n'est pas régénérée : elle lit ses données dans `data.enc.js`). Le dossier de travail (`/tmp/ft-build` par défaut) contient des données en clair : ne pas le placer dans le dépôt.

## Contenu
- `src/model.py` : chargement des données (`BUNDLE=...json`).
- `src/ages_gen.py`, `src/rebuild_ages.py` : page Âges.
- `src/rebuild_carte.py` : page Carte (nouveaux lieux avec coordonnées sourcées, rattachements de libellés, événements, branches, poids).
- `src/rebuild_arbre.py` : page Arbre du zip = HTML de l'artifact (copie courante, 5e argument de `build.sh`) + adaptations « zip » (lecture seule, données de `data.enc.js`, coque) ; échoue si une ancre n'est plus unique.
- `src/rebuild_metiers.py`, `src/metiers_gen.py`, `src/canon.py` : page Métiers (reconstruits le 25/11/2026, voir ci-dessous).
- `src/check_moves.py` : contrôle des relocalisations (règle de stats2).
- `tools/unpack.py`, `tools/pack.py` : décodage et reconstitution du zip ; `tools/merge_export.py` : fusion d'un export dans le jeu de données.

## Limites
- **Métiers (reconstruit le 25/11/2026)** : `metiers_gen.py` calcule les vues (générations minimales, groupes G1–4 … G11–12, poids 1/n entre les familles reconnues par mots-clés sur l'intitulé entier, siècles `cc`/`ny`) ; `canon.py` donne, pour chaque intitulé brut, les métiers listés par famille (fenêtres « i »). `LEARNED` (241 intitulés) a été relevée sur la page du 23/11/2026 ; `NEW` = intitulés ajoutés depuis, à faire valider par Arthur. Un intitulé absent de la table fait échouer la construction (ajouter une entrée dans `NEW`). Les règles de mots-clés sont une reconstruction : validées en rejouant la page du 23/11 (vues Arthur, Constance, toutes branches, 48 branches et 3 profils identiques aux données près, une fois neutralisés les métiers ajoutés depuis ; ordre des listes, index `nm` et siècles compris). Les branches (noms, structure) et les textes viennent de la page d'entrée.
- La Carte conserve les relocalisations de la page d'entrée ; `check_moves.py` signale seulement les écarts avec la règle (26 éligibles contre 27 le 25/11/2026, cas d'Ami Merle d'Aubigné après le changement de lieu de naissance).
- Pour intégrer de nouvelles données, il faut d'abord les mettre dans le `data.enc.js` du zip d'entrée ; `build.sh` ne lit pas la base de l'artefact.
- Testé le 25/11/2026 sur le zip du jour : la page Âges est régénérée à l'identique ; la page Carte l'est à l'ordre près de la liste des lieux non localisés ; le contenu est identique.
- Reconstruit après une perte d'environnement ; les sources d'origine n'existent plus. Voir aussi `claude/sources-generateurs-2026-11-25.md` dans le projet Claude « Généalogie ».

## Sauvegardes de la base (`backups/`)
- `backups/arbre-AAAA-MM-JJ.enc` : export du bouton « Sauvegarde » de l'artifact (format `arbre-genealogique`), chiffré. Première sauvegarde : 25/11/2026 (2547 personnes, 1186 unions).
- Chiffrement : PBKDF2-SHA256 (600 000 itérations), AES-256-GCM, gzip ; fichier = `FTB1` + sel + nonce + texte chiffré. Le mot de passe n'est stocké nulle part : sans lui, le fichier est irrécupérable.
- `TREE_PASSWORD=... python3 -I tools/backup_crypt.py enc <sauvegarde.json> backups/arbre-AAAA-MM-JJ.enc`
- `TREE_PASSWORD=... python3 -I tools/backup_crypt.py dec backups/arbre-AAAA-MM-JJ.enc <sortie.json>`
