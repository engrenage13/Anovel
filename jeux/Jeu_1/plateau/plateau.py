from systeme.FondMarin import xf, draw_rectangle, BLUE

class Plateau:
    def __init__(self) -> None:
        self.tplateau = 6
        self.tcase = int(xf*0.2)
        # pump up the jam
        self.bloque = False

    def dessine(self, x: int, y: int) -> None:
        px = x
        py = y
        for i in range(self.tplateau):
            for j in range(self.tplateau):
                draw_rectangle(px, py, self.tcase, self.tcase, [39, 86, 127, 255])
                px += self.tcase
            py += self.tcase
            px = x