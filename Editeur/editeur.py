from systeme.FondMarin import *
from objets.Bateau import Bateau
from ui.bouton import Bouton
from ui.ptiBouton import PtiBouton
from ui.notif import Notification
from objets.Joueur import Joueur
from objets.plateau import Plateau
from Editeur.positionneur import Positionneur
from Editeur.tiroir import Tiroir
from Editeur.grilleBt import GrilleBt
from museeNoyee import mer

class Editeur:
    def __init__(self, joueur: Joueur, creator: object) -> None:
        """Crée la fenêtre d'installation de bateaux pour un joueur.

        Args:
            joueur (Joueur): Joueur concerné par l'installation.
            creator (Partie): Objet "Partie" qui a lancé l'éditeur.
        """
        self.createur = creator
        self.joueur = joueur
        self.lBat = self.joueur.getBateaux()
        self.bateaux = []
        self.ordre = []
        self.placeur = Positionneur(len(self.lBat))
        self.tiroir = Tiroir(self)
        self.tiroir.setListe(self.lBat)
        self.listeBrillante = []
        self.attente = 0
        self.plateau = Plateau(10, 10)
        # Boutons
        self.affG1 = False
        self.affG2 = False
        self.grille1 = GrilleBt()
        self.grille1.ajouteElement(PtiBouton([self.declencheG2, self.verification], [8, 223, 53, 255], 
                                             "Valider", "images/ui/check.png"), 0, 0)
        self.grille2 = GrilleBt()
        self.grille2.ajouteElement(PtiBouton([self.createur.nouvelleEtape, self.verif], [8, 223, 53, 255], 
                                             "Confirmer", "images/ui/check.png"), 0, 0)
        self.grille2.ajouteElement(PtiBouton([self.declencheG1], [207, 35, 41, 255], "Annuler", 
                                             "images/ui/croix.png"), 1, 0)
        ory = int((yf-hbarre)/2-tailleCase*5)+hbarre
        self.ymaxGrilles = [ory+int(tailleCase*10-self.grille1.hauteur), 
                            ory+int(tailleCase*10-self.grille2.hauteur)]
        self.yGrilles = [ory+int(tailleCase*10-self.grille1.hauteur), int(yf*1.1)]
        # Notifs
        self.notifs = []

    def dessine(self) -> None:
        """Dessine l'éditeur à l'écran.
        """
        ory = int((yf-hbarre)/2-tailleCase*5)+hbarre
        draw_texture(mer, 0, 0, WHITE)
        self.barreTitre()
        self.plateau.dessine((tlatba, ory), tailleCase, self.listeBrillante)
        self.dessineBateaux([tlatba, ory, tailleCase, 10])
        valid = self.verif()
        self.grille1.dessine(int(xf-tlatba+(tlatba-self.grille1.largeur)/2), self.yGrilles[0], 
                             [valid])
        self.grille2.dessine(int(xf-tlatba+(tlatba-self.grille2.largeur)/2), self.yGrilles[1], 
                             [valid, False])
        self.bougeGrille()
        i = 0
        survol = False
        y = int(yf*0.37)
        while i < len(self.notifs):
            notif = self.notifs[len(self.notifs)-i-1]
            notif.dessine(y)
            if notif.getDisparition():
                del self.notifs[i]
            else:
                i = i + 1
            if survol:
                del self.notifs[0]
            y = y - int(notif.hauteur)*1.05
            if y <= hbarre:
                survol = True
                y = int(yf*0.4)

    def dessineBateaux(self, plateau: list) -> None:
        """Dessine tous les bateaux du joueur.

        Args:
            plateau (list): Infos sur le plateau.
        """
        self.ordreBateaux()
        i = 0
        defil = False
        objectif = len(self.bateaux)
        if len(self.bateaux) > 0 and self.placeur.defil[self.lBat.index(self.bateaux[len(self.bateaux)-1])]:
            defil = True
            objectif = len(self.bateaux)-1
        while i < objectif:
            self.dessineBateau(self.bateaux[self.ordre[i]], plateau)
            i = i + 1
        self.tiroir.dessine(int((yf-hbarre)/2)+hbarre)
        if defil and len(self.bateaux) > 0 and i < len(self.bateaux):
            self.dessineBateau(self.bateaux[self.ordre[i]], plateau)

    def dessineBateau(self, bateau: Bateau, plateau: list) -> None:
        """Dessine un bateau.

        Args:
            bateau (Bateau): Bateau à dessiner.
            plateau (list): Infos sur le plateau.
        """
        cooBat = self.placeur.coords[self.lBat.index(bateau)]
        if self.placeur.defil[self.lBat.index(bateau)]:
            coo = self.dansLeCadre(bateau)
            x = coo[0]
            y = coo[1]
            if x+cooBat[2] >= tlatba and x <= xf-tlatba:
                if y+cooBat[3] >= plateau[1] and y <= plateau[1]+plateau[3]*tailleCase:
                    self.listeBrillante = self.getCasesCibles(plateau, bateau)
                else:
                    self.listeBrillante = []
            else:
                self.listeBrillante = []
            ima = bateau.dessine(x, y)
            self.placeur.setCoord(self.lBat.index(bateau), [x, y, ima.width, ima.height])
        elif not self.placeur.defil[self.lBat.index(bateau)] and bateau.pos:
            colonne = float(bateau.pos[0][1:len(bateau.pos[0])])
            ligne = float(self.plateau.alphabet.index(bateau.pos[0][0]))
            if bateau.orient == 'h':
                colonne = colonne + bateau.taille/2
                ligne = ligne + 0.5
            else:
                colonne = colonne + 0.5
                ligne = ligne + bateau.taille/2
            x = int(plateau[0]+plateau[2]*(colonne-1)-int(cooBat[2]/2))
            y = int(plateau[1]+plateau[2]*ligne-int(cooBat[3]/2))
            bateau.dessine(x, y)
        if self.attente <= 0:
            self.ckeckSelect(bateau)
        else:
            self.attente = self.attente - 1

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        draw_rectangle_gradient_h(0, 0, xf, hbarre, [112, 31, 126, 120], [150, 51, 140, 100])
        draw_text_pro(police1, f"Installation : {self.joueur.getNom()}", (int(hbarre/4), int(hbarre/4)), 
                      (0, 0), 0, 25, 0, WHITE)
        self.createur.croix.dessine((xf-hbarre, int(hbarre*0.05)))

    def ordreBateaux(self) -> None:
        """Determine dans quel ordre, il est préférable d'afficher les bateaux.
        """
        self.ordre = []
        for i in range(len(self.bateaux)):
            if not self.placeur.defil[self.lBat.index(self.bateaux[i])]:
                self.ordre = [i] + self.ordre
            else:
                self.ordre.append(i)

    def dansLeCadre(self, bateau: Bateau) -> tuple:
        """Trouve les coordonnées du bateau sur le plateau.

        Args:
            bateau (Bateau): Le bateau sélectionné.

        Returns:
            tuple: Les coordonnées (x, y) de l'origine du bateau.
        """
        cooBat = self.placeur.coords[self.lBat.index(bateau)]
        x = get_mouse_x()-int(cooBat[2]/2)
        y = get_mouse_y()-int(cooBat[3]/2)
        if x < 0:
            x = 0
        if x+cooBat[2] > xf:
            x = xf-cooBat[2]
        if y < hbarre:
            y = hbarre
        if y > yf-cooBat[3]:
            y = yf-cooBat[3]
        return (x, y)

    def ckeckSelect(self, bateau: Bateau) -> None:
        """Agit si l'une des touches de la souris est appuyée et que le pointeur est sur le bateau visé.

        Args:
            bateau (Bateau): Bateau sur lequel agir.
        """
        if self.placeur.getContact(self.lBat.index(bateau)):
            if is_mouse_button_pressed(0):
                self.listeBrillante = []
                signal = self.placeur.switchMode(self.lBat.index(bateau), bateau)
                if not signal and not bateau.pos:
                    if self.placeur.checkClone(bateau, self.tiroir.liste):
                        self.tiroir.ajValListe(bateau)
                    del self.bateaux[self.bateaux.index(bateau)]
                    self.ordreBateaux()
            elif is_mouse_button_pressed(1):
                self.placeur.tourne(self.lBat.index(bateau), bateau)

    def getCasesCibles(self, plateau: list, bateau: Bateau) -> list:
        """Renvoie les cases survolés par le bateau.

        Args:
            plateau (list): Coordonnées du plateau.
            bateau (Bateau): Le bateau cible.

        Returns:
            list: Liste de nom de cases.
        """
        rep = []
        couleur = BLACK
        zone = 1
        cooBat = self.placeur.coords[self.lBat.index(bateau)]
        if bateau.orient == 'h':
            indice = int((cooBat[1]+int(cooBat[3]/2)-plateau[1])/plateau[2])
            if indice < plateau[3] and indice >= 0:
                ligne = self.plateau.getLigne(self.plateau.alphabet[indice])
                zone = 2
                boucle = bateau.taille
                couleur = WHITE
                if cooBat[0] >= plateau[0]:
                    origine = int((cooBat[0]-plateau[0])/plateau[2])
                    sens = 1
                    if plateau[3]-origine < boucle:
                        boucle = plateau[3]-origine
                        couleur = RED
                        zone = 3
                else:
                    origine = int(((cooBat[0]+cooBat[2])-plateau[0])/plateau[2])
                    sens = -1
                    if origine < boucle:
                        boucle = origine+1
                        couleur = RED
                        zone = 1
                for i in range(boucle):
                    rep.append(ligne[origine+i*sens])
        else:
            indice = int((cooBat[0]+int(cooBat[2]/2)-plateau[0])/plateau[2])+1
            if indice <= plateau[3] and indice > 0:
                ligne = self.plateau.getColonne(indice)
                zone = 2
                boucle = bateau.taille
                couleur = WHITE
                if cooBat[1] >= plateau[1]:
                    origine = int((cooBat[1]-plateau[1])/plateau[2])
                    sens = 1
                    if plateau[3]-origine < boucle:
                        boucle = plateau[3]-origine
                        couleur = RED
                        zone = 3
                else:
                    origine = int(((cooBat[1]+cooBat[3])-plateau[1])/plateau[2])
                    sens = -1
                    if origine < boucle:
                        boucle = origine+1
                        couleur = RED
                        zone = 1
                for i in range(boucle):
                    rep.append(ligne[origine+i*sens])
        self.placeur.setPosition(rep, zone, bateau)
        reponse = rep
        if couleur != BLACK:
            reponse = [rep, couleur]
        contact = self.placeur.getCaseJumelles(rep, self.bateaux.index(bateau), self.bateaux)
        if contact[0]:
            ididi = contact[1]
            if ididi >= len(rep):
                ididi = len(rep)-1
            rep[ididi] = False
            reponse = [rep, RED]
        return reponse

    def setJoueur(self, joueur: Joueur) -> None:
        """Permet de changer le joueur qui utilise l'éditeur.

        Args:
            joueur (Joueur): Nouveau joueur.
        """
        self.joueur = joueur
        self.lBat = self.joueur.getBateaux()
        self.placeur.reset(len(self.lBat))
        self.tiroir.setListe(self.lBat)
        self.declencheG1()
        self.bateaux = []

    def verification(self) -> bool:
        """Affiche les notifications adaptées en fonction de la position des bateaux lors de la validation.

        Returns:
            bool: Si oui ou non, les bateaux sont bien placés.
        """
        rep = self.verif()
        if not rep:
            self.notifs.append(Notification("Vous devez placer tous vos bateaux.", 'd', [210, 7, 22, 255]))
        else:
            self.notifs.append(Notification("Sauvegarde termine", 'd', [8, 223, 53, 255]))
        return rep

    def declencheG2(self) -> None:
        """Déclenche le passage à la deuxième grille de bouton.
        """
        self.affG2 = True
        self.affG1 = False

    def declencheG1(self) -> None:
        """Déclenche le passage à la première grille de bouton.
        """
        self.affG1 = True
        self.affG2 = False

    def bougeGrille(self) -> None:
        """Permet de déplacer les grilles de boutons.
        """
        pas = int(yf*0.01)
        if self.affG2:
            if self.yGrilles[0] < int(yf*1.1):
                self.yGrilles[0] += pas
            elif self.yGrilles[1] > self.ymaxGrilles[1]:
                if self.yGrilles[1]-self.ymaxGrilles[1] < pas:
                    pas = self.yGrilles[1]-self.ymaxGrilles[1]
                self.yGrilles[1] -= pas
            else:
                self.affG2 = False
        elif self.affG1:
            if self.yGrilles[1] < int(yf*1.1):
                self.yGrilles[1] += pas
            elif self.yGrilles[0] > self.ymaxGrilles[0]:
                self.yGrilles[0] -= pas
            else:
                self.affG1 = False

    def verif(self) -> bool:
        """Vérifie si tous les bateaux du joueur ont étaient placés correctement.

        Returns:
            bool: True si tous les bateaux sont placés de manière acceptable.
        """
        rep = True
        i = 0
        if len(self.tiroir.liste) > 0:
            rep = False
        else:
            while i < len(self.bateaux) and rep:
                if not self.bateaux[i].pos or False in self.bateaux[i].pos:
                    rep = False
                i = i + 1
        return rep