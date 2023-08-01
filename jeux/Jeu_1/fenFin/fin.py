from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.objets.Joueur import Joueur
from jeux.Jeu_1.fenFin.blocJoueur import BlocJoueur

class Fin:
    def __init__(self, joueurs: list[Joueur]) -> None:
        self.setJoueurs(joueurs)
        # Boutons
        self.opt = [Bouton(TB1o, BTV, "QUITTER", '', [self.quitte]),
                    Bouton(TB1o, BTV, "REJOUER", '', [self.reset])]
        self.gm1 = Grille(int(xf*0.44), [False])
        self.gm1.ajouteElement(self.opt[0], 0, 0)
        self.gm1.ajouteElement(self.opt[1], 1, 0)
        # connexion
        self.message = 0
        self.lu = False
        # Animations
        self.resetAnim()

    def dessine(self) -> None:
        draw_rectangle(0, 0, xf, yf, [14, 27, 63, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        tt = measure_text_ex(police1i, "CLASSEMENT FINAL", yf*0.06, 0)
        draw_text_ex(police1i, "CLASSEMENT FINAL", (int(xf/2-tt.x/2), int(yf*0.015)), yf*0.06, 0, [250, 248, 220, self.opac[0]])
        for i in range(len(self.blocs)):
            bloc = self.blocs[i]
            bloc.dessine(int(xf/2-bloc.getDims()[0]/2), y)
            y += bloc.getDims()[1] + ecart
        draw_line_ex((int(xf/2-xf*0.22), y), (int(xf/2+xf*0.22), y), 2, GRAY)
        y += 2 + ecart
        self.gm1.dessine(int(xf/2-self.gm1.largeur/2), y)
        if is_key_pressed(32):
            self.quitte()
        elif is_key_pressed(82):
            self.reset()
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

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
        self.joueurs = [joueurs[0]]
        for i in range(len(joueurs)-1):
            j1 = self.joueurs[0]
            j2 = joueurs[i+1]
            if j2.compteBateau() > j1.compteBateau():
                self.joueurs = [j2] + self.joueurs
            elif j1.compteBateau() > j2.compteBateau():
                self.joueurs.append(j2)
            else:
                if j2.nbelimination > j1.nbelimination:
                    self.joueurs = [j2] + self.joueurs
                else:
                    self.joueurs.append(j2)
        classement = 1
        self.blocs = []
        for j in range(len(self.joueurs)):
            self.blocs.append(BlocJoueur(self.joueurs[j], classement))
            if j < len(self.joueurs)-1:
                if self.joueurs[j].compteBateau() > self.joueurs[j+1].compteBateau():
                    classement += 1

    def resetAnim(self) -> None:
        self.playAnim = True
        self.ok = False
        self.opac = [0, 254]
        self.hauteurContenu = [int(yf*1.1), int(yf*0.11)]

    def reset(self) -> None:
        self.message = 1
        self.lu = False
        self.resetAnim()

    def quitte(self) -> None:
        self.message = 2
        self.lu = False
        self.resetAnim()

    def regarde(self) -> int:
        if not self.lu:
            self.lu = True
            rep = self.message
        else:
            rep = 0
        return rep