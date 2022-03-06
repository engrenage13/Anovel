import random
from FondMarin import *

def plateau(x: int, y: int, couleurs: list, idtag: str): # Crée un plateau.
    """Crée un plateau de jeu.

    Args:
        x (int): Nombre de cases dans la longueur.
        y (int): Nombre de cases dans la hauteur.
        couleurs (list): Liste de couleurs à apporter au plateau (disposition aléatoire).
        idtag (str): Tag du plateau (permet de l'identifier).

    Returns:
        _type_: _description_
    """
    taille = yf*0.84/x
    g = fond.coords('pg')
    b = yf*0.105
    c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
         'V', 'W', 'X', 'Y', 'Z']
    e = []
    for i in range(y):
        a = g[2]
        f = []
        for j in range(x):
            d = c[i] + str(j+1) + idtag[0] + idtag[len(idtag)-1]
            fond.create_rectangle(a, b, a+taille, b+taille, fill=random.choice(couleurs), state='hidden', 
                                  tags=(d, idtag, 'plateau'))
            f.append(d)
            a = a + taille
        b = b + taille
        e.append(f)
    return e