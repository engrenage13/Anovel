from systeme.FondMarin import *
from objets.BateauJoueur import *

class Tiroir:
    def __init__(self) -> None:
        self.liste = []
        self.largeur = int(xf*0.16)
        self.positions = [(1, [50]), (2, [30, 70]), (3, [20, 50, 80]), (4, [15, 37, 63, 85]), 
                          (5, [10, 30, 50, 70, 90])]

    def dessine(self, y: int) -> None:
        if len(self.liste) > 0:
            tCase = 1.6*tailleCase
            originex = -20
            originey = y-int(tCase/2*len(self.liste))
            tailley = int(tCase*len(self.liste))
            draw_rectangle_rounded_lines((originex, originey, self.largeur, tailley), 0.2, 30, 3, WHITE)
            for i in range(len(self.liste)):
                xbat = 0
                if self.liste[i].originale.width >= (self.largeur+originex)*0.9:
                    xbat = int((self.largeur+originex)*0.9-self.liste[i].originale.width)
                ybat = int(tailley*(self.positions[len(self.liste)-1][1][i]/100)+originey)
                self.liste[i].dessine(xbat, ybat-int(self.liste[i].originale.height/2))

    def setListe(self, liste: list) -> None:
        self.liste = liste

    def supValListe(self, indice: int) -> None:
        if indice >= 0 and indice < len(self.liste):
            del self.liste[indice]

    def ajValListe(self, valeur: BateauJoueur) -> None:
        self.liste.append(valeur)