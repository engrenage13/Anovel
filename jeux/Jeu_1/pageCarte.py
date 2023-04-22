from jeux.Jeu_1.objets.bases.fenetre import Fenetre, xf, yf, draw_rectangle

class PageCarte(Fenetre):
    def __init__(self) -> None:
        super().__init__()

    def dessine(self) -> None:
        super().dessine()
        draw_rectangle(0, 0, xf, yf, [144, 132, 78, 85])