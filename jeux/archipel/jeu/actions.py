from jeux.archipel.jeu.joueur import Joueur
from jeux.archipel.jeu.bateau import Bateau

def vole_marin(victime: Bateau, voleur: Bateau, nb_marins: int = 1) -> bool:
    """Déplace un certain nombre de marins d'un bateau vers un autre.

    Args:
        victime (Bateau): Le bateau qui va perdre des marins.
        voleur (Bateau): Le bateau qui va gagner des marins.
        nb_marins (int, optional): Le nombre de marins à déplacer. Defaults to 1.

    Returns:
        bool: True si l'opération s'est faite sans encombre, False dans le cas contraire.
    """
    retour = False
    if victime.get_marins() >= nb_marins:
        retour = True
        victime.marins - nb_marins
        voleur.marins + nb_marins
    return retour

def vole_bateau(victime: Joueur, voleur: Joueur, cible: Bateau) -> bool:
    """Prélève le bateau passé en paramètre de la main de victime pour l'ajouter à celle de voleur.

    Args:
        victime (Joueur): Le joueur à qui prendre le bateau.
        voleur (Joueur): Le joueur qui va gagner le bateau.
        cible (Bateau): Le bateau qui va changer de main.

    Returns:
        bool: True si l'opération s'est déroulée sans accroc, False dans le cas contraire.
    """
    retour = False
    if cible in victime:
        retour = True
        victime - cible
        voleur + cible
    return retour

def inflige_dommage(victime: Bateau, proprietaire: Joueur, degats: int) -> bool:
    """Inflige un nombre variable de dégâts à un bateau précis.

    Args:
        victime (Bateau): Le bateau qui va subir les dégâts.
        proprietaire (Joueur): Le propriétaire de ce bateau.
        degats (int): Les dégâts à infliger au bateau.

    Returns:
        bool: True si le bateau a coulé. Sinon False.
    """
    coule = False
    if victime in proprietaire.bateaux:
        coule = victime - degats
        if coule:
            proprietaire - victime
    return coule