from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.fonctions.bases import TAILLECASE
from jeux.Jeu_1.jeu import Jeu, config

class Scene(Jeu):
    def __init__(self) -> None:
        super().__init__()
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.optDev = [Bouton(TB2n, BTDEV, "REJOUER", 'images/ui/reset.png', [self.rejouer]), 
                       Bouton(TB2n, BTDEV, "PASSER L'ACTION", 'images/ui/passer.png', [self.passeAction])]
        t = TB2n.hauteur
        self.g1 = Grille(int(t+yf*0.01), [False], False)
        self.gDev = Grille(int(t+yf*0.01), [False])
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.g1.largeur = int((1*(t+yf*0.005))+yf*0.005)
        for i in range(len(self.optDev)):
            self.gDev.ajouteElement(self.optDev[i], 0, i)
        self.gDev.hauteur = int(((len(self.opt)-1)*(t+yf*0.005))+yf*0.005)
        self.posCurseur = (get_mouse_x(), get_mouse_y())
        self.move = False
        self.trajet = (0, 0)
        self.afficheSecteur('c')
        self.delaiDepart = 70
        # Between the worlds
        self.play = False
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        fenetre = self.fen[self.fenActif]
        super().dessine()
        if self.play:
            if config[self.fenActif]['interface']:
                self.g1.dessine(int(xf-self.g1.largeur), 0)
                if config['dev']:
                    self.gDev.dessine(int(xf-self.gDev.largeur), self.g1.hauteur)
            if fenetre == self.plateau:
                if not self.plateau.bloque:
                    if self.delaiDepart <= 0:
                        self.deplace()
                    else:
                        self.delaiDepart -= 1
                else:
                    self.plateau.bloque = False
            else:
                if not self.plateau.bloque:
                    self.plateau.bloque = True
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

    def afficheSecteur(self, secteur: str) -> None:
        secteur = secteur.lower()
        if secteur == 'c':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'n':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        elif secteur == 'ne':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        elif secteur == 'e':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'se':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 's':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'so':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'o':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'no':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        else:
            px = py = 0
        if px != 0 and py != 0:
            self.plateau.place(px, py)

    def rejouer(self) -> None:
        super().rejouer()
        self.afficheSecteur('c')
        self.delaiDepart = 70

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