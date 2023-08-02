from jeux.archipel.fonctions.deplacement import regleVitesse

class Bougeable:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.pos = (x, y)

    def deplace(self, x: int, y: int) -> None:
        self.setPos(self.pos[0]+x, self.pos[1]+y)

    def deplaceGlisse(self, destination: tuple[int], vitesse: int = 1) -> None:
        x = self.pos[0]
        y = self.pos[1]
        dx = destination[0]
        dy = destination[1]
        vitx = regleVitesse(x, dx, vitesse)
        vity = regleVitesse(y, dy, vitesse)
        if x < dx:
            x += vitx
        elif x > dx:
            x -= vitx
        if y < dy:
            y += vity
        elif y > dy:
            y -= vity
        self.pos = (x, y)

    def setPos(self, x: int, y: int) -> None:
        self.pos = (x, y)