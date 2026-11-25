"""Décode un zip local (arbre_local.zip) : pages en clair -> <w>/pages/*.html, données -> <w>/bundle.json.
usage : python3 -I tools/unpack.py <arbre_local.zip> <dossier de travail>
Les fichiers produits contiennent des données personnelles en clair : ne jamais les commiter (voir .gitignore)."""
import sys,os,re,zipfile,base64
z,w=sys.argv[1],sys.argv[2]
os.makedirs(w+'/pages',exist_ok=True); os.makedirs(w+'/zip',exist_ok=True)
rx=re.compile(r'="([A-Za-z0-9+/=]+)";')
with zipfile.ZipFile(z) as f:
    f.extractall(w+'/zip')
    for n in f.namelist():
        if n.endswith('.enc.js'):
            raw=base64.b64decode(rx.search(f.read(n).decode('ascii')).group(1))
            name=n[:-len('.enc.js')]
            if name=='data': open(w+'/bundle.json','wb').write(raw)
            elif name.startswith('planche-'): continue
            else: open(f'{w}/pages/{name}.html','wb').write(raw)
print('ok',sorted(os.listdir(w+'/pages')))
