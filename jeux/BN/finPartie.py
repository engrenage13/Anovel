from systeme.FondMarin import *
from jeux.BN.collectionImage import viseur, croix, rond
from animations.Paillette import Paillette
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille

class FinPartie:
    def __init__(self, joueurs: list, tour: int, createur: object) -> None:
        """Crée la fenêtre de fin de partie.

        Args:
            joueurs (list): Les joueurs ayant joué la partie.
            tour (int): Le nombre de tour qu'à durer la partie.
            createur (object): L'entité qui crée la fenêtre et gère la partie.
        """
        self.tt1 = hbarre
        self.tt2 = int(hbarre*0.7)
        self.proprio = createur
        self.joueurs = joueurs
        self.duree = tour
        self.pos = False
        self.saturation = 0
        # Boutons
        self.gbt = Grille(int(xf*0.15), [False])
        self.gbt.ajouteElement(Bouton(TB1o, BTV, "CONTINUER", '', [self.portailBoreal]), 0, 0)
        self.hauteurBt = int(yf*1.11)
        self.hBtIndice = int(yf*0.91)
        # /Boutons
        # Paillettes
        self.paillettes = []
        x1 = 0
        x2 = int(xf/2)
        if self.joueurs[1][1]:
            x1 = x2
            x2 = xf
        for i in range(8):
            self.paillettes.append(Paillette((x1, int(yf*0.2), x2, yf), 
                [(40, 40, 40, 255), (10, 10, 10, 255), (20, 20, 20, 255), (30, 30, 30, 255), (0, 0, 30, 255)]))

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        draw_rectangle(0, 0, xf, yf, (0, 0, 0, self.saturation))
        for i in range(len(self.paillettes)):
            self.paillettes[i].dessine()
        draw_line_ex((int(xf/2), int(yf*0.2)), (int(xf/2), int(yf*0.83)), 4, (255, 203, 0, self.saturation))
        tLong = measure_text_ex(police2, "LONGUEUR DE LA PARTIE", self.tt2, 0)
        tTour = measure_text_ex(police2, f"{self.duree} TOURS", self.tt1, 0)
        draw_text_pro(police2, "LONGUEUR DE LA PARTIE", (int(xf/2-tLong.x/2), int(yf*0.1-tLong.y/2)), 
                      (0, 0), 0, self.tt2, 0, (255, 255, 255, self.saturation))
        draw_text_pro(police2, f"{self.duree} TOURS", (int(xf/2-tTour.x/2), int(yf*0.14-tTour.y/2)), 
                      (0, 0), 0, self.tt1, 0, (255, 255, 255, self.saturation))
        ytit = int(yf*0.11)
        ystat = int(ytit+yf*0.14)
        ybat = int(ystat+yf*0.14)
        for i in range(len(self.joueurs)):
            xtit = int(xf*0.01)
            xstat = int(xf*0.1)
            xbat = int(xf*0.02)
            if i > 0:
                xtit = xf-xtit
                xstat = xstat*6
                xbat = int(xf-xbat)
            self.dessineTitre((xtit, ytit), i)
            self.dessineStats((xstat, ystat), i)
            self.dessineBateaux((xbat, ybat), i)
        self.gbt.dessine(int(xf*0.5-self.gbt.largeur/2), int(self.hauteurBt-self.gbt.hauteur/2))
        if self.hauteurBt > self.hBtIndice:
            self.apparition()

    def apparition(self) -> None:
        """Rend oppaque le fond de la fenêtre et fait apparaître le drapeau vainqueur.
        """
        if self.saturation < 255:
            self.saturation = self.saturation + 5
        elif self.pos > 0:
            self.pos = int(self.pos - xf*0.01)
            if self.pos < 0:
                self.pos = 0
        elif self.hauteurBt > self.hBtIndice:
            self.hauteurBt = int(self.hauteurBt-int(yf*0.01))

    def dessineTitre(self, coord: tuple, indice: int) -> None:
        """Dessine les noms des joueurs et la bannière "VAINQUEUR".

        Args:
            coord (tuple): Origine voulue pour les noms.
            indice (int): Indice du joueur qui a gagné.
        """
        x = coord[0]
        y = coord[1]
        tTit = measure_text_ex(police1, self.joueurs[indice][0].getNom().upper(), self.tt1, 0)
        tWin = measure_text_ex(police2i, "VAINQUEUR", self.tt1, 0)
        x1 = x
        y1 = int(y + yf*0.08 - tTit.y/2)
        fagnon = (0, int(y1-yf*0.005), int(x+tWin.x+xf*0.02), int(tWin.y+yf*0.01))
        multiplicateur = -1
        if indice == 1:
            x = x - tTit.x
            x1 = x1 - tWin.x
            fagnon = (int(x1-xf*0.02), int(y1-yf*0.005), int(x+tWin.x+xf*0.02), int(tWin.y+yf*0.01))
            multiplicateur = 1
        if not self.pos and not (type(self.pos) == int and self.pos == 0):
            self.pos = fagnon[2]
        draw_text_pro(police1, self.joueurs[indice][0].getNom().upper(), (x, y), (0, 0), 0, self.tt1, 0, 
                      (0, 121, 241, self.saturation))
        if self.joueurs[indice][1]:
            draw_rectangle(fagnon[0]+self.pos*multiplicateur, fagnon[1], fagnon[2], fagnon[3], GOLD)
            draw_text_pro(police2i, "VAINQUEUR", (x1+self.pos*multiplicateur, y1), (0, 0), 0, self.tt1, 0, BLACK)

    def dessineStats(self, coord: tuple, indice: int) -> None:
        """Dessine les stats du joueur concerné.
        """
        x = coord[0]
        y = coord[1]
        images = [viseur, croix, rond]
        valeurs = self.joueurs[indice][0].getStats()
        draw_line_ex((int(x-xf*0.05), int(y-yf*0.02)), (int(x+xf*0.35), int(y-yf*0.02)), 2, 
                     (0, 121, 241, self.saturation))
        for i in range(len(images)):
            if type(valeurs[i]) != list:
                valeur = str(valeurs[i])
            else:
                valeur = str(valeurs[i][0])
            tVal = measure_text_ex(police2, valeur, 60, 0)
            draw_text_pro(police2, valeur, (x, y), (0, 0), 0, 60, 0, (255, 255, 255, self.saturation))
            draw_texture(images[i], int(x+tVal.x+xf*0.01), int(y-images[i].height/2+tVal.y/2), 
                         (255, 255, 255, self.saturation))
            x = int(x + xf*0.1)
        draw_line_ex((int(coord[0]-xf*0.05), int(y+tVal.y+yf*0.02)), (int(coord[0]+xf*0.35), 
                     int(y+tVal.y+yf*0.02)), 2, (0, 121, 241, self.saturation))

    def dessineBateaux(self, coord: tuple, indice: int) -> None:
        """Dessine les bateaux du joueur dans son cadre de récap.

        Args:
            coord (tuple): Où doivent être dessinés les bateaux.
            indice (int): Joueur concerné.
        """
        liBat = self.joueurs[indice][0].getBateaux()
        y = coord[1]
        taille = int(tailleCase*0.5)
        for i in range(len(liBat)):
            x = coord[0]
            t = taille*liBat[i].taille
            if indice == 1:
                x = int(x-t)
            touche = liBat[i].etatSeg
            if not liBat[i].coule:
                draw_rectangle(x, y, t, taille, (130, 130, 130, self.saturation))
                xt = x
                for j in range(len(touche)):
                    if touche[j] == 'x':
                        draw_rectangle(xt, y, taille, taille, (255, 0, 0, self.saturation))
                    xt = xt + taille
            else:
                draw_rectangle(x, y, t, taille, (40, 40, 40, self.saturation))
            tNom = measure_text_ex(police2, liBat[i].nom.upper(), self.tt2, 0)
            xText = int(x+t+taille)
            if indice == 1:
                xText = int(x-taille-tNom.x)
            draw_text_pro(police2, liBat[i].nom.upper(), (xText, int(y+taille/2-tNom.y/2)), (0, 0), 0, self.tt2, 0, 
                          (255, 255, 255, self.saturation))
            y = int(y+tailleCase)

    # Between the worlds
    def portailBoreal(self) -> None:
        self.proprio.message = 'ANOVEL_MENU'
        self.proprio.lu = False