from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.objets.plateau.plateau import Plateau

class Scene:
    def __init__(self) -> None:
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.g1 = Grille(int(xf*0.04), [False], False)
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.plateau = Plateau(15)
        self.posCurseur = (get_mouse_x(), get_mouse_y())
        self.move = False
        self.trajet = (0, 0)
        # Between the worlds
        self.play = False
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        self.plateau.dessine()
        if self.play:
            self.g1.dessine(int(xf-self.g1.largeur), 0)
            if self.plateau.bloque:
                self.plateau.bloque = False
            self.deplace()
        else:
            if not self.plateau.bloque:
                self.plateau.bloque = True

    def deplace(self) -> None:
        x = get_mouse_x()
        y = get_mouse_y()
        if is_mouse_button_down(0):
            self.move = True
            if x != self.posCurseur[0] or y != self.posCurseur[1]:
                l = x - self.posCurseur[0]
                h = y - self.posCurseur[1]
                self.plateau.deplace(l, h)
                self.trajet = (self.trajet[0]+l, self.trajet[1]+h)
        elif self.trajet != (0, 0):
            self.glisse()
        self.posCurseur = (x, y)

    def glisse(self) -> None:
        if self.move:
            self.trajet = (int(self.trajet[0]/7), int(self.trajet[1]/7))
            self.move = False
        elif self.trajet != (0, 0):
            x = self.trajet[0]
            y = self.trajet[1]
            self.plateau.deplace(x, y)
            if x < 0:
                x = x + 1
            elif x > 0:
                x = x - 1
            if y < 0:
                y = y + 1
            elif y > 0:
                y = y - 1
            self.trajet = (x, y)

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