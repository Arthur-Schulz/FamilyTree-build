"""Reconstitue le zip : fichiers de <w>/zip, remplacés par les pages de <w>/out/*.html et <w>/bundle.json.
usage : python3 -I tools/pack.py <dossier de travail> <zip de sortie>"""
import sys,os,base64,zipfile
w,out=sys.argv[1],sys.argv[2]
def enc(name,raw): open(f'{w}/zip/{name}.enc.js','w',encoding='ascii').write('(window.__FT_CLEAR=window.__FT_CLEAR||{})["%s.enc"]="%s";\n'%(name,base64.b64encode(raw).decode()))
for f in sorted(os.listdir(w+'/out')):
    if f.endswith('.html'): enc(f[:-5],open(f'{w}/out/{f}','rb').read())
if os.environ.get('PACK_DATA')=='1': enc('data',open(w+'/bundle.json','rb').read())
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(os.listdir(w+'/zip')): z.write(f'{w}/zip/{f}',f)
print('zip',out,os.path.getsize(out))
