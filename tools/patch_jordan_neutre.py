"""Page C. Jordan 1917 : texte sans mention du propriétaire de l'arbre (règle « le prénom d'Arthur n'apparaît dans aucune page »).
Idempotent : une page déjà neutre est recopiée telle quelle. Échoue si l'ancre n'est ni l'ancien texte ni le nouveau.
usage : python3 -I tools/patch_jordan_neutre.py <cjordan.html entrée> <cjordan.html sortie>"""
import sys
src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()
OLD1 = 'est l’<b>arrière-arrière-grand-père d’Arthur</b> : il est le père de <b>Marie-Thérèse Jordan</b> (1897-1959), elle-même mère de <b>Corinne Denis</b>, grand-mère paternelle d’Arthur.'
NEW1 = 'est le père de <b>Marie-Thérèse Jordan</b> (1897-1959), elle-même mère de <b>Corinne Denis</b>.'
if OLD1 in t:
    assert t.count(OLD1) == 1
    t = t.replace(OLD1, NEW1)
else:
    assert NEW1 in t, 'ancre de la phrase d\'ouverture introuvable'
assert 'Arthur' not in t, 'mention résiduelle'
open(dst, 'w', encoding='utf-8').write(t)
print('jordan neutre ok')
