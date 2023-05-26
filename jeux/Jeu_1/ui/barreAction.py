from systeme.FondMarin import *
from ui.bouton.bouton import Bouton

class BarreAction:
    def __init__(self, joueurs: list, passe) -> None:
        self.joueurs = joueurs
        self.actuel = 0
        # boutons
        self.passe = Bouton(TB2n, PTIBT1, "PASSE", 'images/ui/passer+.png', [passe])
        # dimensions
        self.hauteur = int(yf*0.07)

    def dessine(self) -> None:
        draw_rectangle(0, yf-self.hauteur, xf, yf, [80, 80, 80, 150])
        self.passe.dessine(int(xf-self.passe.getDims()[0]*0.7), int(yf-self.hauteur/2))