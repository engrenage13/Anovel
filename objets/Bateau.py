from objets.BateauJoueur import Bateau
from FondMarin import fond, noir

def estTouche(bateau: Bateau, posi: str) -> bool:
    """
    Dit si le bateau passé en paramètres est sur la case qui est regardée.
    param: bateau: le bateau
    param: posi: la case à vérifier
    return: booléen
    """
    a = False
    i = 0
    while i < len(bateau.pos) and not a:
        b = bateau.pos[i][0:len(bateau.pos[i])-2]
        if b == posi:
            bateau.etatSeg[i] = 'x'
            a = True
        i = i + 1
    return a

def estToucheBateau(joueur: Bateau, case: str) -> bool:
    """
    Retourne vrai si l'un des bateaux du joueur est touché.
    param: joueur: le joueur
    param: case: la case touchée
    return: liste composé du booléen réponse et de l'indice du bateau correspondant.
    """
    a = False
    i = 0
    while i < len(joueur.SetBateaux) and not a:
        a = estTouche(joueur.SetBateaux[i], case)
        i = i + 1
    return [a, i-1]

def estCoule(bateau: Bateau) -> bool:
    """
    Dit si le bateau regardé est coulé ou non.

    bateau: le bateau.
    return: booléen.
    """
    a = False
    if bateau.coule:
        a = True
    else:
        if 'o' not in bateau.etatSeg:
            bateau.coule = True
            a = True
    return a

def aPerduJoueur(joueur: Bateau) -> bool:
    """
    Vérifie si le joueur passé en paramètre a encore des bateaux non-coulés.

    joueur: le joueur pour lequel il faut vérifier les bateaux.
    return: booléen.
    """
    a = True
    i = 0
    while i < len(joueur.SetBateaux) and a:
        if not estCoule(joueur.SetBateaux[i]):
            a = False
        i = i + 1
    return a

def plongerDanslAbysse(bateau: Bateau) -> None:
    """Colorie toutes les cases occupé par le bateau en noir.

    Args:
        bateau (Bateau): Bateau coulé.
    """
    for i in range(len(bateau.pos)):
        cible = bateau.pos[i][0:len(bateau.pos[i])-2] + "c" + str(3-bateau.proprio.id)
        fond.itemconfigure(cible, fill=noir)