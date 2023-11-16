import random
from systeme.FondMarin import is_mouse_button_pressed
from jeux.archipel.action.Action import Action
from jeux.archipel.ui.objets.plateau.case import Case
from jeux.archipel.ui.objets.Bateau import Bateau

class Placement(Action):
    """Action permettant de placer des éléments en jeu.

    Args:
        Action (Action): Hérite de la structure d'une action.
    """
    def __init__(self, bateaux: list[Bateau], cases: list[Case]) -> None:
        """Crée une action de placement.

        Args:
            bateaux (list[Bateau]): Les bateaux qu'il faut placer.
            cases (list[Case]): Les cases sur les-quelles il faut placer les bateaux.
        """
        self.bateaux = bateaux
        self.cases = cases
        self.etape = 1
        self.resultat = [None, None, 0]

    def verifClic(self) -> None:
        """Vérifie si l'utilisateur a cliqué sur un bateau ou une case.
        """
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
        """Vérifie si l'action est terminée.

        Returns:
            bool: True si l'action est terminée.
        """
        if self.resultat[0] == None or self.resultat[1] == None:
            return False
        else:
            return True

    def passe(self) -> None:
        """Choisis un bateau au hasard dans la liste et le place sur l'une des cases au hasard.
        """
        self.resultat[0] = 0
        self.resultat[1] = random.randint(0, len(self.cases)-1)
        self.resultat[2] = random.randint(0, 3)