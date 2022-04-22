from objets.BateauJoueur import Bateau
from objets.Joueur import Joueur

def estTouche(bateau: Bateau, posi: str) -> bool:
    """Dit si le bateau passé en paramètres est sur la case qui est regardée.

    Args:
        bateau (Bateau): Bateau comparer.
        posi (str): Case vérifier.

    Returns:
        bool: True si le bateau est sur la case touché.
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

def estToucheBateau(joueur: Joueur, case: str) -> list:
    """Vérifie si l'un des bateaux du joueur est touché.

    Args:
        joueur (Joueur): Joueur pour lequel, il faut vérifier.
        case (str): Case à comparer.

    Returns:
        list: Une liste composé d'un booléen, ainsi que l'indice du bateau touché dans la liste du joueur.
    """
    a = False
    i = 0
    while i < len(joueur.SetBateaux) and not a:
        a = estTouche(joueur.SetBateaux[i], case)
        i = i + 1
    return [a, i-1]

def estCoule(bateau: Bateau) -> bool:
    """Dit si le bateau testé est coulé ou non.

    Args:
        bateau (Bateau): Bateau à vérifier.

    Returns:
        bool: True si le bateau est coulé.
    """
    a = False
    if bateau.coule:
        a = True
    else:
        if 'o' not in bateau.etatSeg:
            bateau.coule = True
            a = True
    return a

def aPerduJoueur(joueur: Joueur) -> bool:
    """Vérifie si le joueur passé en paramètre a encore des bateaux non-coulés.

    Args:
        joueur (Joueur): Joueur à tester.

    Returns:
        bool: True si tous les bateaux du joueur ont coulés.
    """
    a = True
    i = 0
    while i < len(joueur.SetBateaux) and a:
        if not estCoule(joueur.SetBateaux[i]):
            a = False
        i = i + 1
    return a