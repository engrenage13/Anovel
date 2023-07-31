from systeme.FondMarin import draw_rectangle, draw_rectangle_lines_ex, WHITE, is_mouse_button_pressed
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.objets.Bateau import Bateau

class Cible:
    def __init__(self, case: Case, bateau: Bateau) -> None:
        self.case = case
        self.bateau = bateau
        self.play = True

    def dessine(self) -> None:
        if not self.case.estPleine() and not self.case.marqueur:
            draw_rectangle(self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille, [255, 255, 255, 130])
            draw_rectangle_lines_ex([self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille], 
                                    int(self.case.largeurBordure*2), WHITE)
            self.positionne()
        
    def setCase(self, case: Case) -> None:
        self.case = case

    def setBateau(self, bateau: Bateau) -> None:
        self.bateau = bateau

    def positionne(self) -> None:
        if self.play:
            if is_mouse_button_pressed(0):
                self.case + self.bateau

    def checkBateauEstPlace(self) -> bool:
        if self.bateau in self.case.contenu:
            return True
        else:
            return False