from random import shuffle
from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from ui.blocTexte import BlocTexte

class Joueur():
    def __init__(self, code: int, bateaux: list):
        """Crée un joueur.

        Args:
            code (int): L'identifiant numérique du joueur.
        """
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.bateaux = []
        self.viseur = BlocTexte("x", police2, int(yf*0.04))
        # bateaux
        urlBats = 'jeux/Jeu_1/images/Bateaux/'
        for i in range(len(bateaux)):
            for j in range(bateaux[i][1]):
                bat = Bateau(urlBats+bateaux[i][0]+".png")
                bat.tourne()
                if code > 1:
                    bat.tourne()
                    bat.tourne()
                self.bateaux.append(bat)
        # /bateaux
        self.rejouer()

    def dessine(self) -> None:
        for i in range(len(self.bateaux)):
            self.bateaux[i].dessine()

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.actif = False
        for i in range(len(self.bateaux)):
            self.bateaux[i].rejouer()
        shuffle(self.bateaux)
        self.placeBateau()

    def placeBateau(self) -> None:
        if self.id == 1:
            x = int(xf*0.08)
        else:
            x = int(xf*0.92)
        y = int(yf*0.2)
        for i in range(len(self.bateaux)):
            bateau = self.bateaux[i]
            bateau.pos = [x, y]
            y += int(yf*0.15)

    def jouer(self, dest: tuple) -> bool:
        bat = self.bateaux[0]
        x = bat.pos[0]
        y = bat.pos[1]
        draw_line(x, y, dest[0], dest[1], WHITE)
        draw_circle(x, y, yf*0.005, WHITE)
        self.viseur.dessine([[dest[0], int(dest[1]-self.viseur.getDims()[1]/4)], 'c'])

    def __pos__(self) -> None:
        self.actif = True
        +self.bateaux[0]

    def __neg__(self) -> None:
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]