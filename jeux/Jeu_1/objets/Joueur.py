from random import shuffle
from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.config import bateaux as libat
#from ui.blocTexte import BlocTexte

class Joueur():
    def __init__(self, nom: str, bateaux: list, couleur: Color):
        """Crée un joueur.

        Args:
            nom (str): Le nom du joueur.
            bateaux (list): Ses bateaux.
            couleur (Color): Sa couleur.
        """
        self.nom = nom
        self.couleur = couleur
        self.bateaux = []
        # bateaux
        for i in range(len(bateaux)):
            bateau = libat[bateaux[i]]
            bat = Bateau(bateau["nom"], bateau["image"], bateau["vie"], bateau["marins"], bateau["pm"])
            self.bateaux.append(bat)
        self.actuel = 0
        shuffle(self.bateaux)
        # /bateaux
        self.actif = False
        self.phase = "installation"

    def dessine(self) -> None:
        if self.phase != "installation":
            for i in range(len(self.bateaux)):
                self.bateaux[i].dessine()

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.actif = False
        self.phase = "installation"
        for i in range(len(self.bateaux)):
            self.bateaux[i].rejouer()
        shuffle(self.bateaux)

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
        if self.phase != "installation":
            +self.bateaux[self.actuel]

    def __neg__(self) -> None:
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]