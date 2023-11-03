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

    def check_case_existe(self, case: tuple[int]) -> bool:
        existe = False
        if type(case) == tuple[int] and len(case) >= 2:
            if case[0] < self.taille and case[1] < len(self.cases[case[0]]):
                existe = True
        return existe

    def __getitem__(self, key: int) -> list[Case]|bool:
        if key < len(self.cases):
            return self.cases[key]
        else:
            return False
        
    def __len__(self) -> int:
        return len(self.cases)