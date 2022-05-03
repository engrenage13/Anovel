from random import choice, randint
from FondMarin import *

class Paillette:
    def __init__(self, zone: tuple, couleurs: list):
        self.zone = zone
        self.taille = 0
        self.couleurs = couleurs
        self.mode = True
        self.horloge = 0
        self.setParam()

    def setParam(self):
        self.position = (randint(0, self.zone[0]), randint(0, self.zone[1]))
        self.max = randint(15, 45)
        self.couleur = choice(self.couleurs)
        
    def dessine(self):
        draw_poly(self.position, 4, self.taille, 0, self.couleur)
        self.redim()

    def redim(self):
        if self.mode and self.horloge == 0:
            if self.taille < self.max:
                self.taille = self.taille + 1
            else:
                self.mode = False
                self.horloge = self.horloge + 1
        elif self.horloge > 0:
            if self.horloge < randint(40, 60):
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