from systeme.FondMarin import *

defaut = [('anims', "2"), ("stats", "1")]
actuel = []

def fichierExiste() -> bool:
    """Vérifie si le fichier de sauvegarde existe.

    Returns:
        bool: True s'il existe.
    """
    rep = False
    if file_exists("parametres/set.txt"):
        rep = True
    return rep

def lecture() -> None:
    """Lis le fichier de sauvegarde.
    """
    texte = load_file_text("parametres/set.txt")
    fil = texte.split("\n")
    for i in range(len(fil)):
        actuel.append(fil[i].split(" "))
    if len(defaut) != len(actuel):
        for i in range(len(defaut)):
            trouve = False
            j = 0
            while j < len(actuel) and not trouve:
                if defaut[i][0] == actuel[j][0]:
                    trouve = True
                j += 1
            if not trouve:
                actuel.append(list(defaut[i]))

def sauvegarde(reset: bool = False) -> None:
    """Sauvegarde les valeurs des paramètres.

    Args:
        reset (bool, optional): Réinitialise les valeurs par défaut. Defaults to False.
    """
    contenu = ""
    if not reset:
        liste = actuel
    else:
        liste = defaut
    for i in range(len(liste)):
        l = " ".join(liste[i])
        contenu += l
        if reset and fichierExiste():
            actuel[i][1] = defaut[i][1]
        if i < len(liste)-1:
            contenu += "\n"
    fichier = open("parametres/set.txt", "w+")
    fichier.write(contenu)
    fichier.close()

def setParam(param: str, valeur: int) -> None:
    """Modifie la valeur d'un paramètre.

    Args:
        param (str): Le paramètre dont la valeur va être modifiée.
        valeur (int): La nouvelle valeur à appliquer.
    """
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
    """Lance l'opération de sauvegarde.
    """
    if not fichierExiste():
        sauvegarde(True)
    lecture()

def trouveParam(param: str) -> int:
    """Trouve la valeur d'un paramètre.

    Args:
        param (str): Le paramètre recherché.

    Returns:
        int: La valeur du paramètre.
    """
    trouve = False
    valeur = False
    i = 0
    while i < len(actuel) and not trouve:
        if actuel[i][0] == param:
            trouve = True
            valeur = int(actuel[i][1])
        i = i + 1
    return valeur