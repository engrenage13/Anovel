from objets.BateauJoueur import BateauJoueur
from systeme.FondMarin import *
from ui.bouton import Bouton
from objets.Joueur import Joueur
from objets.plateau import Plateau
from museeNoyee import mer

class Installateur:
    def __init__(self, joueur: Joueur, creator: object) -> None:
        """Crée la fenêtre d'installation de bateaux pour un joueur.

        Args:
            joueur (Joueur): Joueur concerné par l'installation.
            creator (Partie): Objet "Partie" qui a lancé l'installateur.
        """
        self.proprio = creator
        self.joueur = joueur
        self.liBat = self.joueur.getBateaux()
        self.listeBrillante = []
        self.plateau = Plateau(10, 10)
        self.btValid = Bouton([self.proprio.nouvelleEtape, self.verif], "Valider", [DARKBLUE, BLUE, WHITE])
        self.btValid.setTexteNotif("Action Impossible", "Vous devez placer tous vos bateaux.")

    def dessine(self) -> None:
        ory = int((yf-hbarre)/2-tailleCase*5)+hbarre
        draw_texture(mer, 0, 0, WHITE)
        self.barreTitre()
        self.plateau.dessine((tlatba, ory), tailleCase, self.listeBrillante)
        self.dessineBateaux([tlatba, ory, tailleCase, 10])
        self.btValid.dessine((int(xf-tlatba*0.5), ory+int(tailleCase*9.5)))

    def dessineBateaux(self, plateau: list) -> None:
        """Dessine tous les bateaux du joueur.

        Args:
            plateau (list): Infos sur le plateau.
        """
        for i in range(len(self.liBat)):
            if not self.liBat[i].pos and not self.liBat[i].defil:
                x = int(xf*0.01)
                y = int((yf*0.15)*(i+1))
            elif self.liBat[i].defil:
                coo = self.dansLeCadre(self.liBat[i])
                x = coo[0]
                y = coo[1]
                if x+self.liBat[i].coord[2] >= tlatba and x <= xf-tlatba:
                    if y+self.liBat[i].coord[3] >= plateau[1] and y <= plateau[1]+plateau[3]*tailleCase:
                        self.listeBrillante = self.getCasesCibles(plateau, self.liBat[i])
                    else:
                        self.listeBrillante = []
                else:
                    self.listeBrillante = []
            else:
                colonne = float(self.liBat[i].pos[0][1:len(self.liBat[i].pos[0])])
                ligne = float(self.plateau.alphabet.index(self.liBat[i].pos[0][0]))
                if self.liBat[i].orient == 'h':
                    colonne = colonne + self.liBat[i].taille/2
                    ligne = ligne + 0.5
                else:
                    colonne = colonne + 0.5
                    ligne = ligne + self.liBat[i].taille/2
                x = int(plateau[0]+plateau[2]*(colonne-1)-int(self.liBat[i].coord[2]/2))
                y = int(plateau[1]+plateau[2]*ligne-int(self.liBat[i].coord[3]/2))
            draw_text_pro(police1, self.liBat[i].nom, (int(xf*0.01), int((yf*0.15)*(i+1)-yf*0.03)), (0, 0),
                          0, 20, 0, WHITE)
            self.liBat[i].dessine(x, y)
            self.ckeckSelect(self.liBat[i])

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        draw_rectangle_gradient_h(0, 0, xf, hbarre, [112, 31, 126, 120], [150, 51, 140, 100])
        draw_text_pro(police1, f"Installation : {self.joueur.getNom()}", (int(hbarre/4), int(hbarre/4)), 
                      (0, 0), 0, 25, 0, WHITE)
        self.proprio.croix.dessine((xf-hbarre, int(hbarre*0.05)))

    def dansLeCadre(self, bateau: BateauJoueur) -> tuple:
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

    def ckeckSelect(self, bateau: BateauJoueur) -> bool:
        if is_mouse_button_pressed(0):
            if bateau.getContact():
                self.listeBrillante = []
                bateau.switchMode()
        elif is_mouse_button_pressed(1):
            if bateau.getContact():
                bateau.tourne()

    def getCasesCibles(self, plateau: list, bateau: BateauJoueur) -> list:
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
        contact = self.getContactBateaux(rep, self.liBat.index(bateau))
        if contact[0]:
            ididi = contact[1]
            if ididi >= len(rep):
                ididi = len(rep)-1
            rep[ididi] = False
            reponse = [rep, RED]
        return reponse

    def getContactBateaux(self, position: list, idBateau: int) -> bool:
        rep = False
        i = 0
        while i < len(position) and not rep:
            j = 0
            while j < len(self.liBat) and not rep:
                if j != idBateau and self.liBat[j].pos:
                    if position[i] in self.liBat[j].pos:
                        rep = True
                j = j + 1
            i = i + 1
        return [rep, i]

    def setJoueur(self, joueur: Joueur) -> None:
        self.joueur = joueur
        self.liBat = self.joueur.getBateaux()

    def verif(self) -> bool:
        """Vérifie si tous les bateaux du joueur ont étaient placés correctement.

        Returns:
            bool: True si tous les bateaux sont placés de manière acceptable.
        """
        rep = True
        i = 0
        while i < len(self.liBat) and rep:
            if not self.liBat[i].pos or False in self.liBat[i].pos:
                rep = False
            i = i + 1
        return rep