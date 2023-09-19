import random
from systeme.FondMarin import is_mouse_button_pressed
from jeux.archipel.action.Action import Action

class Choix(Action):
    """Un choix est un type d'Action.

    Args:
        Action (Action): Hérite de la structure d'une action.
    """
    def __init__(self, elements: list) -> None:
        """Crée une action de choix.

        Args:
            elements (list): Tous les éléments que l'on peut choisir.
        """
        super().__init__(elements)

    def verifClic(self) -> None:
        """Vérifi si l'utilisateur clic sur l'un des éléments.
        """
        if is_mouse_button_pressed(0):
            i = 0
            trouve = False
            while i < len(self.elements) and not trouve:
                if self.elements[i].getContact():
                    trouve = True
                    self.resultat = i
                else:
                    i += 1

    def passe(self) -> None:
        """Choisi un élément au hasard parmis tous ceux qui sont possible.
        """
        self.resultat = random.randint(0, len(self.elements)-1)