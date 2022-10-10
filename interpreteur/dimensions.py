from ui.blocTexte import BlocTexte
from ui.PosiJauge import PosiJauge

def getDimsCadre(cadre: list, espace: int) -> list:
    largeur = cadre[0][0]
    hauteur = int(espace/2)
    for i in range(len(cadre)-1):
        element = cadre[i+1]
        if type(element) == str:
            hauteur += espace
        elif type(element) == list and type(element[0]) == list:
            hauteur += getDimsCadre(element, espace)[1] + int(espace/2)
        elif type(element) == BlocTexte:
            hauteur += element.getDims()[1] + int(espace/2)
        elif type(element) == PosiJauge:
            hauteur += element.getDims()[1] + espace
    return [largeur, hauteur]

def mesureTaille(contenu: list, espace: int) -> int:
    """Mesure la taille du contenu de la fenêtre.
    """
    h = 0
    for i in range(len(contenu)):
        element = contenu[i]
        if type(element) == list:
            h += int(getDimsCadre(element, espace)[1] + espace)
        elif type(element) == BlocTexte:
            h += int(element.getDims()[1] + espace/2)
        elif type(element) == PosiJauge:
            h += int(element.getDims()[1] + espace)
        elif type(element) == str:
            h += espace
    return h