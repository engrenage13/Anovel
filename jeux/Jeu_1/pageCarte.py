from jeux.Jeu_1.objets.bases.fenetre import Fenetre, xf, yf, draw_rectangle
from jeux.Jeu_1.objets.plateau.ptiPlateau import PtiPlateau
from jeux.Jeu_1.fonctions.bases import TAILLEPETITECASE

class PageCarte(Fenetre):
    def __init__(self) -> None:
        super().__init__()
        self.plateau = PtiPlateau(15)

    def dessine(self) -> None:
        super().dessine()
        draw_rectangle(0, 0, xf, yf, [144, 132, 78, 85])
        self.plateau.dessine()