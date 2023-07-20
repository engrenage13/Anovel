from random import choice
from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.boutonPression import BoutonPression
from ui.bouton.grille import Grille
from jeux.Jeu_1.fonctions.bases import TAILLECASE
from jeux.Jeu_1.Jeu import Jeu, config
from systeme.set import trouveParam

class Scene(Jeu):
    def __init__(self) -> None:
        super().__init__()
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.optDev = [Bouton(TB2n, BTDEV, "REJOUER", 'images/ui/reset.png', [self.rejouer]), 
                       Bouton(TB2n, BTDEV, "PASSER L'ACTION", 'images/ui/passer.png', [self.passeAction]),
                       Bouton(TB2n, BTDEV, "PASSER LE TOUR", 'images/ui/passer+.png', [self.passeTour]),
                       Bouton(TB2n, BTDEV, "PASSER LA PHASE", 'images/ui/passer++.png', [self.passePhase])]
        t = TB2n.hauteur
        self.g1 = Grille(int(t+yf*0.01), [False], False)
        self.gDev = Grille(int(t+yf*0.01), [False])
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.g1.largeur = int((1*(t+yf*0.005))+yf*0.005)
        for i in range(len(self.optDev)):
            self.gDev.ajouteElement(self.optDev[i], 0, i)
        self.gDev.hauteur = int(((len(self.opt)-1)*(t+yf*0.005))+yf*0.005)
        self.posCurseur = (get_mouse_x(), get_mouse_y())
        self.move = False
        self.trajet = (0, 0)
        self.afficheSecteur('c')
        self.delaiDepart = 70
        # Placement
        self.btValid = BoutonPression(TB1o, BTNOIR, "VALIDER", "images/ui/check.png", [self.joueurSuivant])
        self.btAlea = Bouton(TB1n, PTIBT1, "PLACEMENT ALEATOIRE", "images/ui/hasard.png", [self.placementAleatoire])
        self.btSup = Bouton(TB1n, PTIBT1, "EFFACER", "images/ui/corbeille.png", [self.tousAuTiroir])
        # Between the worlds
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        fenetre = self.fen[self.actif]
        super().dessine()
        if self.play:
            if config[self.actif]['interface']:
                self.g1.dessine(int(xf-self.g1.largeur), 0)
                if config['dev']:
                    self.gDev.dessine(int(xf-self.gDev.largeur), self.g1.hauteur)
            if fenetre == self.plateau:
                if not self.plateau.bloque:
                    if self.delaiDepart <= 0:
                        self.deplace()
                    else:
                        self.delaiDepart -= 1
                else:
                    if self.phase != "placement":
                        self.plateau.bloque = False
            else:
                if not self.plateau.bloque:
                    self.plateau.bloque = True
        else:
            if not self.plateau.bloque:
                self.plateau.bloque = True
        if self.actif == 'placement' and self.phase == 'placement':
            if not self.deplaPlacement and self.pause <= 0:
                secteurs = ['no', 'n', 'ne', 'e', 'se', 's', 'so', 'o']
                if self.actuel == 0:
                    self.afficheSecteur(secteurs[self.fen['choix_zone'].action.resultat])
                elif self.actuel == 1:
                    self.afficheSecteur(secteurs[(self.fen['choix_zone'].action.resultat+4)%8])
                self.deplaPlacement = True
                self.pause = 100
            elif not self.affRec and not self.affTeleco:
                if self.tiroir.estApparu():
                    self.btSup.dessine(int(xf*0.05), int(yf*0.81))
                    self.btAlea.dessine(int(xf*0.05), int(yf*0.89))
                if len(self.tiroir) == 0:
                    self.btSup.dessine(int(xf*0.05), int(yf*0.81))
                    self.btAlea.dessine(int(xf*0.05), int(yf*0.89))
                    self.btValid.dessine(int(xf*0.99-self.btValid.getDims()[0]/2), int(yf-xf*0.01-self.btValid.getDims()[1]/2))
        elif self.actif == 'jeu' and self.phase == 'jeu':
            self.tour()
            if self.play:
                self.barre.dessine(self.indiqueTour)
        elif self.actif == 'fin' and self.phase == 'fin':
            if fenetre != self.plateau and not fenetre.lu:
                message = fenetre.regarde()
                if message == 1:
                    self.rejouer()
                elif message == 2:
                    self.nouveauMessage("ANOVEL_MENU")

    def deplace(self) -> None:
        x = get_mouse_x()
        y = get_mouse_y()
        if is_mouse_button_down(0):
            self.move = True
            if x != self.posCurseur[0] or y != self.posCurseur[1]:
                l = x - self.posCurseur[0]
                h = y - self.posCurseur[1]
                self.plateau.deplace(l, h)
                self.trajet = (self.trajet[0]+l, self.trajet[1]+h)
        elif self.trajet != (0, 0):
            self.glisse()
        self.posCurseur = (x, y)

    def glisse(self) -> None:
        if self.move:
            self.trajet = (int(self.trajet[0]/7), int(self.trajet[1]/7))
            self.move = False
        elif self.trajet != (0, 0):
            x = self.trajet[0]
            y = self.trajet[1]
            self.plateau.deplace(x, y)
            if x < 0:
                x = x + 1
            elif x > 0:
                x = x - 1
            if y < 0:
                y = y + 1
            elif y > 0:
                y = y - 1
            self.trajet = (x, y)

    def afficheSecteur(self, secteur: str) -> None:
        secteur = secteur.lower()
        if secteur == 'c':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'n':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        elif secteur == 'ne':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        elif secteur == 'e':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'se':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-xf)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 's':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'so':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'o':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'no':
            px = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
            py = int(self.plateau.largeurBordure+self.plateau.largeurEnvirronement/2)
        else:
            px = py = 0
        if px != 0 and py != 0:
            self.plateau.place(px, py, True)

    def focusBat(self) -> None:
        bat = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        case = self.trouveCase(bat)
        self.plateau.focusCase(case)

    def rejouer(self) -> None:
        super().rejouer()
        self.afficheSecteur('c')
        self.delaiDepart = 70

    def setPlay(self, etat: bool) -> None:
        self.play = etat
        self.tiroir.play = etat
        self.cible.play = etat
        self.rectangle.play = etat
        self.teleco.play = etat
        self.fleche.play = etat

    # Placement

    def tousAuTiroir(self) -> None:
        for i in range(len(self.zoneDep)):
            self.plateau[self.zoneDep[i][0]][self.zoneDep[i][1]].vide()
        self.tiroir.setListe(self.joueurs[self.actuel].bateaux)

    def placementAleatoire(self) -> None:
        if len(self.tiroir) == 0:
            self.tousAuTiroir()
        elif trouveParam('hasard') == 0:
            self.tousAuTiroir()
        while len(self.tiroir) > 0:
            bat = self.tiroir[0]
            self.tiroir.supValListe(0)
            lcase = self.zoneDep.cases
            cases = []
            for j in range(len(lcase)):
                if not self.plateau[lcase[j][0]][lcase[j][1]].estPleine():
                    cases.append(self.plateau[lcase[j][0]][lcase[j][1]])
            c1 = choice(cases)
            c2 = choice([0, 1, 2, 3])
            for k in range(c2):
                bat.droite()
            c1.ajoute(bat)

    # Jeu

    def tour(self) -> None:
        if not self.deplaPlacement:
            self.focusBat()
            self.deplaPlacement = True
            #self.barre.deplacement = True
        if self.barre.chabat:
            self.deplaPlacement = False
            self.barre.chabat = False
            self.setDeplacement = False

    def joueurSuivant(self) -> None:
        super().joueurSuivant()
        self.barre.setActuel(self.actuel)

    # Between the worlds
    def portailAustral(self) -> None:
        if self.play:
            i = 0
            v = False
            while i < len(self.opt) and not v:
                if self.opt[i][0].getContact():
                    v = True
                    self.nouveauMessage(self.opt[i][1])
                else:
                    i += 1

    def nouveauMessage(self, message: str) -> None:
        self.message = message
        self.lu = False