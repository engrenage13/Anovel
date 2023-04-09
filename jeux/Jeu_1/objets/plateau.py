from systeme.FondMarin import xf, yf, draw_rectangle

class Plateau:
    def __init__(self) -> None:
        self.longueur = xf
        self.hauteur = yf
        # Lien Menu
        self.bloque = False

    def dessine(self, x: int, y: int) -> None:
        px = x
        py = y
        draw_rectangle(px, py, self.longueur, self.hauteur, [39, 86, 127, 255])