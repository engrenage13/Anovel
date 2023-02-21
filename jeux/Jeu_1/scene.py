from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.plateau.plateau import Plateau

class Scene:
    def __init__(self) -> None:
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.g1 = Grille(int(xf*0.04), [False], False)
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.plateau = Plateau()
        # Between the worlds
        self.play = False
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        draw_rectangle(0, 0, xf, yf, BLACK)
        self.plateau.dessine(0, 0)
        if self.play:
            self.g1.dessine(int(xf-self.g1.largeur), 0)
            if self.plateau.bloque:
                self.plateau.bloque = False
        else:
            if not self.plateau.bloque:
                self.plateau.bloque = True

    # Between the worlds
    def portailAustral(self) -> None:
        if self.play:
            i = 0
            v = False
            while i < len(self.opt) and not v:
                if self.opt[i][0].getContact():
                    v = True
                    self.nouveauMessage(self.opt[i][1])
                else:
                    i += 1

    def nouveauMessage(self, message: str) -> None:
        self.message = message
        self.lu = False