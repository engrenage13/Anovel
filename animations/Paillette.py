from random import choice, randint
from systeme.FondMarin import *

class Paillette:
    def __init__(self, zone: tuple, couleurs: list):
        """Crée une paillette (objet d'animation).

        Args:
            zone (tuple): Zone dans laquelle la paillette peut apparaître.
            couleurs (list): Couleurs possibles pour la paillette.
        """
        self.zone = zone
        self.taille = 0
        self.couleurs = couleurs
        self.mode = True
        self.horloge = 0
        self.setParam()

    def setParam(self):
        """Modifie certains paramètres importants de la paillette.
        """
        self.max = randint(3, 15)
        self.position = (randint(self.zone[0]+self.max, self.zone[2]-self.max), 
                         randint(self.zone[1]+self.max, self.zone[3]-self.max))
        self.couleur = choice(self.couleurs)
        
    def dessine(self):
        """Dessine la paillette.
        """
        draw_poly(self.position, 4, self.taille, 0, self.couleur)
        self.redim()

    def redim(self):
        """Gère l'anim de la paillette.
        """
        if self.mode and self.horloge == 0:
            if self.taille < self.max:
                self.taille = self.taille + 1
            else:
                self.mode = False
                self.horloge = self.horloge + 1
        elif self.horloge > 0:
            if self.horloge < randint(7, 15):
                self.horloge = self.horloge + 1
            else:
                self.horloge = 0
        else:
            if self.taille > 0:
                self.taille = self.taille - 1
            else:
                self.mode = True
                self.horloge = self.horloge + 1
                self.setParam()