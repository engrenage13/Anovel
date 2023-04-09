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
        self.actuel = 0
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

    def jouer(self, coord: tuple) -> bool:
        bat = self.bateaux[self.actuel]
        if is_mouse_button_pressed(0):
            bat.setPos(coord[0], coord[1])
            self.bateauSuivant()

    def bateauSuivant(self) -> None:
        bat = self.bateaux[self.actuel]
        -bat
        self.actuel += 1
        if self.actuel >= len(self.bateaux):
            self.actuel = 0
            -self
        else:
            +self.bateaux[self.actuel]

    def __pos__(self) -> None:
        self.actif = True
        +self.bateaux[self.actuel]

    def __neg__(self) -> None:
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]