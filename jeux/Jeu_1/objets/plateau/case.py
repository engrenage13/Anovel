import random
from systeme.FondMarin import *
from jeux.Jeu_1.fonctions.bases import TAILLECASE, EAUX

class Case:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.pos = (x, y)
        self.taille = TAILLECASE
        self.couleur = random.choice(EAUX)

    def dessine(self) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleur)
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], 1.5, [80, 80, 80, 150])

    def deplace(self, x: int, y: int) -> None:
        self.pos = (self.pos[0]+x, self.pos[1]+y)