from systeme.set import sauvegarde

def trouveFonction(code: str):
    """Permet de trouver une fonction dans la liste des fonctions systeme de REVE.

    Args:
        code (str): L'identifiant de la fonction recherchée.

    Returns:
        function: Une fonction, ou False si la fonction n'a pas était trouvée.
    """
    rep = False
    i = 0
    while i < len(lifonc) and not rep:
        test = lifonc[i]
        if test[0] == code.lower():
            rep = test[1]
        i = i + 1
    return rep

def reset() -> None:
    """Réinitialise les paramètres du jeu.
    """
    sauvegarde(True)

lifonc = [("reset", reset)]