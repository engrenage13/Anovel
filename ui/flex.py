from systeme.FondMarin import *

class Flex:
    def __init__(self, l: int|str = "", h: int|str = "") -> None:
        self.longueur = self.definiTaille(l, xf)
        self.hauteur = self.definiTaille(h, yf)

    def dessine(self, couleur: Color = [0, 0, 0, 0]) -> None:
        draw_rectangle(0, 0, self.longueur, self.hauteur, couleur)

    def definiTaille(self, l: int|str, dimMax: int) -> int:
        if type(l) == int:
            rep = l
        elif type(l) == str:
            if l == "":
                rep = dimMax
            elif l[-1] == "%":
                m = int(l[0:-1])/100
                rep = int(dimMax*m)
        return rep