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

## Site par périmètres (reconstruit le 26/11/2026)
Quatre accès : **proches** (racine du site, mot de passe, tout l'arbre) et trois **liens à clé** (`schulz` = Henri Schulz-Robellaz + Corinne Denis ; `bonhomme` = Jean-Claude Bonhomme + Brigitte Masson ; `lefranc` = Jean-Daniel Le Franc + Jackie Patry). Un périmètre = ascendants des deux racines ; périmètres deux à deux disjoints (contrôlé à chaque construction) ; recalculés d'après les données courantes (26/11 : 549 / 1 067 / 939). Définition : `profils.json` (racines, pages, dossiers, variables d'environnement). Conception détaillée : `claude/site-par-perimetres.md` (projet « Généalogie »).
- `tools/build_profiles.py enc <travail> <sortie>` : construit le site chiffré (racine + un dossier `<dossier>-<jeton12>/` par lien). `PW_PROCHES` (mot de passe, jamais enregistré, obligatoire). Liens : `LIEN_SCHULZ`, `LIEN_BONHOMME`, `LIEN_LEFRANC` = `<jeton12>/<clé20>` si fournis ; sinon repris de **`liens.enc`** (liens déjà diffusés, scellés avec `PW_PROCHES`) ; sinon tirés au hasard. `PERSIST_LIENS=1` écrit `liens.enc` : une mise à jour du site conserve donc les liens diffusés tant que le mot de passe ne change pas ; pour de nouveaux liens, retirer `liens.enc`. Lien d'accès : `https://<site>/<dossier>-<jeton>/index.html#k=<clé>`.
- `tools/build_profiles.py local-profils <travail>` : réécrit `profils.js` du zip local (appelé par `build.sh`) ; échoue si un identifiant disparaît d'un périmètre.
- `build.sh` avec `ENC_OUT=<dossier>` construit aussi le site chiffré.
- Chiffrement : PBKDF2-SHA256 600 000 itérations + AES-256-GCM + gzip ; fichier = sel16 + iv12 + chiffré ; clé maître aléatoire par dossier ; `acces-0.enc` = `{m, prof}` scellé par le mot de passe (racine) ou la clé du lien (dossiers). Coque : `src/shell/common.js` (copie de celle du zip ; ne contient aucune donnée).
- Dossiers de liens : pages **pré-filtrées à la construction** (blocs `/*PT:BEGIN*/…/*PT:END*/` exécutés avec node), Métiers réduit à `D.profiles[id]`, données (`data.enc`) restreintes au périmètre, note « Exception » de la Carte retirée hors périmètre, aucune relocalisation partielle (contrôle). Page C. Jordan 1917 et planches : proches et schulz seulement. « À compléter » : version locale seulement.
- **Règle de confidentialité** : le prénom du propriétaire (et celui de sa conjointe) n'apparaît dans aucune note ni dans le code des dossiers de périmètre. `tools/patch_jordan_neutre.py` neutralise le texte de la page C. Jordan 1917 (appelé par `build.sh`) ; `SCRUB` de `build_profiles.py` remplace les libellés « Arthur… / Constance… » du code de Carte, Âges, Métiers, Aide, Arbre ; `NOTES_SUBST` neutralise une formule des notes de fiches (la base n'est pas modifiée). Toute mention résiduelle fait échouer la construction.
- Tests (secrets de test, jamais ceux de production) : `tools/test_fuites.py <site> <travail>` (déchiffre chaque dossier, aucun identifiant hors périmètre, aucune mention interdite, clés croisées refusées) ; `tools/test_navigateur.py <site>` (Playwright : mot de passe, trois liens sans saisie, fragment retiré, réouverture, lien sans clé / clé fausse, pages, relocalisations 25 / 16 / 6 / 3 au 26/11, Jordan bloqué hors schulz, texte visible sans mention interdite).
- Déploiement : jamais sans accord explicite d'Arthur ; ce dépôt ne publie rien (le dépôt `FamilyTree` / Netlify est séparé).

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

## Carte : lignées des relocalisations (26/11/2026)
8 lignées (couleurs `--c1`…`--c8`) : Schulz, Denis, Jordan, Hachette, Masson, Le Franc, Jacquey, Bonhomme (racine `joseph-bonhomme`). `IDX`/`BN` dans `src/rebuild_moves.py` ; `tools/patch_carte_bonhomme.py` (appelé par `build.sh`) ajoute la couleur, la légende, la ligne de la frise et le motif hachuré au gabarit. Un groupe conservé sans lignée reçoit ses lignées au recalcul.
