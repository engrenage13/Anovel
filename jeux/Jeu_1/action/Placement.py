import random
from systeme.FondMarin import is_mouse_button_pressed
from jeux.Jeu_1.action.Action import Action
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.objets.Bateau import Bateau

class Placement(Action):
    def __init__(self, bateaux: list[Bateau], cases: list[Case]) -> None:
        self.bateaux = bateaux
        self.cases = cases
        self.etape = 1
        self.resultat = [None, None, 0]

    def verifClic(self) -> None:
        if is_mouse_button_pressed(0):
            i = 0
            trouve = False
            if self.etape == 1:
                elements = self.bateaux
            else:
                elements = self.cases
            while i < len(elements) and not trouve:
                if elements[i].getContact():
                    trouve = True
                    if self.etape == 1:
                        self.resultat[0] = i
                    else:
                        self.resultat[1] = i
                        self.etape = 2
                else:
                    i += 1

    def estFinie(self) -> bool:
        if self.resultat[0] == None or self.resultat[1] == None:
            return False
        else:
            return True

    def passe(self) -> None:
        self.resultat[0] = 0
        self.resultat[1] = random.randint(0, len(self.cases)-1)
        self.resultat[2] = random.randint(0, 3)