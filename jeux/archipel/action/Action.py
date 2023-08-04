class Action:
    """Une action est l'élément de base pour effectuer n'importe quelle "action" dans le jeu.
    """
    def __init__(self, elements: list) -> None:
        """Crée une action

        Args:
            elements (list): Tous ce qu'il est possible de faire avec cette action.
        """
        self.elements = elements
        self.resultat = None

    def estFinie(self) -> bool:
        """Vérifie si l'action est terminée.

        Returns:
            bool: True si l'action est terminée.
        """
        if self.resultat == None:
            return False
        else:
            return True