from jeux.archipel.fonctions.deplacement import regleVitesse

class Bougeable:
    """Définit un objet déplaçable.
    """
    def __init__(self, x: int = 0, y: int = 0) -> None:
        """Crée un objet déplaçable.

        Args:
            x (int, optional): Abcsisse de départ de l'objet. Defaults to 0.
            y (int, optional): Ordonnée de départ de l'objet. Defaults to 0.
        """
        self.pos = (x, y)

    def deplace(self, x: int, y: int) -> None:
        """Déplace l'élément.

        Args:
            x (int): Ajoute x à l'abcsisse de la position de l'objet.
            y (int): Ajoute y à l'ordonnée de la position de l'objet.
        """
        self.setPos(self.pos[0]+x, self.pos[1]+y)

    def deplaceGlisse(self, destination: tuple[int], vitesse: int = 1) -> None:
        """Déplace l'objet vers une destination souhaitée.

        Args:
            destination (tuple[int]): L'endroit où l'objet doit aller.
            vitesse (int, optional): La vitesse de l'objet en pixels/déplacement. Defaults to 1.
        """
        x = self.pos[0]
        y = self.pos[1]
        dx = destination[0]
        dy = destination[1]
        vitx = regleVitesse(x, dx, vitesse)
        vity = regleVitesse(y, dy, vitesse)
        if x < dx:
            x += vitx
        elif x > dx:
            x -= vitx
        if y < dy:
            y += vity
        elif y > dy:
            y -= vity
        self.pos = (x, y)

    def setPos(self, x: int, y: int) -> None:
        """Modifie la position de l'élément.

        Args:
            x (int): Le nouvel abscisse de l'objet.
            y (int): Le nouvel ordonnée de l'objet.
        """
        self.pos = (x, y)