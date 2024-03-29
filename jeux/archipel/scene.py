from random import choice, shuffle
from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.boutonPression import BoutonPression
from ui.bouton.grille import Grille
from jeux.archipel.fonctions.bases import TAILLECASE
from jeux.archipel.Jeu import Jeu, config
from systeme.set import trouveParam

class Scene(Jeu):
    """La scène de jeu.

    Args:
        Jeu (Jeu): Hérite de toute la structure du jeu.
    """
    def __init__(self) -> None:
        """Met en place la scène.
        """
        super().__init__()
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "ARCHIPEL_MENU"]]
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
        """Dessine le jeu est la scène.
        """
        fenetre = self.fen[self.actif]
        super().dessine()
        if self.play:
            if config[self.actif]['interface']:
                self.g1.dessine(int(xf-self.g1.largeur), 0)
                if is_key_pressed(256):
                    self.openMenu()
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
                #secteurs = ['n', 'e', 's', 'o']
                if self.actuel == 0:
                    self.afficheSecteur(secteurs[self.fen['choix_zone'].action.resultat])
                elif self.actuel == 1:
                    self.afficheSecteur(secteurs[(self.fen['choix_zone'].action.resultat+int(len(self.fen['choix_zone'].zones)/2))%len(self.fen['choix_zone'].zones)])
                self.deplaPlacement = True
                self.pause = 100
            elif not self.affRec and not self.affTeleco:
                ecart = int(yf*0.01)
                y = int(yf-ecart-self.btAlea.getDims()[1]/2)
                if self.tiroir.estApparu() or len(self.tiroir) == 0:
                    self.btAlea.dessine(int(ecart+self.btAlea.getDims()[0]/2), y)
                    y -= int(self.btAlea.getDims()[1]/2+self.btSup.getDims()[1]/2+ecart)
                    self.btSup.dessine(int(ecart+self.btSup.getDims()[0]/2), y)
                    if len(self.tiroir) == 0:
                        self.btValid.dessine(int(xf-ecart-self.btValid.getDims()[0]/2), int(yf-ecart-self.btValid.getDims()[1]/2))
                    if is_key_pressed(261):
                        self.tousAuTiroir()
                    if is_key_pressed(82):
                        self.placementAleatoire()
        elif self.actif == 'jeu' and self.phase == 'jeu':
            self.tour()
            if self.play:
                self.barre.dessine(self.indiqueTour, self.tourmax)
        elif self.actif == 'fin' and self.phase == 'fin':
            if fenetre != self.plateau and not fenetre.lu:
                message = fenetre.regarde()
                if message == 1:
                    self.rejouer()
                elif message == 2:
                    self.nouveauMessage("ANOVEL_MENU")

    def deplace(self) -> None:
        """Déplace la caméra.
        """
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
        """Fait glisser la caméra.
        """
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
        """Affiche un secteur particulier du plateau.

        Args:
            secteur (str): Le secteur qui a le focus.
        """
        secteur = secteur.lower()
        if secteur == 'c':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'n':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = int(self.plateau.largeurEnvirronement/2)
        elif secteur == 'ne':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-xf)
            py = int(self.plateau.largeurEnvirronement/2)
        elif secteur == 'e':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-xf)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'se':
            px = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-xf)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 's':
            px = int(-(len(self.plateau)*TAILLECASE)/2+xf/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'so':
            px = int(self.plateau.largeurEnvirronement/2)
            py = -int(len(self.plateau)*TAILLECASE+self.plateau.largeurEnvirronement/2-yf)
        elif secteur == 'o':
            px = int(self.plateau.largeurEnvirronement/2)
            py = int(-(len(self.plateau)*TAILLECASE)/2+yf/2)
        elif secteur == 'no':
            px = int(self.plateau.largeurEnvirronement/2)
            py = int(self.plateau.largeurEnvirronement/2)
        else:
            px = py = 0
        if px != 0 and py != 0:
            self.plateau.place(px, py, True)

    def focusBat(self) -> None:
        """Centre le bateau dont le tour vient de commencer.
        """
        bat = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        case = self.trouveCase(bat)
        self.plateau.focusCase(case)

    def rejouer(self) -> None:
        """Réinitialise certains paramètres afin de pouvoir rejouer une autre partie.
        """
        super().rejouer()
        self.afficheSecteur('c')
        self.delaiDepart = 70

    def setPlay(self, etat: bool) -> None:
        """Bloque/Débloque la caméra.

        Args:
            etat (bool): True pour débloquer, False pour bloquer.
        """
        self.play = etat
        self.tiroir.play = etat
        self.cible.play = etat
        self.rectangle.play = etat
        self.teleco.play = etat
        self.fleche.play = etat

    # Placement

    def tousAuTiroir(self) -> None:
        """Remet tous les bateaux placés du joueur actif dans le tiroir.
        """
        for i in range(len(self.zoneDep)):
            self.plateau[self.zoneDep[i][0]][self.zoneDep[i][1]].vide()
        self.tiroir.setListe(self.joueurs[self.actuel].bateaux)

    def placementAleatoire(self) -> None:
        """Place tous les bateaux du joueur actif de manière aléatoire.
        """
        if len(self.tiroir) == 0:
            self.tousAuTiroir()
            shuffle(self.joueurs[self.actuel].bateaux)
        while len(self.tiroir) > 0:
            bat = self.tiroir[0]
            self.tiroir.supValListe(0)
            lcase = self.zoneDep.cases
            cases = []
            for j in range(len(lcase)):
                if not self.plateau[lcase[j][0]][lcase[j][1]].estPleine():
                    if not self.plateau[lcase[j][0]][lcase[j][1]].marqueur:
                        cases.append(self.plateau[lcase[j][0]][lcase[j][1]])
            c1 = choice(cases)
            c2 = choice([0, 1, 2, 3])
            for k in range(c2):
                bat.droite()
            c1.ajoute(bat)
        self.joueurs[self.actuel].setIds()

    # Jeu

    def tour(self) -> None:
        """Définit certains paramètres pour la gestion de l'interface pendant la partie.
        """
        if not self.deplaPlacement:
            self.focusBat()
            self.deplaPlacement = True
        if self.barre.chabat:
            self.deplaPlacement = False
            self.barre.chabat = False
            self.setDeplacement = False

    def joueurSuivant(self) -> None:
        """Passe au joueur suivant.
        """
        super().joueurSuivant()
        self.barre.setActuel(self.actuel)

    # Between the worlds
    def portailAustral(self) -> None:
        """Recherche quel bouton a était cliqué pour savoir quel action exécuter.
        """
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
        """Rédige un message au système d'Archipel.

        Args:
            message (str): Le message à transmettre.
        """
        self.message = message
        self.lu = False

    def openMenu(self) -> None:
        """Ouvre le menu.
        """
        self.message = "ARCHIPEL_MENU"
        self.lu = False