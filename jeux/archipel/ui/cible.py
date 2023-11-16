from systeme.FondMarin import draw_rectangle, draw_rectangle_lines_ex, WHITE, is_mouse_button_pressed
from jeux.archipel.ui.objets.plateau.case import Case
from jeux.archipel.ui.objets.Bateau import Bateau

class Cible:
    """Le carré qui permet de placer un bateau sur le plateau.
    """
    def __init__(self, case: Case, bateau: Bateau) -> None:
        """Crée la cible.

        Args:
            case (Case): La case sur laquelle s'affiche la cible.
            bateau (Bateau): Le bateau qui doit être placée.
        """
        self.case = case
        self.bateau = bateau
        self.play = True

    def dessine(self) -> None:
        """Dessine la cible.
        """
        if not self.case.estPleine() and not self.case.marqueur:
            draw_rectangle(self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille, [255, 255, 255, 130])
            draw_rectangle_lines_ex([self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille], 
                                    int(self.case.largeurBordure*2), WHITE)
            self.positionne()
        
    def setCase(self, case: Case) -> None:
        """Modifie la case de la cible.

        Args:
            case (Case): La nouvelle case.
        """
        self.case = case

    def setBateau(self, bateau: Bateau) -> None:
        """Modifie le bateau à placer.

        Args:
            bateau (Bateau): le nouveau bateau qui doit être placer.
        """
        self.bateau = bateau

    def positionne(self) -> None:
        """Place le bateau sur la case si l'utilisateur clique dessus.
        """
        if self.play:
            if is_mouse_button_pressed(0):
                self.case + self.bateau

    def checkBateauEstPlace(self) -> bool:
        """Vérifie si le bateau est placé.

        Returns:
            bool: True si le bateau est sur la case.
        """
        if self.bateau in self.case.contenu:
            return True
        else:
            return False