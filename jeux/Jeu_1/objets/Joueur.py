from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.config import bateaux as libat
from ui.blocTexte import BlocTexte

class Joueur:
    def __init__(self, nom: str, bateaux: list[Bateau], couleur: Color):
        """Crée un joueur.

        Args:
            nom (str): Le nom du joueur.
            bateaux (list): Ses bateaux.
            couleur (Color): Sa couleur.
        """
        self.nom = nom
        self.titre = BlocTexte(nom, police1, int(yf*0.04), [int(xf*0.1), int(yf*0.06)])
        self.couleur = couleur
        self.btx = bateaux
        self.rejouer()

    def dessine(self) -> None:
        # ui
        draw_rectangle_rounded([int(yf*0.01), int(yf*0.01), int(xf*0.1), int(yf*0.06)], 0.15, 30, [255, 255, 255, 170])
        self.titre.dessine([[int(yf*0.01+xf*0.05), int(yf*0.01+yf*0.025)], 'c'], self.couleur)

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.actif = False
        self.phase = "placement"
        self.bateaux = []
        self.nbelimination = 0
        # bateaux
        for i in range(len(self.btx)):
            bateau = libat[self.btx[i]]
            bat = Bateau(bateau["nom"], bateau["image"], bateau["vie"], bateau["marins"], bateau["pm"], bateau["degats"], self.couleur, i+1)
            self.bateaux.append(bat)

    def bateauSuivant(self) -> None:
        if self.actuel < len(self.bateaux):
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
        if i < len(self.bateaux):
            self.actuel = i
        else:
            self.actuel = 0

    def tourFini(self) -> bool:
        i = 0
        fin = True
        while i < len(self.bateaux) and fin:
            if not self.bateaux[i].aFini():
                fin = False
            else:
                i += 1
        return fin
    
    def compteBateau(self) -> int:
        compteur = 0
        for i in range(len(self.bateaux)):
            bat = self.bateaux[i]
            if bat.estEnVie():
                compteur += 1
        return compteur
    
    def setIds(self) -> None:
        for i in range(len(self.bateaux)):
            self.bateaux[i].id = i+1

    def __pos__(self) -> None:
        self.actif = True
        if self.phase != "placement":
            i = 0
            while i < len(self.bateaux):
                if self.bateaux[i].coule:
                    del self.bateaux[i]
                else:
                    self.bateaux[i].finiTour = False
                    i += 1
            if len(self.bateaux) > 0:
                +self.bateaux[self.actuel]

    def __neg__(self) -> None:
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]

    def __getitem__(self, key) -> Bateau|bool:
        if key < len(self.bateaux):
            return self.bateaux[key]
        else:
            return False
    
    def __len__(self) -> int:
        return len(self.bateaux)
    
    def __add__(self, bateau: Bateau) -> int:
        self.bateaux.append(bateau)
        bateau.finiTour = False
        bateau.couleur = self.couleur
        self.setIds()
        return len(self.bateaux)
    
    def __sub__(self, bateau: Bateau) -> int:
        if bateau in self.bateaux:
            del self.bateaux[self.bateaux.index(bateau)]
        self.setIds()
        return len(self.bateaux)