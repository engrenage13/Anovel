from re import S
from systeme.FondMarin import *

class Article:
    def __init__(self) -> None:
        self.titre = None
        self.texte = []

    def dessine(self, largeur: int) -> None:
        tpoltit = int(yf*0.02)
        tpolice = int(yf*0.015)
        h = 0
        if self.titre != None:
            tti = measure_text_ex(police2, self.titre, tpoltit, 0)
            h += int(tti.y*1.8)
        if len(self.texte) > 0:
            texte = "\n\n".join(self.texte)
        draw_text_ex(police2, self.titre, [xf-int(xf*0.015)-tti.x, int(yf*0.06)], tpoltit, 0, WHITE)

    def decodeur(self, ligne: str) -> list:
        rep = False
        if len(ligne) > 0 and ligne[0] == "#":
            li = ligne.split(" ")
            del li[0]
            self.setTitre(" ".join(li))
        elif ligne == "//art_":
            rep = True
        else:
            self.ajouteTexte([ligne, 't'])
        return rep

    def setTitre(self, titre: str) -> None:
        self.titre = titre

    def ajouteTexte(self, texte: list) -> None:
        self.texte.append(texte)