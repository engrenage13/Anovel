from systeme.FondMarin import *

class Flex:
    def __init__(self, l: tuple[int|str, int] = ("", xf), h: tuple[int|str, int] = ("", yf)) -> None:
        self.longueur = self.defini_taille(l[0], l[1])
        self.hauteur = self.defini_taille(h[0], h[1])
        self.enfants = []

    def dessine(self, couleur: Color = BLANK) -> None:
        draw_rectangle(0, 0, self.longueur, self.hauteur, couleur)
        for i in range(len(self.enfants)):
            self.enfants[i][0].dessine(self.enfants[i][1])

    def defini_taille(self, l: int|str, dimMax: int) -> int:
        if type(l) == int:
            rep = l
        elif type(l) == str:
            if l == "":
                rep = dimMax
            elif l[-1] == "%":
                m = int(l[0:-1])/100
                rep = int(dimMax*m)
        return rep
    
    def ajoute_enfant(self, l: int|str = "", h: int|str = "", couleur: Color = BLANK) -> None:
        self.enfants.append((Flex((l, self.longueur), (h, self.hauteur)), couleur))