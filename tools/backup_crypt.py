"""Chiffre / déchiffre une sauvegarde JSON de l'arbre (bouton « Sauvegarde » de l'artifact).
Schéma identique à celui du site : PBKDF2-SHA256 (600 000 itérations), AES-256-GCM, données compressées gzip.
Format du fichier : b'FTB1' + sel (16) + nonce (12) + texte chiffré. Le mot de passe n'est jamais stocké : variable d'environnement TREE_PASSWORD.
usage : TREE_PASSWORD=... python3 -I tools/backup_crypt.py enc <sauvegarde.json> <sortie.enc>
        TREE_PASSWORD=... python3 -I tools/backup_crypt.py dec <entree.enc> <sortie.json>"""
import sys,os,gzip
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
M=b'FTB1'
def key(pw,salt): return PBKDF2HMAC(hashes.SHA256(),32,salt,600000).derive(pw.encode('utf-8'))
mode,src,dst=sys.argv[1:4]; pw=os.environ['TREE_PASSWORD']
raw=open(src,'rb').read()
if mode=='enc':
    salt,nonce=os.urandom(16),os.urandom(12)
    open(dst,'wb').write(M+salt+nonce+AESGCM(key(pw,salt)).encrypt(nonce,gzip.compress(raw,9),M))
else:
    assert raw[:4]==M,'format inconnu'
    open(dst,'wb').write(gzip.decompress(AESGCM(key(pw,raw[4:20])).decrypt(raw[20:32],raw[32:],M)))
print(mode,'ok',os.path.getsize(dst))
