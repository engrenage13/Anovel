from reve.OZ import POLICE, TAILLEPOLICE
from reve.fonctions import trouveFonction
from ui.PosiJauge import PosiJauge
from ui.blocTexte import BlocTexte
from ui.bouton import Bouton
from ui.interrupteur import Interrupteur

def cadre(ligne: str) -> list:
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

def bouton(ligne: str) -> Bouton:
    fonctions = []
    couleur = []
    texte = ""
    icone = []
    set = ""
    capsule = False
    sequence = ""
    for i in range(len(ligne)):
        car = ligne[i]
        if car == " ":
            if sequence != "":
                sequence += car
        elif car == "=":
            if sequence.lower() == "f":
                set = "f"
                sequence = ""
            elif sequence.lower() == "c":
                set = "c"
                sequence = ""
            elif sequence.lower() == "t":
                set = "t"
                sequence = ""
            elif sequence.lower() == "i":
                set = "i"
                sequence = ""
            else:
                sequence += car
        elif car == "(":
            capsule = True
        elif car == ")":
            if capsule:
                if set == "f":
                    fon = trouveFonction(sequence)
                    if fon:
                        fonctions.append(fon)
                elif set == "c":
                    couleur.append(int(sequence))
                elif set == "i":
                    icone.append(sequence)
                sequence = ""
            capsule = False
        elif car == ",":
            if sequence != "":
                if set == "f":
                    fon = trouveFonction(sequence)
                    if fon:
                        fonctions.append(fon)
                elif set == "c":
                    couleur.append(int(sequence))
                elif set == "t":
                    texte += sequence
                elif set == "i":
                    icone.append(sequence)
                sequence = ""
            if not capsule:
                set = ""
        else:
            sequence += car
    if len(couleur) == 0:
        couleur = [0, 0, 0, 255]
    elif len(couleur) == 3:
        couleur.append(255)
    if len(icone) == 0:
        icone = None
    return Bouton(fonctions, couleur, texte, icone)

def interrupteur(ligne: str) -> Interrupteur:
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
    else:
        t = int(TAILLEPOLICE*1.4)
    return BlocTexte(sequence, POLICE, t, [largeurMax, ''])

def widget(ligne: str) -> list:
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
            elif sequence.lower() == "bouton":
                rep = bouton(ligne[i+1:len(ligne)])
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