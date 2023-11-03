from jeux.archipel.jeu.joueur import Joueur
from jeux.archipel.jeu.bateau import Bateau

def vole_marin(victime: Bateau, voleur: Bateau, nb_marins: int = 1) -> bool:
    retour = False
    if victime.get_marins() >= nb_marins:
        retour = True
        victime.marins - nb_marins
        voleur.marins + nb_marins
    return retour

def vole_bateau(victime: Joueur, voleur: Joueur, cible: Bateau) -> bool:
    retour = False
    if cible in victime:
        retour = True
        victime - cible
        voleur + cible
    return retour