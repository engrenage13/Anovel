from systeme.FondMarin import *
from BN.objets.Bateau import Bateau
from ui.bouton.bouton import Bouton
from ui.bouton.boutonPression import BoutonPression
from ui.bouton.grille import Grille
from BN.objets.Joueur import Joueur
from BN.objets.plateau import Plateau
from BN.Editeur.positionneur import Positionneur
from BN.Editeur.tiroir import Tiroir
from BN.Editeur.chronologie import Chronologie
from BN.collectionImage import mer

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
        self.grille = Grille(int(xf*0.15), [[255, 255, 255, 50], WHITE])
        self.grille.ajouteElement(Bouton(TB1o, PTIBT2, "ANNULER", "images/ui/annuler.png", [self.annuler]), 0, 0)
        self.grille.ajouteElement(Bouton(TB1o, PTIBT2, "RETABLIR", "images/ui/retablir.png", [self.retablir]), 1, 0)
        self.grille.ajouteElement(Bouton(TB1o, PTIBT2, "PLACEMENT ALEATOIRE", "images/ui/hasard.png", [self.alea]), 0, 1)
        self.grille.ajouteElement(Bouton(TB1o, PTIBT2, "EFFACER", "images/ui/corbeille.png", [self.tousAuTiroir]), 1, 1)
        self.grille.ajouteElement(BoutonPression(TB1o, BTNOIR, "VALIDER", "images/ui/check.png", 
                                    [self.createur.nouvelleEtape, self.verif]), 0, 2)
        # Chronologie
        self.chronologie = Chronologie(self.tiroir, self.lBat)

    def dessine(self) -> None:
        """Dessine l'éditeur à l'écran.
        """
        ory = int((yf-hbarre)/2-tailleCase*5)+hbarre
        draw_texture(mer, 0, 0, WHITE)
        self.barreTitre()
        self.plateau.dessine((tlatba, ory), tailleCase, self.listeBrillante)
        self.dessineBateaux([tlatba, ory, tailleCase, 10])
        self.grille.dessine(int(xf-self.grille.largeur-espaceBt*2), int(yf-self.grille.hauteur-espaceBt*2))

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
            if bateau.direction%2 == 0:
                colonne = colonne + bateau.taille/2
                ligne = ligne + 0.5
            else:
                colonne = colonne + 0.5
                ligne = ligne + bateau.taille/2
            x = int(plateau[0]+plateau[2]*(colonne-1)-int(cooBat[2]/2))
            y = int(plateau[1]+plateau[2]*ligne-int(cooBat[3]/2))
            ima = bateau.dessine(x, y)
            if [x, y, ima.width, ima.height] != cooBat:
                self.placeur.setCoord(self.lBat.index(bateau), [x, y, ima.width, ima.height])
        if self.attente <= 0:
            self.ckeckSelect(bateau)
        else:
            self.attente = self.attente - 1

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        tx = f"INSTALLATION : {self.joueur.getNom().upper()}"
        tt = measure_text_ex(police1, tx, int(yf*0.05*0.7), 0)
        draw_rectangle_rounded([-tt.x*0.05, -tt.y*0.1, tt.x*1.1, yf*0.05*1.05], 0.15, 25, [112, 31, 126, 120])
        draw_text_pro(police1, tx, (int(hbarre/5), int(hbarre/6)), (0, 0), 0, int(hbarre*0.7), 0, WHITE)

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
                if not signal:
                    self.chronologie.nouvelleSauvegarde()
                    if not bateau.pos:
                        if self.placeur.checkClone(bateau, self.tiroir.liste):
                            self.tiroir.ajValListe(bateau)
                        del self.bateaux[self.bateaux.index(bateau)]
                        self.ordreBateaux()
            elif is_mouse_button_pressed(1):
                self.placeur.tourne(self.lBat.index(bateau), bateau)

    def alea(self) -> None:
        for i in range(len(self.lBat)):
            bateau = self.lBat[i]
            if bateau in self.tiroir.liste:
                self.bateaux.append(bateau)
                self.tiroir.supValListe(self.tiroir.liste.index(bateau))
        self.placeur.placementAleatoire(self.lBat, self.plateau)
        self.chronologie.nouvelleSauvegarde()

    def tousAuTiroir(self) -> None:
        """Permet de remettre tous les bateaux placés dans le tirroir.
        """
        taille = len(self.bateaux)
        for i in range(len(self.bateaux)):
            bateau = self.bateaux[i]
            bateau.pos = False
            if bateau.direction != 0:
                bateau.direction = 0
            self.tiroir.ajValListe(bateau)
        self.bateaux = []
        if taille > 0:
            self.chronologie.nouvelleSauvegarde()

    def annuler(self) -> None:
        """Permet d'annuler la dernière action effectuée.
        """
        self.chronologie.annuler()
        self.bateaux = self.chronologie.retablirSauvegarde()

    def retablir(self) -> None:
        """Permet de rétablir la dernière action annulée.
        """
        self.chronologie.retablir()
        self.bateaux = self.chronologie.retablirSauvegarde()

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
        if bateau.direction%2 == 0:
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
        self.chronologie.setBateaux(self.lBat)
        self.chronologie.reset()
        self.bateaux = []

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