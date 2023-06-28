from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from ui.blocTexte import BlocTexte
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.objets.Joueur import Joueur
from jeux.Jeu_1.fenFin.blocJoueur import BlocJoueur

class Fin:
    def __init__(self, joueurs: list[Joueur]) -> None:
        self.setJoueurs(joueurs)
        # Autres
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
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 254]
        self.hauteurContenu = [int(yf*1.1), int(yf*0.11)]

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
            else:
                self.joueurs.append(j2)
        classement = 1
        self.blocs = []
        for j in range(len(self.joueurs)):
            self.blocs.append(BlocJoueur(self.joueurs[j], classement))
            if j < len(self.joueurs)-1:
                if self.joueurs[j].compteBateau() > self.joueurs[j+1].compteBateau():
                    classement += 1

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