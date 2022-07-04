from systeme.FondMarin import *
from objets.BateauJoueur import *

class Tiroir:
    def __init__(self) -> None:
        self.liste = []
        self.positions = [(1, [50]), (2, [30, 70]), (3, [20, 50, 80]), (4, [15, 37, 63, 85]), 
                          (5, [10, 30, 50, 70, 90])]
        # Graphique
        self.tCase = 1.6*tailleCase
        self.originex = -20
        self.largeur = int(xf*0.16)
        # Images
        coraux = load_image('images/decors/coraux1.png')
        ratio = self.largeur/coraux.width
        image_resize(coraux, int(coraux.width*ratio), int(coraux.height*ratio))
        self.coraux = load_texture_from_image(coraux)

    def dessine(self, y: int) -> None:
        if len(self.liste) > 0:
            originey = y-int(self.tCase/2*len(self.liste))
            tailley = int(self.tCase*len(self.liste))
            draw_rectangle_rounded((self.originex, originey, self.largeur, tailley), 0.2, 30, 
                                   [255, 255, 255, 50])
            draw_rectangle_rounded_lines((self.originex, originey, self.largeur, tailley), 
                                         0.2, 30, 3, WHITE)
            #draw_texture(self.coraux, self.originex, originey+tailley-self.coraux.height, WHITE)
            for i in range(len(self.liste)):
                xbat = 0
                if self.getContactBateau(i):
                    xbat = int(xf*0.01)
                    self.soulevement[i] = True
                elif self.liste[i].originale.width >= (self.largeur+self.originex)*0.9:
                    self.soulevement[i] = False
                    xbat = int((self.largeur+self.originex)*0.9-self.liste[i].originale.width)
                ybat = int(tailley*(self.positions[len(self.liste)-1][1][i]/100)+originey)
                self.liste[i].dessine(xbat, ybat-int(self.liste[i].originale.height/2))

    def setListe(self, liste: list) -> None:
        self.liste = liste
        self.soulevement = [False]*len(self.liste)

    def supValListe(self, indice: int) -> None:
        if indice >= 0 and indice < len(self.liste):
            del self.liste[indice]
            del self.soulevement[indice]

    def ajValListe(self, valeur: BateauJoueur) -> None:
        self.liste.append(valeur)
        self.soulevement.append(False)

    def getContactBateau(self, indice: int) -> bool:
        """Vérifie si le curseur est sur le bateau.

        Returns:
            bool: True si le curseur est sur le bateau, False dans le cas contraire.
        """
        bateau = self.liste[indice]
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= bateau.coord[1] and y <= bateau.coord[1]+bateau.coord[3]:
            if (not self.soulevement[indice] and x <= int(self.largeur+self.originex)) or (self.soulevement[indice] and x <= int(bateau.coord[0]+bateau.coord[2])):
                rep = True
        return rep