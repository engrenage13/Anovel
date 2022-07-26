from ui.blocTexte import BlocTexte
from systeme.FondMarin import *

class Article:
    def __init__(self) -> None:
        self.titre = ""
        self.contenu = []
        self.largeur = 0
        self.hauteur = 0
        self.espace = int(yf*0.03)
        self.taillePolice = [int(yf*0.055), int(yf*0.035)]

    def dessine(self, x: int, y: int) -> None:
        l = self.largeur
        h = self.hauteur
        ph = y + self.espace
        draw_rectangle_rounded([x, y, l, h], 0.2, 30, [105, 105, 105, 170])
        if self.titre != "":
            tti = measure_text_ex(police2, self.titre, self.taillePolice[0], 0)
            draw_text_ex(police2, self.titre, [int(x+l/2-tti.x/2), ph], self.taillePolice[0], 0, WHITE)
            ph = ph + tti.y + self.espace
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                tt = self.contenu[i].getDims()
                draw_rectangle_rounded([int(x+l*0.025), ph, int(l*0.95), tt[1]+self.espace], 
                                       0.4, 30, [20, 20, 20, 167])
                self.contenu[i].dessine([[int(x+l*0.05), int(ph+self.espace/2)], 'no'], alignement='g')
                ph = ph + tt[1] + self.espace*2

    def getDims(self) -> list:
        h = self.espace
        if self.titre != "":
            ttit = measure_text_ex(police2, self.titre, self.taillePolice[0], 0)
            h = h + ttit.y + self.espace
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                tt = self.contenu[i].getDims()
                h = h + tt[1] + self.espace*2
        if self.hauteur != h:
            self.redim(self.largeur, h)
        return [self.largeur, h]

    def decodeur(self, ligne: str) -> list:
        rep = False
        if len(ligne) > 0 and ligne[0] == "#":
            li = ligne.split(" ")
            del li[0]
            self.setTitre(" ".join(li))
        elif ligne == "//art_":
            rep = True
        elif ligne != "":
            self.ajouteContenu(BlocTexte(ligne, police2, self.taillePolice[1], 
                               [int(self.largeur*0.9), '']))
        return rep

    def setTitre(self, titre: str) -> None:
        self.titre = titre

    def ajouteContenu(self, contenu: str) -> None:
        self.contenu.append(contenu)

    def redim(self, x: int, y: int) -> None:
        self.largeur = x
        self.hauteur = y