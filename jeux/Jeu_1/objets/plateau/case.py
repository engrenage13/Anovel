from systeme.FondMarin import *
from jeux.Jeu_1.fonctions.bases import TAILLECASE

class Case:
    def __init__(self, x: int = 0, y: int = 0, taille: int = TAILLECASE) -> None:
        self.pos = (x, y)
        self.taille = taille

    def dessine(self) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [48, 140, 201, 255])
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], 1.5, [80, 80, 80, 150])

    def deplace(self, x: int, y: int) -> None:
        self.pos = (self.pos[0]+x, self.pos[1]+y)