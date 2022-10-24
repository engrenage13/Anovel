from systeme.FondMarin import *
from ui.PosiJauge import PosiJauge
from ui.blocTexte import BlocTexte
from ui.bouton import Bouton
from reve.dimensions import getDimsCadre

def dessineBouton(bouton: Bouton, x: int, y: int) -> list:
    bouton.dessine((int(x+bouton.largeur/2), int(y+bouton.hauteur/2)))
    return bouton.getDims()

def dessinePosiJauge(jauge: PosiJauge, x: int, y: int, longueurMax: int) -> list:
    l = int(longueurMax-jauge.points[len(jauge.points)-1][0].getDims()[0]/2-jauge.points[0][0].getDims()[0]/2)
    jauge.dessine(x, y, l)
    return jauge.getDims()

def dessineTexte(texte: BlocTexte, x: int, y: int) -> list:
    texte.dessine([[x, y], 'no'], alignement='g')
    return texte.getDims()

def dessineCadre(cadre: list, x: int, y: int, espace: int) -> list:
    h = getDimsCadre(cadre, espace)[1]
    draw_rectangle_rounded([x, y, cadre[0][0], h], 0.2, 30, cadre[0][1])
    ecart = int(xf*0.0125)
    x += ecart
    y += int(espace/2)
    for i in range(len(cadre)-1):
        element = cadre[i+1]
        if type(element) == BlocTexte:
            y += dessineTexte(element, x, y)[1] + int(espace/2)
        elif type(element) == PosiJauge:
            y += dessinePosiJauge(element, x, int(y+espace/2), cadre[0][0]-ecart)[1] + espace
        elif type(element) == Bouton:
            y += dessineBouton(element, x, y)[1] + int(espace/2)
        elif type(element) == list and type(element[0]) == list:
            y += dessineCadre(element, x, y, espace)[1] + int(espace/2)
        else:
            y += espace
    return [cadre[0][0], h]