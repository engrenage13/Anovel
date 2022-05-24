from systeme.FondMarin import *
from museeNoyee import viseur, croix, rond
from animations.Paillette import Paillette
from ui.bouton import Bouton

class FinPartie:
    def __init__(self, joueurs: list, tour: int) -> None:
        self.joueurs = joueurs
        self.duree = tour
        self.pos = yf
        self.delai = 200
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
        draw_rectangle(0, self.pos, xf, yf, BLACK)
        if self.pos == 0:
            for i in range(len(self.paillettes)):
                self.paillettes[i].dessine()
        draw_line_ex((int(xf/2), int(self.pos+yf*0.2)), (int(xf/2), int(self.pos+yf*0.83)), 4, GOLD)
        tLong = measure_text_ex(police2, "Longueur de la partie", 20, 0)
        tTour = measure_text_ex(police2, f"{self.duree} Tours", 40, 0)
        draw_text_pro(police2, "Longueur de la partie", (int(xf/2-tLong.x/2), int(self.pos+yf*0.1-tLong.y/2)), 
                      (0, 0), 0, 20, 0, WHITE)
        draw_text_pro(police2, f"{self.duree} Tours", (int(xf/2-tTour.x/2), int(self.pos+yf*0.14-tTour.y/2)), 
                      (0, 0), 0, 40, 0, WHITE)
        ytit = int(self.pos+yf*0.12)
        ystat = int(ytit+yf*0.13)
        ybat = int(ystat+yf*0.13)
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
        if self.pos > 0:
            self.defil()

    def defil(self) -> None:
        """Fait défiler vers le haut de 1 écran, la fenêtre.
        """
        if self.delai > 0:
            self.delai = self.delai - 1
        else:
            self.pos = int(self.pos - yf*0.01)
            if self.pos < 0:
                self.pos = 0

    def dessineTitre(self, coord: tuple, indice: int) -> None:
        x = coord[0]
        y = coord[1]
        tTit = measure_text_ex(police1, self.joueurs[indice][0].getNom(), 40, 0)
        tWin = measure_text_ex(police2, "VAINQUEUR", 28, 0)
        x1 = x
        y1 = int(y + yf*0.07 - tTit.y/2)
        if indice == 1:
            x = x - tTit.x
            x1 = x1 - tWin.x
        draw_text_pro(police1, self.joueurs[indice][0].getNom(), (x, y), (0, 0), 0, 40, 0, BLUE)
        if self.joueurs[indice][1]:
            draw_text_pro(police2, "VAINQUEUR", (x1, y1), (0, 0), 0, 28, 0, GOLD)

    def dessineStats(self, coord: tuple, indice: int) -> None:
        """Dessine les stats du joueur concerné.
        """
        x = coord[0]
        y = coord[1]
        images = [viseur, croix, rond]
        valeurs = self.joueurs[indice][0].getStats()
        for i in range(len(images)):
            if type(valeurs[i]) != list:
                valeur = str(valeurs[i])
            else:
                valeur = str(valeurs[i][0])
            tVal = measure_text_ex(police2, valeur, 60, 0)
            draw_text_pro(police2, valeur, (x, y), (0, 0), 0, 60, 0, WHITE)
            draw_texture(images[i], int(x+tVal.x+xf*0.01), y, WHITE)
            x = int(x + xf*0.1)

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
                draw_rectangle(x, y, t, taille, GRAY)
                xt = x
                for j in range(len(touche)):
                    if touche[j] == 'x':
                        draw_rectangle(xt, y, taille, taille, RED)
                    xt = xt + taille
            else:
                draw_rectangle(x, y, t, taille, (40, 40, 40, 255))
            tNom = measure_text_ex(police2, liBat[i].nom, 25, 0)
            xText = int(x+t+taille)
            if indice == 1:
                xText = int(x-taille-tNom.x)
            draw_text_pro(police2, liBat[i].nom, (xText, int(y+taille/2-tNom.y/2)), (0, 0), 0, 25, 0, WHITE)
            y = int(y+tailleCase)