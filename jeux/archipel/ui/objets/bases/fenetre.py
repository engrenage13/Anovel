from systeme.FondMarin import draw_rectangle, BLACK, Color, xf, yf

class Fenetre:
    """Elément fenêtre.
    """
    def __init__(self, fond: Color = BLACK) -> None:
        """Crée une fenêtre

        Args:
            fond (Color, optional): La couleur de fond de la fenêtre. Defaults to BLACK.
        """
        self.boutons = []
        self.action = None
        self.fond = fond

    def dessine(self) -> None:
        """Dessine la fenêtre
        """
        draw_rectangle(0, 0, xf, yf, self.fond)

    def estFini(self) -> bool:
        """Vérifie si l'action de la fenêtre est terminée.

        Returns:
            bool: True si la fenêtre doit se fermer.
        """
        return False
    
    def rejouer(self) -> None:
        """Réinitialise les éléments de la fenêtre.
        """
        pass