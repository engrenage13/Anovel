from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from jeux.archipel.ui.objets.Bateau import Bateau
from jeux.archipel.ui.icones import minicoeur, minimarin

class BarreAction:
    """La barre contenant les actions proposées aux joueurs.
    """
    def __init__(self, joueurs: list, passe) -> None:
        """Crée la barre.

        Args:
            joueurs (list[Joueur]): Les joueurs présents dans la partie.
            passe (function): La méthode à exécuter quand un joueur passe son tour.
        """
        self.joueurs = joueurs
        self.actuel = 0
        # boutons
        self.passe = Bouton(TB2n, PTIBT1, "PASSE", 'images/ui/passer+.png', [passe])
        self.precedent = Bouton(TB2n, PTIBT1, "PRECEDENT", 'images/ui/precedent.png', [self.actPrecedent])
        self.suivant = Bouton(TB2n, PTIBT1, "SUIVANT", 'images/ui/suivant.png', [self.actSuivant])
        self.btDep = Bouton(TB2o, BTV, "DEPLACEMENT", '', [self.activeDeplacement])
        self.btAt = Bouton(TB2o, BTX, "ATTAQUE", '', [self.activeAttaque])
        self.btv = Bouton(TB2n, PTIBT1, "VALIDER", 'images/ui/check.png', [self.valideAction])
        self.btx = Bouton(TB2n, PTIBT1, "ANNULER", 'images/ui/CroSom.png', [self.annuleAction])
        self.btOrga = Bouton(TB2o, BTV, "ORGANISER", '', [self.activeOrga])
        self.btAbordage = Bouton(TB2o, BTV, "ABORDAGE", '', [self.activeAbordage])
        # dimensions
        self.hauteur = int(yf*0.07)
        # Autres
        self.chabat = self.deplacement = self.choixAction = self.valide = self.annule = self.orga = self.abordage = self.attaque = False
        # Capteurs
        self.actionsPossibles = {"deplacement": True, "organisation": False, "abordage": False, "attaque": True}

    def dessine(self, tour: int, dernierTour: int) -> None:
        """Dessine la barre à l'écran

        Args:
            tour (int): Tour actuel de la partie.
            dernierTour (int): Tour final.
        """
        draw_rectangle(0, yf-self.hauteur, xf, yf, [80, 80, 80, 150])
        self.dessineInfoBat(tour, dernierTour)
        if not self.deplacement and not self.attaque:
            texte = "ACTIONS POSSIBLES : "
            x = int(xf*0.31)
            tt = measure_text_ex(police2, texte, self.hauteur*0.5, 0)
            espace = int(xf*0.005)
            draw_text_ex(police2, texte, (x, int(yf-self.hauteur*0.75)), self.hauteur*0.5, 0, WHITE)
            x += tt.x
            if not self.actionsPossibles["deplacement"] and not self.actionsPossibles["attaque"]:
                draw_text_ex(police2i, "AUCUNE", (x, int(yf-self.hauteur*0.75)), self.hauteur*0.5, 0, WHITE)
            elif self.actionsPossibles["deplacement"]:
                self.btDep.dessine(int(x+self.btDep.getDims()[0]/2), int(yf-self.hauteur/2))
                if is_key_pressed(90):
                    self.activeDeplacement()
                if self.actionsPossibles["attaque"]:
                    x += int(self.btDep.getDims()[0]+espace)
                    self.btAt.dessine(int(x+self.btAt.getDims()[0]/2), int(yf-self.hauteur/2))
                    if is_key_pressed(88):
                        self.activeAttaque()
            elif self.actionsPossibles["attaque"]:
                self.btAt.dessine(int(x+self.btAt.getDims()[0]/2), int(yf-self.hauteur/2))
                if is_key_pressed(88):
                    self.activeAttaque()
            self.passe.dessine(int(xf-self.passe.getDims()[0]*0.7), int(yf-self.hauteur/2))
        else:
            self.btv.dessine(int(xf-self.btv.getDims()[0]*0.7), int(yf-self.hauteur/2))
            if is_key_pressed(32):
                self.valideAction()
            self.btx.dessine(int(xf-self.btv.getDims()[0]*2), int(yf-self.hauteur/2))
            if is_key_pressed(261):
                self.annuleAction()
            if self.deplacement:
                if self.actionsPossibles["organisation"]:
                    self.btOrga.dessine(int(xf-self.btv.getDims()[0]*2.8-self.btOrga.getDims()[0]/2), int(yf-self.hauteur/2))
                    if is_key_pressed(90):
                        self.activeOrga()
                if self.actionsPossibles["abordage"]:
                    self.btAbordage.dessine(int(xf-self.btv.getDims()[0]*2.8-self.btAbordage.getDims()[0]/2), int(yf-self.hauteur/2))
                    if is_key_pressed(90):
                        self.activeAbordage()
            if self.attaque:
                bateau = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
                tda1 = "INFLIGER "
                tda2 = f"{bateau.degats}"
                tda3 = f" DEGATS A UN AUTRE BATEAU DANS LA ZONE"
                taille = self.hauteur*0.5
                tt1 = measure_text_ex(police2, tda1, taille, 0)
                tt2 = measure_text_ex(police1, tda2, taille, 0)
                x = int(xf*0.28)
                draw_text_ex(police2, tda1, (x, int(yf-self.hauteur*0.75)), taille, 0, WHITE)
                x += int(tt1.x)
                draw_text_ex(police1, tda2, (x, int(yf-self.hauteur*0.75)), taille, 0, [0, 255, 0, 255])
                x += int(tt2.x)
                draw_text_ex(police2, tda3, (x, int(yf-self.hauteur*0.75)), taille, 0, WHITE)

    def dessineInfoBat(self, tour: int, tourmax: int) -> None:
        """Dessine les infos relatives au bateau actif.

        Args:
            tour (int): Tour actuel de la partie.
            tourmax (int): Tour final.
        """
        bateau = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        if isinstance(bateau, Bateau):
            colFond = [24, 22, 22, 170]
            x = int(xf*0.005)
            y = int(yf-self.hauteur+yf*0.007)
            draw_rectangle(x, y, int(xf*0.136), int(yf*0.025), colFond)
            draw_texture(minicoeur, x, y, WHITE)
            x += int(xf*0.015)
            y += int(yf*0.0028)
            draw_rectangle(x, y, int(xf*0.12), int(yf*0.02), [230, 183, 183, 255])
            draw_rectangle(x, y, int((xf*0.12)*(bateau.get_vie()/bateau.sauvegarde["vie"])), int(yf*0.02), RED)
            x += int(xf*0.004)
            y -= int(yf*0.0008)
            draw_text_ex(police1, str(bateau.get_vie())+"/"+str(bateau.sauvegarde["vie"]), (x, y), int(yf*0.02), 0, WHITE)
            x = int(xf*0.005)
            y += int(yf*0.03)
            draw_rectangle(x, y, int(xf*0.04), int(yf*0.025), colFond)
            draw_texture(minimarin, x, y, WHITE)
            x += int(xf*0.019)
            y += int(yf*0.003)
            draw_text_ex(police1, str(bateau.get_marins()), (x, int(y+yf*0.001)), int(yf*0.02), 0, WHITE)
            x += int(xf*0.025)
            draw_text_ex(police2, f"TOUR {str(tour)}/{str(tourmax)}", (x, y), yf*0.02, 0, WHITE)

    # Choix bateau - Désactivé
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
    # /Choix bateau - désactivé
    
    def rejouer(self) -> None:
        """Réinitialise certains paramètres pour pouvoir rejouer une partie.
        """
        self.actuel = 0
    
    def setActuel(self, actuel: int) -> None:
        """Modifie le joueur actuel.

        Args:
            actuel (int): Indice du joueur actuel.
        """
        self.actuel = actuel

    def activeDeplacement(self) -> None:
        """Annonce que le joueur a choisi l'action de déplacement.
        """
        self.deplacement = self.choixAction = True

    def activeAttaque(self) -> None:
        """Annoce que le joueur a choisi l'action d'attaque.
        """
        self.attaque = self.choixAction = True

    def valideAction(self) -> None:
        """Valide l'action effectuée par le joueur.
        """
        self.valide = True

    def annuleAction(self) -> None:
        """Annule l'action effectuée par le joueur.
        """
        self.annule = True

    def activeOrga(self) -> None:
        """Active l'organisation.
        """
        self.orga = True

    def activeAbordage(self) -> None:
        """Active l'abordage.
        """
        self.abordage = True