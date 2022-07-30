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
        self.balises = ['//', 'i/', '!/']
        self.types = ['cad', 'ast', 'imp']

    def dessine(self, x: int, y: int) -> None:
        l = self.largeur
        h = self.hauteur
        ph = y
        draw_rectangle(x, y, l, h, [105, 105, 105, 170])
        if self.titre != "":
            tti = measure_text_ex(police2, self.titre, self.taillePolice[0], 0)
            draw_rectangle(x, y, l, int(tti.y*1.4), [100, 100, 100, 170])
            draw_text_ex(police2, self.titre, [int(x+l/2-tti.x/2), int(ph+tti.y*0.2)], self.taillePolice[0], 
                         0, WHITE)
            ph = int(ph + tti.y*1.4 + self.espace)
        ph + self.espace
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                type = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                pt = [int(x+l*0.025), ph]
                if type in self.types:
                    couleur = [20, 20, 20, 165]
                    if type == 'ast':
                        couleur = [82, 73, 245, 165]
                    elif type == 'imp':
                        couleur = [244, 80, 77, 165]
                    draw_rectangle(int(x+l*0.025), ph, int(l*0.95), int(tt[1]+self.espace), couleur)
                    pt = [int(x+l*0.05), int(ph+self.espace/2)]
                alig = 'g'
                if type in self.types and contenu.getNbLignes() == 1:
                    alig = 'c'
                contenu.dessine([pt, 'no'], alignement=alig)
                nbEspace = 1
                if type in self.types:
                    nbEspace = 2
                ph = int(ph + tt[1] + self.espace*nbEspace)

    def getDims(self) -> list:
        h = self.espace
        if self.titre != "":
            ttit = measure_text_ex(police2, self.titre, self.taillePolice[0], 0)
            h = h + ttit.y + self.espace
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                type = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                nbEspace = 1
                if type in self.types:
                    nbEspace = 2
                h = h + tt[1] + self.espace*nbEspace
        if self.hauteur != h:
            self.redim(self.largeur, h)
        return [self.largeur, h]

    def decodeur(self, ligne: str) -> list:
        rep = False
        li = ligne.split(" ")
        if len(ligne) > 0 and ligne[0] == "#":
            del li[0]
            self.setTitre(" ".join(li))
        elif ligne == "//art_":
            rep = True
        elif li[0] in self.balises:
            balise = self.types[self.balises.index(li[0])]
            del li[0]
            self.ajouteContenu([balise, BlocTexte(" ".join(li), police2, self.taillePolice[1], 
                               [int(self.largeur*0.9), ''])])
        elif ligne != "":
            self.ajouteContenu(['t', BlocTexte(ligne, police2, self.taillePolice[1], 
                               [int(self.largeur*0.95), ''])])
        return rep

    def setTitre(self, titre: str) -> None:
        self.titre = titre

    def ajouteContenu(self, contenu: str) -> None:
        self.contenu.append(contenu)

    def redim(self, x: int, y: int) -> None:
        self.largeur = int(x)
        self.hauteur = int(y)