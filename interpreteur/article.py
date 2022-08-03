from ui.blocTexte import BlocTexte
from systeme.FondMarin import *

class Article:
    def __init__(self) -> None:
        """Créu un article pour la fenêtre de l'interpréteur.
        """
        self.titre = ""
        self.contenu = []
        self.largeur = 0
        self.hauteur = 0
        self.hauteurCadre = 0
        self.espace = int(yf*0.03)
        self.taillePolice = [int(yf*0.055), int(yf*0.035)]
        self.balises = ['//', 'i/', '!/']
        self.types = ['cad', 'ast', 'imp']

    def dessine(self, x: int, y: int) -> None:
        """Dessine l'article.

        Args:
            x (int): Position en abscisse du coin en haut à gauche de l'article.
            y (int): Position en ordonnée du coin en haut à droite de l'article.
        """
        l = self.largeur
        hc = self.hauteurCadre
        ph = y
        if self.titre != "":
            tti = measure_text_ex(police2, self.titre, self.taillePolice[0], 0)
            draw_text_ex(police2, self.titre, [int(x+l/2-tti.x/2), int(ph+tti.y*0.2)], self.taillePolice[0], 
                         0, [0, 255, 255, 255])
            ph = int(ph + tti.y + self.espace)
        draw_rectangle_rounded([x, ph, l, hc], 0.1, 30, [200, 200, 200, 170])
        ph = ph + self.espace
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                type = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                pt = [int(x+l*0.025), ph]
                if type in self.types:
                    couleur = [20, 20, 20, 145]
                    if type == 'ast':
                        couleur = [22, 29, 124, 145]
                    elif type == 'imp':
                        couleur = [145, 18, 18, 145]
                    draw_rectangle_rounded([int(x+l*0.025), ph, int(l*0.95), int(tt[1]+self.espace)], 
                                           0.2, 30, couleur)
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
        """Permet de mesurer la taille de l'article.

        Returns:
            list: Les dimensions de l'article.
        """
        h = self.espace
        hc = h
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
                hc = hc + tt[1] + self.espace*nbEspace
        if self.hauteur != h + hc:
            self.redim(self.largeur, h+hc)
            self.hauteurCadre = hc
        return [self.largeur, h+hc]

    def decodeur(self, ligne: str) -> bool:
        """Décode les lignes du fichier proposées (rapport avec un Article).

        Args:
            ligne (str): Ligne à décoder

        Returns:
            bool: True si la on quitte le mode Article dans le décodeur de l'interpréteur.
        """
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
        """Modifie le titre de l'article.

        Args:
            titre (str): Le nouveau titre à mettre en place.
        """
        self.titre = titre

    def ajouteContenu(self, contenu: str) -> None:
        """Ajoute du contenu dans l'article.

        Args:
            contenu (str): Le contenu à ajouter.
        """
        self.contenu.append(contenu)

    def redim(self, x: int, y: int) -> None:
        """Permet de redimensionner un Article.

        Args:
            x (int): Nouvelle largeur.
            y (int): Nouvelle hauteur.
        """
        self.largeur = int(x)
        self.hauteur = int(y)