from systeme.FondMarin import *

class Fenetre:
    def __init__(self, titre: str) -> None:
        self.titre = titre

    def dessine(self) -> None:
        l = int(xf*0.7)
        h = int(yf*0.8)
        draw_rectangle(0, 0, xf, yf, [0, 0, 0, 200])
        draw_rectangle_rounded([int(xf/2-l/2), int(yf/2-h/2), l, h], 0.2, 30, [23, 31, 49, 255])