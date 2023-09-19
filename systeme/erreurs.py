e000 = ("000", "Fichier manquant ou se trouvant au mauvais endroit.")
e001 = ("001", "Ce type de fichier n'est pas lu.")
e100 = ("100", "Un des widget est mal definit.")
e101 = ("101", "Une couleur se compose de 4 valeurs comprisent entre 0 et 255.")

def checkCouleurErreur(erreur: tuple) -> list:
    """Vérifie le type de l'erreur pour renvoyer sa couleur.

    Args:
        erreur (tuple): L'erreur testé.

    Returns:
        list: La couleur retournée.
    """
    err = int(erreur[0])
    if err < 100:
        couleur = [255, 0, 0, 255]
    else:
        couleur = [249, 106, 8, 255]
    return couleur

def pasCouleur(couleur: list) -> bool:
    correct = 0
    for i in range(len(couleur)):
        if type(couleur[i]) == int and couleur[i] >= 0 and couleur[i] <= 255:
            correct += 1
    if len(couleur) != 4:
        rep = [e101[0], "Une couleur se compose de 4 valeurs."]
    elif correct != 4:
        rep = [e101[0], "Une couleur se compose de 4 nombres compris entre 0 et 255."]
    else:
        rep = False
    return rep