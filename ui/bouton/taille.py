class Taille:
    def __init__(self, hauteur: int, redimensionnable: bool) -> None:
        self.hauteur = hauteur
        self.redim = redimensionnable
        self.tailleIcone = int(self.hauteur*0.9)