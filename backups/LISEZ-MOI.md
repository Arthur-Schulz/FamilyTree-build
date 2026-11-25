# Déchiffrer une sauvegarde de la base

Les fichiers `arbre-AAAA-MM-JJ.enc` sont des exports du bouton « Sauvegarde » de l'artifact « L'Arbre d'Arsène et Lazare » (format `arbre-genealogique`, clés `people` et `unions`), chiffrés. Le mot de passe n'est stocké nulle part : sans lui, le fichier est irrécupérable (c'est voulu). C'est le mot de passe commun du site.

## Procédure
1. Récupérer le dépôt privé : `git clone https://github.com/Arthur-Schulz/FamilyTree-build`
2. Installer la bibliothèque : `pip install cryptography`
3. Depuis le dossier du dépôt :
   ```
   TREE_PASSWORD='mot de passe' python3 -I tools/backup_crypt.py dec backups/arbre-AAAA-MM-JJ.enc arbre-restaure.json
   ```
4. `arbre-restaure.json` est identique à l'export d'origine. Ne pas le commiter (`*.json` est exclu par `.gitignore`).

Sous Windows, la syntaxe `TREE_PASSWORD='…' commande` ne fonctionne pas : définir avant la commande `set TREE_PASSWORD=…` (cmd) ou `$env:TREE_PASSWORD='…'` (PowerShell).

## Chiffrer une nouvelle sauvegarde
`TREE_PASSWORD='mot de passe' python3 -I tools/backup_crypt.py enc <export.json> backups/arbre-AAAA-MM-JJ.enc`

## Format (si `tools/backup_crypt.py` est indisponible)
Fichier = `FTB1` (4 octets) + sel (16 octets) + nonce (12 octets) + texte chiffré.
- Clé : PBKDF2-HMAC-SHA256, 600 000 itérations, 32 octets, sur le mot de passe en UTF-8 et le sel.
- Chiffrement : AES-256-GCM, nonce ci-dessus, données authentifiées additionnelles = `FTB1`.
- Contenu en clair : le JSON compressé en gzip.

## Limites
- Le réimport dans l'artifact n'a pas été vérifié : essayer d'abord sur une copie.
- Un test de déchiffrement a été fait le 25/11/2026 (résultat identique octet pour octet à l'export). Refaire un essai chez soi pour s'assurer que le mot de passe et la procédure fonctionnent.
