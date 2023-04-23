from jeux.Jeu_1.objets.plateau.case import Case, draw_rectangle, draw_rectangle_lines
from jeux.Jeu_1.fonctions.bases import TAILLEPETITECASE

class PtiteCase(Case):
    def __init__(self, x: int = 0, y: int = 0, taille: int = TAILLEPETITECASE) -> None:
        super().__init__(x, y)
        self.couleur = [0, 0, 0, 50]
        self.taille = taille

    def dessine(self) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleur)
        draw_rectangle_lines(self.pos[0], self.pos[1], self.taille, self.taille, [0, 0, 0, 150])
        """if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                self.contenu[i].dessine()"""