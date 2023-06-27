from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from ui.blocTexte import BlocTexte
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.objets.Joueur import Joueur

class Fin:
    def __init__(self, joueurs: list[Joueur]) -> None:
        self.setJoueurs(joueurs)
        self.definiHauteur()
        # Dimensions
        self.largeur = int(xf*0.5)
        # Autres
        self.titre = BlocTexte("ORGANISATION", police1, int(yf*0.04), [self.largeur, ''])
        self.avertissement = BlocTexte("ATTENTION ! Cette action va mettre fin au deplacement.", police2, int(yf*0.03), [int(xf*0.94), ''])
        # Boutons
        self.opt = [Bouton(TB2n, PTIBT2, "PLUS", 'images/ui/plus.png', [self.plusGauche]),
                    Bouton(TB2n, PTIBT2, "MOINS", 'images/ui/moins.png', [self.moinsGauche]),
                    Bouton(TB2n, PTIBT2, "PLUS", 'images/ui/plus.png', [self.plusDroite]),
                    Bouton(TB2n, PTIBT2, "MOINS", 'images/ui/moins.png', [self.moinsDroite]),
                    Bouton(TB2n, PTIBT2, "REINITIALISER", 'images/ui/reset.png', [self.reset]),
                    Bouton(TB1o, BTX, "ANNULER", '', [self.annule]),
                    Bouton(TB1o, BTV, "CONFIRMER", '', [self.confirme])]
        self.gm1 = Grille(int(self.opt[0].largeur+yf*0.01), [False])
        self.gm1.ajouteElement(self.opt[0], 0, 0)
        self.gm1.ajouteElement(self.opt[1], 0, 1)
        self.gm2 = Grille(int(self.opt[2].largeur+yf*0.01), [False])
        self.gm2.ajouteElement(self.opt[2], 0, 0)
        self.gm2.ajouteElement(self.opt[3], 0, 1)
        self.gm3 = Grille(int(self.largeur*0.6), [False])
        self.gm3.ajouteElement(self.opt[-1], 0, 0)
        self.gm3.ajouteElement(self.opt[-2], 1, 0)
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 170]
        self.hauteurContenu = [int(yf*1.1), int(yf*0.09)]

    def dessine(self) -> None:
        couleurFondRec = [243, 123, 123, 255]
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        draw_rectangle(int(xf/2-self.largeur/2), y, self.largeur, self.hauteur, WHITE)
        if self.egalite:
            texte = "EGALITE"
            couleur = [165, 69, 229, 255]
        else:
            texte = "VICTOIRE"
            couleur = [21, 182, 227, 255]
        tt = measure_text_ex(police2i, texte, yf*0.1, 0)
        draw_text_ex(police2i, texte, (int(xf/2-tt.x/2), y), yf*0.1, 0, couleur)
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

    def dessineBateau(self, y: int, idBat: int, gauche: bool = True) -> int:
        total = self.bat[0].marins + self.bat[1].marins
        espace = int(yf*0.03)
        hbarre = int(yf*0.26)
        lbarre = int(xf*0.02)
        bat = self.bat[idBat]
        y += int(espace/2)
        texte = f"{bat.marinsi} marins en\ndebut de partie"
        tt = measure_text_ex(police2, texte, int(yf*0.025), 0)
        h = int(bat.marins*hbarre/total)
        tm = measure_text_ex(police2, str(bat.marins), int(yf*0.03), 0)
        ta = measure_text_ex(police1i, "ACTIF", int(yf*0.025), 0)
        couleurFondRec = [182, 231, 247, 255]
        couleurJauge = [12, 106, 156, 255]
        couleurContenu = [80, 224, 250, 255]
        couleurTexteRec = BLACK
        couleurTexteJauge = WHITE
        if gauche:
            x = int(xf/2-self.largeur*0.46)
            if bat.actif:
                draw_rectangle_rounded([x, int(y+yf*0.04-ta.y*0.55), int(ta.x*1.2), int(ta.y*1.1)], 0.15, 30, GOLD)
                draw_text_ex(police1i, "ACTIF", (int(x+ta.x*0.1), int(y+yf*0.04-ta.y*0.5)), int(yf*0.025), 0, WHITE)
            draw_texture(bat.images[0], x, int(y+hbarre*0.7-bat.images[0].height/2), WHITE)
            draw_rectangle_rounded([x, int(y+hbarre*0.7+bat.images[0].height*0.9), int(tt.x*1.1), int(tt.y*1.1)], 0.15, 30, couleurFondRec)
            draw_text_ex(police2, texte, (int(x+tt.x*0.05), int(y+hbarre*0.7+bat.images[0].height*0.9+tt.y*0.05)), int(yf*0.025), 0, couleurTexteRec)
            x += bat.images[0].width + espace
            draw_texture(self.marin, int(x+lbarre/2-self.marin.width/2), y, WHITE)
            y += self.marin.height
            draw_rectangle(x, y, lbarre, hbarre, couleurJauge)
            draw_rectangle(x, int(y+hbarre-h), lbarre, h, couleurContenu)
            draw_circle(int(x+lbarre*1.9), int(y+hbarre*0.32), int(lbarre/2), couleurJauge)
            draw_text_ex(police2, str(bat.marins), (int(x+lbarre*1.9-tm.x/2), int(y+hbarre*0.32-tm.y/2)), int(yf*0.03), 0, couleurTexteJauge)
            y += hbarre
            self.gm1.dessine(int(x+lbarre/2-self.gm1.largeur/2), y)
        else:
            x = int(xf/2+self.largeur*0.46)
            if bat.actif:
                draw_rectangle_rounded([int(x-ta.x*1.2), int(y+yf*0.04-ta.y*0.55), int(ta.x*1.2), int(ta.y*1.1)], 0.15, 30, GOLD)
                draw_text_ex(police1i, "ACTIF", (int(x-ta.x*1.1), int(y+yf*0.04-ta.y*0.5)), int(yf*0.025), 0, WHITE)
            draw_texture(bat.images[0], int(x-bat.images[0].width), int(y+hbarre*0.7-bat.images[0].height/2), WHITE)
            draw_rectangle_rounded([int(x-bat.images[0].width), int(y+hbarre*0.7+bat.images[0].height*0.9), int(tt.x*1.1), int(tt.y*1.1)], 0.15, 30, couleurFondRec)
            draw_text_ex(police2, texte, (int(x-bat.images[0].width+tt.x*0.05), int(y+hbarre*0.7+bat.images[0].height*0.9+tt.y*0.05)), int(yf*0.025), 0, couleurTexteRec)
            x -= bat.images[0].width + espace
            draw_texture(self.marin, int(x-lbarre/2-self.marin.width/2), y, WHITE)
            y += self.marin.height
            draw_rectangle(x-lbarre, y, lbarre, hbarre, couleurJauge)
            draw_rectangle(x-lbarre, int(y+hbarre-h), lbarre, h, couleurContenu)
            draw_circle(int(x-lbarre*1.9), int(y+hbarre*0.32), int(lbarre/2), couleurJauge)
            draw_text_ex(police2, str(bat.marins), (int(x-lbarre*1.9-tm.x*0.55), int(y+hbarre*0.32-tm.y/2)), int(yf*0.03), 0, couleurTexteJauge)
            y += hbarre
            self.gm2.dessine(int(x-lbarre/2-self.gm1.largeur/2), y)
        return int(y + self.gm1.hauteur + espace)

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

    def setJoueurs(self, joueurs: list[Joueur]) -> None:
        if joueurs[0].compteBateau() > joueurs[1].compteBateau():
            self.joueurs = joueurs
            self.egalite = False
        elif joueurs[1].compteBateau() > joueurs[0].compteBateau():
            self.joueurs = [joueurs[1], joueurs[0]]
            self.egalite = False
        else:
            self.egalite = True
            self.joueurs = joueurs

    def definiHauteur(self) -> None:
        hauteurTitre = int(yf*0.1)
        self.hauteur = hauteurTitre

    def plusGauche(self) -> None:
        if self.bat[1].marins > 0:
            self.bat[1] - 1
            self.bat[0] + 1

    def plusDroite(self) -> None:
        if self.bat[0].marins > 0:
            self.bat[0] - 1
            self.bat[1] + 1

    def moinsGauche(self) -> None:
        if self.bat[0].marins > 0:
            self.bat[0] - 1
            self.bat[1] + 1

    def moinsDroite(self) -> None:
        if self.bat[1].marins > 0:
            self.bat[1] - 1
            self.bat[0] + 1

    def reset(self) -> None:
        self.bat[0].marins = int(self.valeursInitiales[0])
        self.bat[1].marins = int(self.valeursInitiales[1])

    def annule(self) -> None:
        self.valide = 0
        self.reset()
        self.playAnim = True

    def confirme(self) -> None:
        self.valide = 2
        self.playAnim = True