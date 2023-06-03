from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from museeNoyee import minicoeur, minimarin

class BarreAction:
    def __init__(self, joueurs: list, passe) -> None:
        self.joueurs = joueurs
        self.actuel = self.tour = 0
        # boutons
        self.passe = Bouton(TB2n, PTIBT1, "PASSE", 'images/ui/passer+.png', [passe])
        self.precedent = Bouton(TB2n, PTIBT1, "PRECEDENT", 'images/ui/precedent.png', [self.actPrecedent])
        self.suivant = Bouton(TB2n, PTIBT1, "SUIVANT", 'images/ui/suivant.png', [self.actSuivant])
        # dimensions
        self.hauteur = int(yf*0.07)
        # Autres
        self.chabat = False

    def dessine(self) -> None:
        draw_rectangle(0, yf-self.hauteur, xf, yf, [80, 80, 80, 150])
        self.passe.dessine(int(xf-self.passe.getDims()[0]*0.7), int(yf-self.hauteur/2))
        self.dessineInfoBat()
        self.dessineProgression()

    def dessineInfoBat(self) -> None:
        bateau = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        colFond = [24, 22, 22, 170]
        x = int(xf*0.005)
        y = int(yf-self.hauteur+yf*0.007)
        draw_rectangle(x, y, int(xf*0.136), int(yf*0.025), colFond)
        draw_texture(minicoeur, x, y, WHITE)
        x += int(xf*0.015)
        y += int(yf*0.0028)
        draw_rectangle(x, y, int(xf*0.12), int(yf*0.02), [230, 183, 183, 255])
        draw_rectangle(x, y, int((xf*0.12)*(bateau.vie/bateau.pvi)), int(yf*0.02), RED)
        x += int(xf*0.004)
        y -= int(yf*0.0008)
        draw_text_ex(police1, str(bateau.vie)+"/"+str(bateau.pvi), (x, y), int(yf*0.02), 0, WHITE)
        x = int(xf*0.005)
        y += int(yf*0.03)
        draw_rectangle(x, y, int(xf*0.04), int(yf*0.025), colFond)
        draw_texture(minimarin, x, y, WHITE)
        x += int(xf*0.019)
        y += int(yf*0.003)
        draw_text_ex(police1, str(bateau.marins), (x, int(y+yf*0.001)), int(yf*0.02), 0, WHITE)
        x += int(xf*0.025)
        draw_text_ex(police2, "TOUR "+str(self.tour), (x, y), yf*0.02, 0, WHITE)

    def dessineProgression(self) -> None:
        l = int(yf*0.2)
        ecart = int(xf*0.007)
        nbBat = self.getNbBatRestants()
        x = int(xf/2-l/2-ecart-self.precedent.getDims()[0])
        y = int(yf-self.hauteur+yf*0.01)
        self.precedent.dessine(int(x+self.precedent.getDims()[0]/2), int(yf-self.hauteur/2))
        x += self.precedent.getDims()[0]+ecart
        draw_rectangle_rounded([x, y, l, int(yf*0.05)], 0.15, 30, [40, 40, 40, 200])
        tt = measure_text_ex(police1, str(self.joueurs[self.actuel].actuel+1)+"/"+str(len(self.joueurs[self.actuel])), yf*0.04, 0)
        draw_text_ex(police1, str(self.joueurs[self.actuel].actuel+1)+"/"+str(len(self.joueurs[self.actuel])), (int(x+xf*0.01), int(y+yf*0.007)), yf*0.04, 0, WHITE)
        draw_text_ex(police2i, " - "+str(nbBat)+" restant(s)", (int(x+xf*0.015+tt.x), int(y+yf*0.015)), yf*0.02, 0, WHITE)
        x += l+ecart
        self.suivant.dessine(int(x+self.suivant.getDims()[0]/2), int(yf-self.hauteur/2))

    def rejouer(self) -> None:
        self.actuel = self.tour = 0

    def actSuivant(self) -> None:
        nbBat = len(self.joueurs[self.actuel])
        bateaux = self.joueurs[self.actuel].bateaux
        actuel = self.joueurs[self.actuel].actuel
        i = 0
        trouve = False
        while i < (nbBat-actuel-1) and not trouve:
            if not bateaux[actuel+i+1].aFini():
                trouve = self.chabat = True
                bateaux[actuel].actif = False
                self.joueurs[self.actuel].actuel = actuel+i+1
                +bateaux[actuel+i+1]
            else:
                i += 1
        if not trouve:
            bateaux[actuel].actif = False
            self.joueurs[self.actuel].actuel = 0
            +bateaux[0]
            self.chabat = True
            if bateaux[0].aFini():
                self.actSuivant()

    def actPrecedent(self) -> None:
        nbBat = len(self.joueurs[self.actuel])
        bateaux = self.joueurs[self.actuel].bateaux
        actuel = self.joueurs[self.actuel].actuel
        i = 0
        trouve = False
        while i < (actuel) and not trouve:
            indice = actuel-i-1
            if not bateaux[indice].aFini():
                trouve = self.chabat = True
                bateaux[actuel].actif = False
                self.joueurs[self.actuel].actuel = indice
                +bateaux[indice]
            else:
                i += 1
        if not trouve or indice <= -1:
            bateaux[actuel].actif = False
            self.joueurs[self.actuel].actuel = nbBat-1
            +bateaux[nbBat-1]
            self.chabat = True
            if bateaux[nbBat-1].aFini():
                self.actPrecedent()

    def getNbBatRestants(self) -> int:
        nb = 0
        for i in range(len(self.joueurs[self.actuel])):
            if not self.joueurs[self.actuel][i].aFini():
                nb += 1
        return nb
    
    def setActuel(self, actuel: int) -> None:
        self.actuel = actuel
        if actuel == 0:
            self.tour += 1