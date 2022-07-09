from systeme.FondMarin import *
from objets.BateauJoueur import *

class Tiroir:
    def __init__(self, createur: object) -> None:
        self.createur = createur
        self.liste = []
        self.positions = [(1, [50]), (2, [30, 70]), (3, [20, 50, 80]), (4, [15, 37, 63, 85]), 
                          (5, [10, 30, 50, 70, 90])]
        self.soulevement = []
        # Graphique
        self.tCase = 1.45*tailleCase
        self.originex = -40
        self.largeur = int(xf*0.16)
        self.lumCadre = [0, 5]
        # Images
        deco1 = load_image('images/decors/coraux1.png')
        ratio = self.largeur/deco1.width
        image_resize(deco1, int(deco1.width*ratio), int(deco1.height*ratio))
        self.decos = [load_texture_from_image(deco1)]
        image_flip_vertical(deco1)
        self.decos.append(load_texture_from_image(deco1))

    def dessine(self, y: int) -> None:
        if len(self.liste) > 0:
            tailley = int(self.tCase*len(self.liste))
            originey = y-int(self.tCase/2*len(self.liste))
            draw_rectangle_rounded((self.originex, originey, self.largeur+self.originex*-1, tailley), 
                                   0.2, 30, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[0], self.largeur-self.decos[0].width, 
                         originey+tailley-self.decos[0].height, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[1], self.largeur-self.decos[1].width, originey, 
                         [255, 255, 255, self.lumCadre[0]])
            draw_rectangle_rounded_lines((self.originex, originey, self.largeur+self.originex*-1, tailley), 
                                         0.2, 30, 3, [255, 255, 255, self.lumCadre[1]])
            self.apparition()
            i = 0
            while i < len(self.liste):
                xbat = 0
                contact = self.getContactBateau(i)
                if not contact[1]:
                    if contact[0]:
                        xbat = int(xf*0.01)
                        self.soulevement[i][0] = True
                    elif self.liste[i].images[0].width >= (self.largeur)*0.9:
                        self.soulevement[i][0] = False
                        xbat = int((self.largeur)*0.9-self.liste[i].images[0].width)
                    ybat = int(tailley*(self.positions[len(self.liste)-1][1][i]/100)+originey)
                    self.liste[i].dessine(self.soulevement[i][1], ybat-int(self.liste[i].images[0].height/2))
                    # Animation des bateaux
                    self.bougeBat(i, xbat)
                i = i + 1

    def setListe(self, liste: list) -> None:
        self.liste = liste[:]
        self.lumCadre = [0, 5]
        for i in range(len(self.liste)):
            self.soulevement.append([False, 0-self.liste[i].images[0].width])

    def supValListe(self, indice: int) -> None:
        if indice >= 0 and indice < len(self.liste):
            del self.liste[indice]
            del self.soulevement[indice]
            if len(self.liste) == 0:
                self.lumCadre = [0, 5]

    def ajValListe(self, valeur: BateauJoueur) -> None:
        self.liste.append(valeur)
        self.soulevement.append([False, 0-valeur.images[0].width])

    def getContactBateau(self, indice: int) -> list:
        """Vérifie si le curseur est sur le bateau.

        Returns:
            list: 1. True si le curseur est sur le bateau, False dans le cas contraire. 2. Valeurs spécifiques.
        """
        bateau = self.liste[indice]
        rep = False
        onse = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= bateau.coord[1] and y <= bateau.coord[1]+bateau.coord[3]:
            if (not self.soulevement[indice][0] and x <= int(self.largeur)) or (self.soulevement[indice][0] and x <= int(bateau.coord[0]+bateau.coord[2])):
                rep = True
                onse = self.checkSelect(bateau)
                if onse:
                    rep = False
        return [rep, onse]

    def checkSelect(self, bateau: BateauJoueur) -> bool:
        rep = False
        if is_mouse_button_pressed(0):
            parasite = self.checkBateauVolant()
            bateau.defil = True
            self.createur.attente = 50
            self.createur.bateaux.append(bateau)
            if parasite >= 0:
                self.createur.bateaux[parasite].pos = False
                self.createur.bateaux[parasite].immobile()
                self.liste[self.liste.index(bateau)] = self.createur.bateaux[parasite]
                del self.createur.bateaux[parasite]
                self.createur.ordreBateaux()
            else:
                self.supValListe(self.liste.index(bateau))
            rep = True
        return rep

    def checkBateauVolant(self) -> int:
        rep = -1
        i = 0
        while i < len(self.createur.bateaux) and rep == -1:
            if self.createur.bateaux[i].defil:
                rep = i
            else:
                i = i + 1
        return rep

    def apparition(self) -> None:
        if self.lumCadre[0] < 50:
            self.lumCadre[0] += 1
            self.lumCadre[1] += 5

    def bougeBat(self, bateau: int, verif: int) -> None:
        if self.soulevement[bateau][1] < verif:
            pas = int((verif-self.soulevement[bateau][1])/9)
            if pas < 1:
                pas = 1
            self.soulevement[bateau][1] += pas
        elif self.soulevement[bateau][1] > verif:
            pas = int((self.soulevement[bateau][1]-verif)/9)
            if pas < 1:
                pas = 1
            self.soulevement[bateau][1] -= pas