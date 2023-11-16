from systeme.FondMarin import yf, police1, draw_circle, draw_circle_sector, BLUE, draw_text_ex, WHITE, measure_text_ex

class CptRebours:
    """Le compte à rebours présent sur la page d'intro.
    """
    def __init__(self, depart: int) -> None:
        """Crée le compte à rebours.

        Args:
            depart (int): La valeur de départ du compte à rebours.
        """
        self.multiplicateur = 50
        self.depart = depart
        self.valeur = depart*self.multiplicateur
        self.val = depart
        self.rayon = yf*0.05
        self.taillePolice = self.rayon*1.3
        self.pos = (0, 0)
        self.play = False

    def dessine(self) -> None:
        """Dessine le compte à rebours.
        """
        draw_circle(self.pos[0], self.pos[1], self.rayon, [80, 80, 80, 255])
        draw_circle(self.pos[0], self.pos[1], self.rayon*0.9, [0, 0, 0, 255])
        draw_circle_sector(self.pos, self.rayon*0.9, self.valeur*360/(self.depart*self.multiplicateur)-180, -180, 32, BLUE)
        draw_circle(self.pos[0], self.pos[1], self.rayon*0.8, [80, 80, 80, 255])
        tt = measure_text_ex(police1, self.val, self.taillePolice, 0)
        draw_text_ex(police1, str(self.val), (int(self.pos[0]-tt.x*0.6), int(self.pos[1]-tt.y/2)), self.taillePolice, 0, WHITE)
        if self.play and not self.aFini():
            self.avance()

    def setPos(self, x: int, y: int) -> None:
        """Modifie la position du compte à rebours.

        Args:
            x (int): Nouvel abscisse.
            y (int): Nouvel ordonnée.
        """
        self.pos = (x, y)

    def avance(self) -> None:
        """Décrémente la valeur du compte à rebours.
        """
        self.valeur -= 1
        if self.valeur%self.multiplicateur == 0:
            self.val -= 1

    def run(self) -> None:
        """Active le décompte.
        """
        self.play = True
    
    def pause(self) -> None:
        """Stop le décompte.
        """
        self.play = False

    def reset(self) -> None:
        """Réinitialise le compte à rebours.
        """
        self.play = False
        self.valeur = self.depart*self.multiplicateur
        self.val = self.depart

    def aFini(self) -> bool:
        """Vérifie si le compte à rebours a atteint 0.

        Returns:
            bool: True si le compteur est à 0.
        """
        if self.val == 0:
            return True
        else:
            return False