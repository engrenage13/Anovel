from systeme.FondMarin import police2, yf
from ui.blocTexte import BlocTexte

class Fagnon:
    def __init__(self, texte: str, longueur: int) -> None:
        self.longueur = longueur
        self.tailleTexte = int(yf*0.03)
        self.texte = BlocTexte(texte, police2, self.tailleTexte, [int(self.longueur*0.9), ''])
        self.hauteur = int(self.texte.getDims()[1]*2)
        self.pos = (0, 0)

    def dessine(self) -> None:
        x = self.pos[0] + int(self.longueur/2)
        y = self.pos[1] + int(self.hauteur*0.45)
        self.texte.dessine([[x, y], 'c'])

    def setPos(self, x: int, y: int) -> None:
        self.pos = (x, y)

    def getDims(self) -> tuple[int]:
        return (self.longueur, self.hauteur)