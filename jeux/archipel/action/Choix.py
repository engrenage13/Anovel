import random
from systeme.FondMarin import is_mouse_button_pressed
from jeux.archipel.action.Action import Action

class Choix(Action):
    def __init__(self, elements: list) -> None:
        super().__init__(elements)

    def verifClic(self) -> None:
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
        self.resultat = random.randint(0, len(self.elements)-1)