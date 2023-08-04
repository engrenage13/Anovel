from ui.blocTexte import BlocTexte
from ui.PosiJauge import PosiJauge
from ui.interrupteur import Interrupteur
from museeNoyee import cadreCodeErreur

def getDimsCadre(cadre: list, espace: int) -> list:
    """Renvoie les dimensions d'un cadre.

    Args:
        cadre (list): Le cadre dont on cherche les dimensions.
        espace (int): L'espace entre les composants internes.

    Returns:
        list: (largeur, hauteur).
    """
    largeur = cadre[0][0]
    hauteur = int(espace/2)
    for i in range(len(cadre)-1):
        element = cadre[i+1]
        if type(element) == str:
            hauteur += espace
        elif type(element) == list and type(element[0]) == list:
            hauteur += getDimsCadre(element, espace)[1] + int(espace/2)
        elif type(element) in (BlocTexte, Interrupteur):
            hauteur += element.getDims()[1] + int(espace/2)
        elif type(element) == PosiJauge:
            hauteur += element.getDims()[1] + espace
    return [largeur, hauteur]

def getDimsErreur(erreur: tuple, espace: int) -> list:
    """Mesure la taille d'une erreur.

    Args:
        erreur (tuple): L'erreur à mesurer.
        espace (int): La valeur de l'espace à intercallé.

    Returns:
        list: 1. longueur de l'erreur. 2. hauteur de l'erreur.
    """
    largeur = cadreCodeErreur.width
    hauteur = cadreCodeErreur.height
    dims = erreur[1].getDims()
    if largeur < dims[0]:
        largeur = dims[0]
    hauteur += dims[1] + espace
    return [int(largeur), int(hauteur)]

def mesureTaille(contenu: list, espace: int) -> int:
    """Mesure la taille du contenu de la fenêtre.
    """
    h = 0
    for i in range(len(contenu)):
        element = contenu[i]
        if type(element) == list:
            h += int(getDimsCadre(element, espace)[1] + espace)
        elif type(element) in (BlocTexte, Interrupteur):
            h += int(element.getDims()[1] + espace/2)
        elif type(element) == PosiJauge:
            h += int(element.getDims()[1] + espace)
        elif type(element) == str:
            h += espace
    return h

def mesureTailleErreurs(erreurs: list, espace: int) -> int:
    """Mesure la taille d'une série d'erreurs.

    Args:
        erreurs (list): Les erreurs à mesurer.
        espace (int): La valeur de l'espace à intercalé.

    Returns:
        int: La hauteur de toutes les erreurs de la liste.
    """
    h = 0
    for i in range(len(erreurs)):
        h += getDimsErreur(erreurs[i], espace)[1] + espace
    return h