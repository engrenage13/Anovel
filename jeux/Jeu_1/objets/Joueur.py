from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.config import bateaux as libat
from ui.blocTexte import BlocTexte

class Joueur():
    def __init__(self, nom: str, bateaux: list, couleur: Color):
        """Crée un joueur.

        Args:
            nom (str): Le nom du joueur.
            bateaux (list): Ses bateaux.
            couleur (Color): Sa couleur.
        """
        self.nom = nom
        self.titre = BlocTexte(nom, police1, int(yf*0.04), [int(xf*0.1), int(yf*0.06)])
        self.couleur = couleur
        self.bateaux = []
        # bateaux
        for i in range(len(bateaux)):
            bateau = libat[bateaux[i]]
            bat = Bateau(bateau["nom"], bateau["image"], bateau["vie"], bateau["marins"], bateau["pm"], self.couleur, i+1)
            self.bateaux.append(bat)
        self.actuel = 0
        # /bateaux
        self.actif = False
        self.phase = "installation"

    def dessine(self) -> None:
        # ui
        draw_rectangle_rounded([int(yf*0.01), int(yf*0.01), int(xf*0.1), int(yf*0.06)], 0.15, 30, [255, 255, 255, 170])
        self.titre.dessine([[int(yf*0.01+xf*0.05), int(yf*0.01+yf*0.025)], 'c'], self.couleur)

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.actif = False
        self.phase = "installation"
        for i in range(len(self.bateaux)):
            self.bateaux[i].rejouer()

    def jouer(self, coord: tuple) -> bool:
        bat = self.bateaux[self.actuel]
        if is_mouse_button_pressed(0):
            bat.setPos(coord[0], coord[1])
            self.bateauSuivant()

    def bateauSuivant(self) -> None:
        -self.bateaux[self.actuel]
        if not self.tourFini():
            self.prochainBateau()
            +self.bateaux[self.actuel]
        else:
            self.actuel = 0
            -self

    def estEnPlace(self) -> bool:
        place = True
        i = 0
        while i < len(self.bateaux) and place:
            if not self.bateaux[i].estEnPlace():
                place = False
            else:
                i += 1
        return place
    
    def prochainBateau(self) -> None:
        i = self.actuel+1
        trouve = False
        while i < len(self.bateaux) and not trouve:
            if not self.bateaux[i].aFini():
                trouve = True
                self.actuel = i
            else:
                i += 1
        if not trouve:
            self.actuel = 0
            if self.bateaux[0].aFini():
                self.prochainBateau()

    def tourFini(self) -> bool:
        i = 0
        fin = True
        while i < len(self.bateaux) and fin:
            if not self.bateaux[i].aFini():
                fin = False
            else:
                i += 1
        return fin

    def __pos__(self) -> None:
        self.actif = True
        if self.phase != "installation":
            for i in range(len(self.bateaux)):
                self.bateaux[i].finiTour = False
            +self.bateaux[self.actuel]

    def __neg__(self) -> None:
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]

    def __getitem__(self, key) -> Bateau:
        return self.bateaux[key]
    
    def __len__(self) -> int:
        return len(self.bateaux)