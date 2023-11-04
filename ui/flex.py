from systeme.FondMarin import *

class Flex:
    def __init__(self, l: tuple[int|str, int] = ("", xf), h: tuple[int|str, int] = ("", yf), de: int = 0, pad: int = 0) -> None:
        self.longueur = self.defini_taille(l[0], l[1])
        self.hauteur = self.defini_taille(h[0], h[1])
        self.padding = pad
        self.direction = de
        self.enfants = []

    def dessine(self, x: int = 0, y: int = 0, couleur: Color = BLANK) -> None:
        pad = self.padding
        draw_rectangle(x, y, self.longueur, self.hauteur, couleur)
        nouv_x = x+pad
        nouv_y = y+pad
        for i in range(len(self.enfants)):
            if i > 0:
                if self.direction == 0:
                    nouv_y += self.enfants[i-1][0].get_dims()[1]
                else:
                    nouv_x += self.enfants[i-1][0].get_dims()[0]
            self.enfants[i][0].dessine(nouv_x, nouv_y, self.enfants[i][1])

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
    
    def ajoute_enfant(self, l: int|str = "", h: int|str = "", de: int = 0, pad: int = 0, couleur: Color = BLANK) -> None:
        self.enfants.append((Flex((l, self.longueur-self.padding*2), (h, self.hauteur-self.padding*2), de, pad), couleur))

    def get_dims(self) -> tuple[int]:
        return (self.longueur, self.hauteur)