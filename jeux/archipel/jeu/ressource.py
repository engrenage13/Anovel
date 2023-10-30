from systeme.FondMarin import Color

class Ressource:
    def __init__(self, valeur: int, couleur: Color, icone: str) -> None:
        self.valeur = valeur
        self.couleur = couleur
        self.path_icone = icone

    def __add__(self, valeur: int) -> None:
        self.valeur += valeur

    def __sub__(self, valeur: int) -> None:
        self.valeur -= valeur
        