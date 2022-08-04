from objets.BateauJoueur import BateauJoueur
from systeme.FondMarin import *
from ui.bouton import Bouton
from ui.notif import Notification
from objets.Joueur import Joueur
from objets.plateau import Plateau
from Editeur.tiroir import Tiroir
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
        self.bateaux = []
        self.ordre = []
        self.tiroir = Tiroir(self)
        self.tiroir.setListe(self.joueur.getBateaux())
        self.listeBrillante = []
        self.attente = 0
        self.plateau = Plateau(10, 10)
        # Boutons
        self.btValid = Bouton([self.createur.nouvelleEtape, self.verification], [8, 223, 53, 255], "Valider")
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
        self.btValid.dessine((int(xf-tlatba*0.5), ory+int(tailleCase*9.5)), True)
        i = 0
        survol = False
        y = int(yf*0.4)
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
        if len(self.bateaux) > 0 and self.bateaux[len(self.bateaux)-1].defil:
            defil = True
            objectif = len(self.bateaux)-1
        while i < objectif:
            self.dessineBateau(self.bateaux[self.ordre[i]], plateau)
            i = i + 1
        self.tiroir.dessine(int((yf-hbarre)/2)+hbarre)
        if defil and len(self.bateaux) > 0 and i < len(self.bateaux):
            self.dessineBateau(self.bateaux[self.ordre[i]], plateau)

    def dessineBateau(self, bateau: BateauJoueur, plateau: list) -> None:
        """Dessine un bateau.

        Args:
            bateau (BateauJoueur): Bateau à dessiner.
            plateau (list): Infos sur le plateau.
        """
        if bateau.defil:
            coo = self.dansLeCadre(bateau)
            x = coo[0]
            y = coo[1]
            if x+bateau.coord[2] >= tlatba and x <= xf-tlatba:
                if y+bateau.coord[3] >= plateau[1] and y <= plateau[1]+plateau[3]*tailleCase:
                    self.listeBrillante = self.getCasesCibles(plateau, bateau)
                else:
                    self.listeBrillante = []
            else:
                self.listeBrillante = []
            bateau.dessine(x, y)
        elif not bateau.defil and bateau.pos:
            colonne = float(bateau.pos[0][1:len(bateau.pos[0])])
            ligne = float(self.plateau.alphabet.index(bateau.pos[0][0]))
            if bateau.orient == 'h':
                colonne = colonne + bateau.taille/2
                ligne = ligne + 0.5
            else:
                colonne = colonne + 0.5
                ligne = ligne + bateau.taille/2
            x = int(plateau[0]+plateau[2]*(colonne-1)-int(bateau.coord[2]/2))
            y = int(plateau[1]+plateau[2]*ligne-int(bateau.coord[3]/2))
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
            if not self.bateaux[i].defil:
                self.ordre = [i] + self.ordre
            else:
                self.ordre.append(i)

    def dansLeCadre(self, bateau: BateauJoueur) -> tuple:
        """Trouve les coordonnées du bateau sur le plateau.

        Args:
            bateau (BateauJoueur): Le bateau sélectionné.

        Returns:
            tuple: Les coordonnées (x, y) de l'origine du bateau.
        """
        x = get_mouse_x()-int(bateau.coord[2]/2)
        y = get_mouse_y()-int(bateau.coord[3]/2)
        if x < 0:
            x = 0
        if x+bateau.coord[2] > xf:
            x = xf-bateau.coord[2]
        if y < hbarre:
            y = hbarre
        if y > yf-bateau.coord[3]:
            y = yf-bateau.coord[3]
        return (x, y)

    def ckeckSelect(self, bateau: BateauJoueur) -> None:
        """Agit si l'une des touches de la souris est appuyée et que le pointeur est sur le bateau visé.
        """
        if is_mouse_button_pressed(0):
            if bateau.getContact():
                self.listeBrillante = []
                signal = bateau.switchMode()
                if not signal and not bateau.pos:
                    if self.checkClone(bateau, self.tiroir.liste):
                        self.tiroir.ajValListe(bateau)
                    del self.bateaux[self.bateaux.index(bateau)]
                    self.ordreBateaux()
        elif is_mouse_button_pressed(1):
            if bateau.getContact():
                bateau.tourne()

    def checkClone(self, valeur: object, liste: list) -> bool:
        """Vérifie si la valeur est déjà dans la liste.

        Args:
            valeur (object): Valeur à vérifier.
            liste (list): Liste où il faut vérifier.

        Returns:
            bool: True si la valeur n'est pas dans une liste, False sinon.
        """
        rep = True
        if valeur in liste:
            rep = False
        return rep

    def getCasesCibles(self, plateau: list, bateau: BateauJoueur) -> list:
        """Renvoie les cases survolés par le bateau.

        Args:
            plateau (list): Coordonnées du plateau.
            bateau (BateauJoueur): Le bateau cible.

        Returns:
            list: Liste de nom de cases.
        """
        rep = []
        couleur = BLACK
        zone = 1
        if bateau.orient == 'h':
            indice = int((bateau.coord[1]+int(bateau.coord[3]/2)-plateau[1])/plateau[2])
            if indice < plateau[3] and indice >= 0:
                ligne = self.plateau.getLigne(self.plateau.alphabet[indice])
                zone = 2
                boucle = bateau.taille
                couleur = WHITE
                if bateau.coord[0] >= plateau[0]:
                    origine = int((bateau.coord[0]-plateau[0])/plateau[2])
                    sens = 1
                    if plateau[3]-origine < boucle:
                        boucle = plateau[3]-origine
                        couleur = RED
                        zone = 3
                else:
                    origine = int(((bateau.coord[0]+bateau.coord[2])-plateau[0])/plateau[2])
                    sens = -1
                    if origine < boucle:
                        boucle = origine+1
                        couleur = RED
                        zone = 1
                for i in range(boucle):
                    rep.append(ligne[origine+i*sens])
        else:
            indice = int((bateau.coord[0]+int(bateau.coord[2]/2)-plateau[0])/plateau[2])+1
            if indice <= plateau[3] and indice > 0:
                ligne = self.plateau.getColonne(indice)
                zone = 2
                boucle = bateau.taille
                couleur = WHITE
                if bateau.coord[1] >= plateau[1]:
                    origine = int((bateau.coord[1]-plateau[1])/plateau[2])
                    sens = 1
                    if plateau[3]-origine < boucle:
                        boucle = plateau[3]-origine
                        couleur = RED
                        zone = 3
                else:
                    origine = int(((bateau.coord[1]+bateau.coord[3])-plateau[1])/plateau[2])
                    sens = -1
                    if origine < boucle:
                        boucle = origine+1
                        couleur = RED
                        zone = 1
                for i in range(boucle):
                    rep.append(ligne[origine+i*sens])
        bateau.setPosition(rep, zone)
        reponse = rep
        if couleur != BLACK:
            reponse = [rep, couleur]
        contact = self.getContactBateaux(rep, self.bateaux.index(bateau))
        if contact[0]:
            ididi = contact[1]
            if ididi >= len(rep):
                ididi = len(rep)-1
            rep[ididi] = False
            reponse = [rep, RED]
        return reponse

    def getContactBateaux(self, position: list, idBateau: int) -> bool:
        """Vérifie si le bateau ne touche aucun autre bateau.

        Args:
            position (list): Les cases occupées par le bateau.
            idBateau (int): L'indice du bateau sélectionné.

        Returns:
            bool: True si le bateau est sur une case déjà occupé par un autre.
        """
        rep = False
        i = 0
        while i < len(position) and not rep:
            j = 0
            while j < len(self.bateaux) and not rep:
                if j != idBateau and self.bateaux[j].pos:
                    if position[i] in self.bateaux[j].pos:
                        rep = True
                j = j + 1
            i = i + 1
        return [rep, i]

    def setJoueur(self, joueur: Joueur) -> None:
        """Permet de changer le joueur qui utilise l'éditeur.

        Args:
            joueur (Joueur): Nouveau joueur.
        """
        self.joueur = joueur
        self.tiroir.setListe(self.joueur.getBateaux())
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