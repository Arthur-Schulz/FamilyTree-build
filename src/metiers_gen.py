"""Métiers : calcul des vues (reconstruction du générateur d'origine, 25/11/2026).
Entrées : people (dict id -> fiche) et la page Métiers précédente (gabarit : textes, branches, séries).
Règles (documentées dans claude/a-faire-differe.md et claude/profils-mot-de-passe.md) :
 - génération minimale depuis la racine (implexe compté une fois, à sa génération la plus proche) ;
 - groupes G1–4, G5–6, G7–8, G9–10, G11–12 ; au-delà de G12 : compté dans `beyond` ;
 - un ancêtre pèse 1 au total, réparti à parts égales entre les familles reconnues par les mots-clés de l'intitulé entier ;
 - `cc` / `ny` : siècles (année moyenne naissance-décès) des ancêtres datés du groupe."""
import re, collections
BANDS = [(1, 4), (5, 6), (7, 8), (9, 10), (11, 12)]
N = 14
R = [
 # 0 Négoce et commerce
 r"marchand(?!s\b)|négociant|commerçant|commerce de|libraire|colporteur|voiturier|armateur|maison de commissions|commissions et de poste|publicitaire|directeur commercial|épicier|mercier|charretier",
 # 1 Offices et fonctions publiques
 r"maire|consul|bailli(?!age)|banneret|bourgmestre|percepteur|prévôté|secrétaire du roi|auditeur au conseil|maître d(es|e la) postes?|inspecteur général des ponts|documentaliste|sénateur|intendant|fonction publique|patriote|diplomate|juge consulaire|prévôt des marchands|co-seigneur",
 # 2 Sciences et industrie
 r"ingénieur|chimiste|industriel|mathématicien|mécanicien|manufacturier|fabricant d.amidon|directeur des (chantiers|salins)|forges|fondé de pouvoir|chef de traction|géomètre|amidonnier|papetier|usine",
 # 3 Droit et justice
 r"avocat|notaire|procureur|greffier|juge |praticien|conseiller au grand conseil",
 # 4 Armée et intendance
 r"capitaine|grenadier|général de brigade|commissaire (aux vivres|des poudres|principal d.artillerie|d.artillerie)|artillerie|officier(?! de santé)|chimiste, officier|écuyer(?!, seigneur)|maréchal de camp|chef d.escadron",
 # 5 Banque et finance
 r"banquier|agent de change|fondé de pouvoir",
 # 6 Lettres, arts, enseignement
 r"[eé]diteur|libraire|relieur|graveur|professeur|écrivain|poète|historien|sculpt|figuriste|dessinat|artiste|graphiste|violoncelliste|pasteur, professeur|ingénieur des arts et manufactures, éditeur",
 # 7 Terre et agriculture
 r"laboureu|cultivat|fermier|planteur|bouilleur|meunier|jardinier|légumi|granger",
 # 8 Textile, cuir et habillement
 r"tisseu|tisser|tisserand|fileu|dévideu|couturi|cordonnier|bonnetier|bas au métier|draps|soie|lacets|dentelles|étoffes|sellier|blanchisseu|ouvrière aux cotons|fabricant de soieries|vêtement",
 # 9 Métaux et bâtiment
 r"forgeron|menuisier|cloutier|coutelier|serrurier|serrurière|maçon|charpentier|architecte|maréchal(?! de camp)|potier d.étain|armurier|arquebusier|charron|vrilles|alaines|quincaill|entrepreneur en bâtiment|clous|ouvrier de boutons",
 # 10 Alimentation et hôtellerie
 r"boulanger|pâtissier|aubergiste|hostelier|h[oô]telier|\bvins\b|amidonnier",
 # 11 Joaillerie, horlogerie
 r"bijoutier|joaillier|orfèvre|horloger|cadraturier|uhrmacher",
 # 12 Santé
 r"médecin|chirurgien|officier de santé|pharmacien",
 # 13 Autres
 r"pasteur|prêtre|\bcuré\b|\babbé\b|abbesse|vicaire|chanoine|évêque|archevêque|\bpape\b|moine|moniale|religieu(x|se)|aumônier|diacre|chapelain|prieur|clergé|domestique|servante|ménagère|employé|\bsieur\b|écuyer(?!, seigneur)|banneret|noble|baronne",
]
import unicodedata
def unacc(t): return ''.join(c for c in unicodedata.normalize('NFD', t) if not unicodedata.combining(c))
CR = [re.compile(unacc(r), re.I) for r in R]
def fams(job):
    j = unacc(job).replace('\u2019', "'")
    return [i for i, c in enumerate(CR) if c.search(j)]
def band(g):
    for k, (a, b) in enumerate(BANDS):
        if a <= g <= b: return k
    return None
def mingen(P, root):
    best = {root: 0}; q = collections.deque([(root, 0)])
    while q:
        x, g = q.popleft()
        if best.get(x, 99) < g: continue
        for par in P[x].get('parents', []) or []:
            if par in P and (par not in best or best[par] > g + 1):
                best[par] = g + 1; q.append((par, g + 1))
    return best
def year(s):
    m = re.search(r'(\d{4})', s or ''); return int(m.group(1)) if m else None
def midyear(p):
    b, d = year(p.get('birth')), year(p.get('death'))
    if b and d: return (b + d) / 2
    return b or d
R6 = lambda v: 0 if v == 0 else round(v, 6)
def matrix(P, root, off, glob=None, canon=None):
    mg = mingen(P, root); glob = glob or {}
    M = [[0.0] * N for _ in range(5)]; per = [0] * 5; kn = [0] * 5; ny = [0] * 5
    cc = [collections.Counter() for _ in range(5)]
    un = collections.defaultdict(list); jf = [collections.defaultdict(list) for _ in range(N)]
    bp = bk = 0; unatt = collections.Counter()
    for x, g0 in mg.items():
        g = min(g0 + off, glob.get(x, 99))
        if g < 1: continue
        p = P[x]; job = (p.get('job') or '').strip(); k = band(g)
        if k is None:
            bp += 1; bk += 1 if job else 0; continue
        per[k] += 1
        my = midyear(p)
        if my is not None: ny[k] += 1; cc[k][int((my - 1) // 100) + 1] += 1
        if job:
            kn[k] += 1; f = fams(job)
            if not f: unatt[job] += 1; 
            for i in f: M[k][i] += 1 / len(f)
            if canon:
                for fi, lab in canon(x, job):
                    jf[fi][lab].append(x)
                if not f:
                    for lab in canon(x, job, unclassified=True): un[lab].append(x)
    M = [[R6(v) for v in r] for r in M]
    return dict(counts=M, persons=per, known=kn, labels=[R6(sum(r)) for r in M], beyond={'p': bp, 'k': bk}, unatt=[[j, n] for j, n in sorted(unatt.items(), key=lambda t: (-t[1], t[0]))],
                cc=[{str(c): n for c, n in sorted(cc[b].items())} for b in range(5)], ny=ny, _jf=[dict(d) for d in jf], _uj=dict(un))
