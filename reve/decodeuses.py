from reve.OZ import *
from ui.PosiJauge import PosiJauge
from ui.blocTexte import BlocTexte
from ui.interrupteur import Interrupteur

def cadre(ligne: str) -> list:
    """Décodes les instructions pour créer un cadre.

    Args:
        ligne (str): La ligne lue.

    Returns:
        list: Les paramètres du cadre.
    """
    couleur = []
    sequence = ""
    set = ""
    capsule = False
    for i in range(len(ligne)):
        car = ligne[i]
        if car == " ":
            if sequence != "" and sequence != "[":
                sequence += car
            else:
                sequence = ""
        elif car == "=":
            if sequence.lower() == 'c':
                set = "c"
                sequence = ""
        elif car == "(":
            capsule = True
        elif car == ")":
            if capsule and set == "c":
                couleur.append(int(sequence))
                sequence = ""
            capsule = False
        elif car == ",":
            if set == "c":
                couleur.append(int(sequence))
                sequence = ""
            else:
                sequence += car
        else:
            sequence += car
    if len(couleur) == 0:
        couleur = [0, 0, 0, 255]
    elif len(couleur) == 3:
        couleur.append(255)
    return [couleur]

def checkFinCadre(ligne: str) -> bool:
    """Vérifie si le cadre est terminé.

    Args:
        ligne (str): Ligne lue.

    Returns:
        bool: True si c'est la fin du cadre.
    """
    rep = False
    if "]" in ligne:
        position = ligne.index("]")
        if position == len(ligne)-1:
            rep = True
        else:
            rep = True
            i = position+1
            while i < len(ligne) and rep:
                car = ligne[i]
                if car != " ":
                    rep = False
                i = i + 1
    return rep

def interrupteur(ligne: str) -> Interrupteur:
    """Extrait les informations pour créer un interrupteur.

    Args:
        ligne (str): Ligne lue.

    Returns:
        Interrupteur: L'interrupteur créé.
    """
    sequence = ""
    for i in range(len(ligne)):
        car = ligne[i]
        if car == " ":
            if sequence != "":
                sequence += car
        else:
            sequence += car
    return Interrupteur(sequence)

def posiJauge(ligne: str) -> PosiJauge:
    """Extrait les instructions d'une ligne pour créer une PosiJauge.

    Args:
        ligne (str): Ligne lue.

    Returns:
        PosiJauge: La PosiJauge créée.
    """
    longueur = 1
    points = []
    set = ""
    capsule = False
    sequence = ""
    for i in range(len(ligne)):
        car = ligne[i]
        if car == " ":
            if sequence != "":
                sequence += car
        elif car == "=":
            if sequence.lower() == "l":
                set = "l"
                sequence = ""
            elif sequence.lower() == "p":
                set = "p"
                sequence = ""
            else:
                sequence += car
        elif car == "(":
            capsule = True
        elif car == ")":
            if capsule and set == "p":
                points.append(sequence)
                sequence = ""
            capsule = False
        elif car == ",":
            if set == "l":
                longueur = float(sequence)
                if longueur > 1:
                    longueur = 1
                elif longueur < 0.1:
                    longueur = 0.1
                set = sequence = ""
            elif set == "p":
                if capsule:
                    points.append(sequence)
                    sequence = ""
                else:
                    set = ""
            else:
                sequence += car
        else:
            sequence += car
    return PosiJauge(points, longueur)

def texte(ligne: str, largeurMax: int) -> BlocTexte:
    """Extrait les instructions d'une ligne pour créer un bloc de texte.

    Args:
        ligne (str): Ligne lue.
        largeurMax (int): largeur maximale du bloc.

    Returns:
        BlocTexte: Le bloc de texte généré.
    """
    sequence = ""
    mode = 1
    for i in range(len(ligne)):
        car = ligne[i]
        if car == " ":
            if sequence == "#":
                mode = 2
                sequence = ""
            elif sequence != "":
                if sequence[len(sequence)-1] != " ":
                    sequence += car
        else:
            sequence += car
    if mode == 1:
        t = TAILLEPOLICE
        police = P2
    else:
        t = int(TAILLEPOLICE*1.4)
        police = P1I
    return BlocTexte(sequence.upper(), police, t, [largeurMax, ''])

def widget(ligne: str) -> list:
    """Extrait les informations d'une ligne pour créer un widget.

    Args:
        ligne (str): Ligne lue.

    Returns:
        list: Le ou les widgets créés.
    """
    sequence = ""
    i = 0
    rep = None
    while i < len(ligne) and rep == None:
        car = ligne[i]
        if car == " ":
            if sequence != "":
                sequence += car
        elif car == ">":
            if sequence.lower() == "posijauge":
                rep = posiJauge(ligne[i+1:len(ligne)])
            elif sequence.lower() == "interrupteur":
                rep = interrupteur(ligne[i+1:len(ligne)])
            else:
                sequence = ""
        else:
            sequence += car
        i = i + 1
    if rep != None:
        rep = [rep, rep.erreurs]
    return rep