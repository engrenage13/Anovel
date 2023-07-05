from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from museeNoyee import minicoeur, minimarin

class BarreAction:
    def __init__(self, joueurs: list, passe) -> None:
        self.joueurs = joueurs
        self.actuel = 0
        # boutons
        self.passe = Bouton(TB2n, PTIBT1, "PASSE", 'images/ui/passer+.png', [passe])
        self.precedent = Bouton(TB2n, PTIBT1, "PRECEDENT", 'images/ui/precedent.png', [self.actPrecedent])
        self.suivant = Bouton(TB2n, PTIBT1, "SUIVANT", 'images/ui/suivant.png', [self.actSuivant])
        self.btDep = Bouton(TB2o, BTV, "DEPLACEMENT", '', [self.activeDeplacement])
        self.btv = Bouton(TB2n, PTIBT1, "VALIDER", 'images/ui/check.png', [self.valideAction])
        self.btx = Bouton(TB2n, PTIBT1, "ANNULER", 'images/ui/CroSom.png', [self.annuleAction])
        self.btOrga = Bouton(TB2o, BTV, "ORGANISER", '', [self.activeOrga])
        self.btAbordage = Bouton(TB2o, BTV, "ABORDAGE", '', [self.activeAbordage])
        # dimensions
        self.hauteur = int(yf*0.07)
        # Autres
        self.chabat = self.deplacement = self.choixAction = self.valide = self.annule = self.orga = self.abordage = False
        # Capteurs
        self.actionsPossibles = {"deplacement": True, "organisation": False, "abordage": False}

    def dessine(self, tour: int) -> None:
        draw_rectangle(0, yf-self.hauteur, xf, yf, [80, 80, 80, 150])
        self.dessineInfoBat(tour)
        self.dessineProgression()
        if not self.deplacement:
            texte = "ACTIONS POSSIBLES : "
            x = int(xf*0.45)
            tt = measure_text_ex(police2, texte, self.hauteur*0.5, 0)
            #espace = int(xf*0.01)
            draw_text_ex(police2, texte, (x, int(yf-self.hauteur*0.75)), self.hauteur*0.5, 0, WHITE)
            x += tt.x
            if self.actionsPossibles["deplacement"]:
                self.btDep.dessine(int(x+self.btDep.getDims()[0]/2), int(yf-self.hauteur/2))
                #x += int(self.btDep.getDims()[0]+espace)
            else:
                draw_text_ex(police2i, "AUCUNE", (x, int(yf-self.hauteur*0.75)), self.hauteur*0.5, 0, WHITE)
            self.passe.dessine(int(xf-self.passe.getDims()[0]*0.7), int(yf-self.hauteur/2))
        else:
            self.btv.dessine(int(xf-self.btv.getDims()[0]*0.7), int(yf-self.hauteur/2))
            self.btx.dessine(int(xf-self.btv.getDims()[0]*2), int(yf-self.hauteur/2))
            if self.actionsPossibles["organisation"]:
                self.btOrga.dessine(int(xf-self.btv.getDims()[0]*2.8-self.btOrga.getDims()[0]/2), int(yf-self.hauteur/2))
            if self.actionsPossibles["abordage"]:
                self.btAbordage.dessine(int(xf-self.btv.getDims()[0]*2.8-self.btAbordage.getDims()[0]/2), int(yf-self.hauteur/2))

    def dessineInfoBat(self, tour: int) -> None:
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
        draw_text_ex(police2, "TOUR "+str(tour), (x, y), yf*0.02, 0, WHITE)

    def dessineProgression(self) -> None:
        l = int(yf*0.2)
        ecart = int(xf*0.007)
        nbBat = self.getNbBatRestants()
        x = int(xf*0.26-l/2-ecart-self.precedent.getDims()[0])
        y = int(yf-self.hauteur+yf*0.01)
        if not self.deplacement:
            self.precedent.dessine(int(x+self.precedent.getDims()[0]/2), int(yf-self.hauteur/2))
        x += self.precedent.getDims()[0]+ecart
        draw_rectangle_rounded([x, y, l, int(yf*0.05)], 0.15, 30, [40, 40, 40, 200])
        tt = measure_text_ex(police1, str(self.joueurs[self.actuel].actuel+1)+"/"+str(len(self.joueurs[self.actuel])), yf*0.04, 0)
        draw_text_ex(police1, str(self.joueurs[self.actuel].actuel+1)+"/"+str(len(self.joueurs[self.actuel])), (int(x+xf*0.01), int(y+yf*0.007)), yf*0.04, 0, WHITE)
        draw_text_ex(police2i, " - "+str(nbBat)+" restant(s)", (int(x+xf*0.015+tt.x), int(y+yf*0.015)), yf*0.02, 0, WHITE)
        x += l+ecart
        if not self.deplacement:
            self.suivant.dessine(int(x+self.suivant.getDims()[0]/2), int(yf-self.hauteur/2))

    def rejouer(self) -> None:
        self.actuel = 0

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
        texte = ""
        for i in range(len(self.joueurs[actuel])):
            texte += f"[{self.joueurs[actuel][i].id}, {self.joueurs[actuel][i].aFini()}] "
        print(texte)

    def activeDeplacement(self) -> None:
        self.deplacement = self.choixAction = True

    def valideAction(self) -> None:
        self.valide = True

    def annuleAction(self) -> None:
        self.annule = True

    def activeOrga(self) -> None:
        self.orga = True

    def activeAbordage(self) -> None:
        self.abordage = True