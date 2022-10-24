from systeme.FondMarin import *

defaut = [('anims', "2")]
actuel = []

def fichierExiste() -> bool:
    rep = False
    if file_exists("parametres/set.txt"):
        rep = True
    return rep

def lecture() -> None:
    texte = load_file_text("parametres/set.txt")
    fil = texte.split("\n")
    for i in range(len(fil)):
        actuel.append(fil[i].split(" "))

def sauvegarde(reset: bool = False) -> None:
    contenu = ""
    if not reset:
        liste = actuel
    else:
        liste = defaut
    for i in range(len(liste)):
        l = " ".join(liste[i])
        contenu += l
        if reset:
            actuel[i][1] = defaut[i][1]
        if i < len(liste)-1:
            contenu += "\n"
    fichier = open("parametres/set.txt", "w+")
    fichier.write(contenu)
    fichier.close()

def setParam(param: str, valeur: int) -> None:
    trouve = False
    i = 0
    while i < len(actuel) and not trouve:
        if actuel[i][0] == param:
            trouve = True
            actuel[i][1] = str(valeur)
        i = i + 1
    if not trouve:
        actuel.append((param, str(valeur)))
    sauvegarde()

def startSet() -> None:
    if not fichierExiste():
        sauvegarde(True)
    else:
        lecture()

def trouveParam(param: str) -> int:
    trouve = False
    valeur = False
    i = 0
    while i < len(actuel) and not trouve:
        if actuel[i][0] == param:
            trouve = True
            valeur = int(actuel[i][1])
        i = i + 1
    return valeur