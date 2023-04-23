from systeme.FondMarin import draw_rectangle, BLACK, Color, xf, yf

class Fenetre:
    def __init__(self, fond: Color = BLACK) -> None:
        self.boutons = []
        self.fond = fond

    def dessine(self) -> None:
        draw_rectangle(0, 0, xf, yf, self.fond)

    def estFini(self) -> bool:
        return False