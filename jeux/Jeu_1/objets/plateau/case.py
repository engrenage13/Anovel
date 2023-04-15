import random
from systeme.FondMarin import *
from jeux.Jeu_1.fonctions.bases import TAILLECASE, EAUX

class Case:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.pos = (x, y)
        self.taille = TAILLECASE
        self.couleur = random.choice(EAUX)
        self.contenu = []

    def dessine(self) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleur)
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], 1.5, [80, 80, 80, 150])
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                self.contenu[i].dessine()

    def deplace(self, x: int, y: int) -> None:
        self.setPos(self.pos[0]+x, self.pos[1]+y)

    def setPos(self, x: int, y: int) -> None:
        self.pos = (x, y)
        if len(self.contenu) > 0:
            if len(self.contenu) == 1:
                self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/2))
            else:
                if self.contenu[0].direction%2 == 0:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/10*3))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/10*7))
                else:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/10*3), int(self.pos[1]+self.taille/2))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/10*7), int(self.pos[1]+self.taille/2))

    def retire(self, element) -> bool:
        rep = False
        if element in self.contenu:
            rep = True
            del self.contenu[self.contenu.index(element)]
        return rep

    def ajoute(self, contenu) -> bool:
        rep = True
        if len(self.contenu) > 0:
            if len(self.contenu) >= 2:
                rep = False
            elif self.contenu[0].direction%2 == contenu.direction%2:
                self.contenu.append(contenu)
            else:
                rep = False
        else:
            self.contenu.append(contenu)
        if rep:
            self.setPos(self.pos[0], self.pos[1])
        return rep

    def estPleine(self) -> bool:
        if len(self.contenu) == 2:
            return True
        else:
            return False
        
    def __add__(self, element):
        return self.ajoute(element)

    def __sub__(self, element):
        self.retire(element)