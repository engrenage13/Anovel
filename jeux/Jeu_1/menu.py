from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille

class Menu:
    def __init__(self) -> None:
        self.opt = [[Bouton(TB1o, BTV, "REPRENDRE", '', [self.portailAustral]), "JEU"],
                    [Bouton(TB1o, BTNOIR, "PARAMETRES", '', [self.portailAustral]), "ANOVEL_OPTIONS"],
                    [Bouton(TB1o, BTNOIR, "MENU", '', [self.portailAustral]), "ANOVEL_MENU"],
                    [Bouton(TB1o, BTDANGER, "QUITTER", '', [self.portailAustral]), "QUITTE"]]
        self.gm1 = Grille(int(xf*0.25), [False])
        self.gm1.ajouteElement(self.opt[0][0], 0, 0)
        self.gm1.ajouteElement(self.opt[1][0], 0, 1)
        self.gm2 = Grille(int(xf*0.25), [False])
        self.gm2.ajouteElement(self.opt[2][0], 0, 0)
        self.gm3 = Grille(int(xf*0.25), [False])
        self.gm3.ajouteElement(self.opt[3][0], 0, 0)
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 170]
        ecart = int(yf*0.03)
        h = int(self.gm1.hauteur+self.gm2.hauteur+self.gm3.hauteur+ecart*4)
        self.hauteurContenu = [int(yf*1.1), int(yf/2-h/2)]
        # Between the worlds
        self.play = False
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        if not self.ok and not self.playAnim:
            self.playAnim = True
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        self.gm1.dessine(int(xf/2-self.gm1.largeur/2), y)
        y += self.gm1.hauteur + ecart
        self.dessineLigne(int(xf/2), y)
        y += ecart
        self.gm2.dessine(int(xf/2-self.gm2.largeur/2), y)
        y += self.gm2.hauteur + ecart
        self.dessineLigne(int(xf/2), y)
        y += ecart
        self.gm3.dessine(int(xf/2-self.gm3.largeur/2), y)
        if is_key_pressed(256):
            self.closeMenu()
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

    def dessineLigne(self, x: int, y: int) -> None:
        l = 0.43
        l2 = int(yf*0.02)
        draw_line_ex((int(x-self.gm1.largeur*l), y), (int(x-l2*2), y), 2, GRAY)
        draw_line_ex((int(x+l2*2), y), (int(x+self.gm1.largeur*l), y), 2, GRAY)
        draw_poly_lines_ex((x, y), 4, l2, 0, 3, GRAY)
        draw_poly((x, y), 4, int(yf*0.01), 0, GRAY)

    def anims(self, mode: bool) -> None:
        if mode:
            if self.opac[0] < self.opac[1]:
                self.opac[0] += 2
            if self.hauteurContenu[0] > self.hauteurContenu[1]:
                self.hauteurContenu[0] -= int(yf*0.03)
            if self.opac[0] == self.opac[1] and self.hauteurContenu[0] <= self.hauteurContenu[1]:
                self.playAnim = False
                self.ok = True
        else:
            if self.opac[0] > 0:
                self.opac[0] -= 2
            if self.hauteurContenu[0] < int(yf*1.1):
                self.hauteurContenu[0] += int(yf*0.03)
            if self.opac[0] == 0 and self.hauteurContenu[0] >= int(yf*1.1):
                self.playAnim = False
                self.ok = False

    # Between the worlds
    def portailAustral(self) -> None:
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

    def closeMenu(self) -> None:
        self.message = "JEU"
        self.lu = False