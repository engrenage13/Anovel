from jeux.archipel.jeu.plateau.case import Case, TypeCase
from random import choice

class Plateau:
    def __init__(self, taille: int, nbIles: int) -> None:
        self.taille = taille
        self.nbIles = nbIles
        self.cases = []

    def mise_en_place(self) -> None:
        typIles = [type.value for type in TypeCase]
        countIle = 0
        for i in range(self.taille):
            ligne = []
            for j in range(self.taille):
                if countIle < self.nbIles:
                    typIle = choice(typIles)
                    countIle += 1
                else:
                    typIle = TypeCase.MER
                ligne.append(Case(typIle))
            self.cases.append(ligne)