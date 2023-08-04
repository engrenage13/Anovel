from systeme.FondMarin import *
from ui.PosiJauge import PosiJauge
from ui.blocTexte import BlocTexte
from ui.interrupteur import Interrupteur
from reve.dimensions import getDimsCadre

def dessineInterrupteur(interrupteur: Interrupteur, x: int, y: int) -> list:
    """Dessine un Interrupeteur.

    Args:
        interrupteur (Interrupteur): L'interrupteur à dessiner.
        x (int): Abscisse de l'origine de l'interrupteur.
        y (int): Ordonnée de l'origine de l'interrupteur.

    Returns:
        list: Les dimensions de l'interrupteur.
    """
    interrupteur.dessine(x, y)
    return interrupteur.getDims()

def dessinePosiJauge(jauge: PosiJauge, x: int, y: int, longueurMax: int) -> list:
    """Dessine une PosiJauge.

    Args:
        jauge (PosiJauge): La PosiJauge à dessiner.
        x (int): Abscisse de l'origine de la PosiJauge.
        y (int): Ordonnée de l'origine de la PosiJauge.
        longueurMax (int): La longueur maximale de la PosiJauge.

    Returns:
        list: Les dimensions de la PosiJauge.
    """
    l = int(longueurMax-jauge.points[len(jauge.points)-1][0].getDims()[0]/2-jauge.points[0][0].getDims()[0]/2)
    jauge.dessine(x, y, l)
    return jauge.getDims()

def dessineTexte(texte: BlocTexte, x: int, y: int) -> list:
    """Dessine un bloc de texte.

    Args:
        texte (BlocTexte): Le bloc de texte à dessiner.
        x (int): Abscisse de l'origine du bloc.
        y (int): Ordonnée de l'origine du bloc.

    Returns:
        list: Les dimensions du bloc.
    """
    texte.dessine([[x, y], 'no'], alignement='g')
    return texte.getDims()

def dessineCadre(cadre: list, x: int, y: int, espace: int) -> list:
    """Dessine un cadre.

    Args:
        cadre (list): Le cadre à dessiner.
        x (int): Abscisse de l'origine du cadre.
        y (int): Ordonnée de l'origine du cadre.
        espace (int): Espace entre les éléments internes du cadre.

    Returns:
        list: Les dimensions du cadre.
    """
    h = getDimsCadre(cadre, espace)[1]
    draw_rectangle_rounded([x, y, cadre[0][0], h], 0.2, 30, cadre[0][1])
    ecart = int(xf*0.0125)
    x += ecart
    y += int(espace/2)
    for i in range(len(cadre)-1):
        element = cadre[i+1]
        if type(element) == BlocTexte:
            y += dessineTexte(element, x, int(y-espace*0.1))[1] + int(espace*0.5)
        elif type(element) == PosiJauge:
            y += dessinePosiJauge(element, x, int(y+espace/2), cadre[0][0]-ecart)[1] + espace
        elif type(element) == Interrupteur:
            y += dessineInterrupteur(element, x, y)[1] + int(espace/2)
        elif type(element) == list and type(element[0]) == list:
            y += dessineCadre(element, x, y, espace)[1] + int(espace/2)
        else:
            y += espace
    return [cadre[0][0], h]