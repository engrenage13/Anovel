from objets.Bateau import Bateau
from systeme.FondMarin import *
from systeme.set import trouveParam
from objets.Joueur import Joueur
from museeNoyee import viseur, mer
from objets.plateau import Plateau
from ui.notif import Notification

class Attaque:
    def __init__(self, joueur1: Joueur, joueur2: Joueur, createur: object) -> None:
        """Gère toute la partie attaque du jeu.

        Args:
            joueur1 (Joueur): L'un des deux joueurs.
            joueur2 (Joueur): L'autre joueur.
            createur (Partie): Partie qui est en cours.
        """
        self.proprio = createur
        self.play = True
        # Joueurs
        self.j1 = joueur1
        self.j2 = joueur2
        self.joueurs = [joueur1, joueur2]
        self.gagnant = False
        # /Joueurs
        self.joueurActuel = self.j1
        self.liBat = self.j2.getBateaux()
        # Plateaux
        self.p1 = Plateau(10, 10)
        self.p2 = Plateau(10, 10)
        self.plateaux = [self.p1, self.p2]
        self.plateauYCible = int((yf-hbarre)/2-tailleCase*5)+hbarre
        self.yPlateau = self.plateauYCible
        # /Plateaux
        self.viseur = True
        self.tour = 0
        self.incrementTour()
        # Notification
        self.notifs = []

    def dessine(self) -> None:
        """Dessine les éléments du jeu de la partie attaque à l'écran.
        """
        draw_texture(mer, 0, 0, WHITE)
        for i in range(len(self.plateaux)):
            self.plateaux[i].dessine((tlatba, self.yPlateau+yf*i), tailleCase)
        if trouveParam("stats") == 1:
            self.stats(self.joueurActuel)
        self.barreTitre()
        if self.play:
            if self.viseur:
                posiCurseur = self.localiseCurseur([tlatba, self.plateauYCible, tailleCase], 
                                                self.joueurs.index(self.joueurActuel))
                if posiCurseur:
                    viseur = self.dessineViseur(posiCurseur[0], posiCurseur[1])
                    if is_mouse_button_pressed(0):
                        tire = self.tire(viseur, self.joueurs.index(self.joueurActuel))
                        if self.getDefaite(self.joueurs[len(self.joueurs)-1-self.joueurs.index(self.joueurActuel)]):
                            self.gagnant = self.joueurActuel
                            self.proprio.nouvelleEtape()
                            self.play = False
                        if viseur.lower() != 'x':
                            if tire[2] != 'o':
                                self.startNotif(self.liBat[tire[1]], viseur)
                            self.joueurActuel.toucheCase(tire[0])
                            self.viseur = False
            else:
                if self.joueurActuel == self.j1:
                    self.monter()
                else:
                    self.descendre()
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

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        ttour = measure_text_ex(police1, f"Tour {self.tour}", int(hbarre*0.7), 0)
        draw_rectangle_gradient_h(0, 0, xf, hbarre, [112, 31, 126, 120], [150, 51, 140, 100])
        draw_text_pro(police1, self.joueurActuel.getNom(), (int(hbarre/4), int(hbarre/4)), 
                      (0, 0), 0, int(hbarre*0.7), 0, WHITE)
        draw_text_pro(police1, f"Tour {self.tour}", (int(xf/2-ttour.x/2), int(hbarre/4)), 
                      (0, 0), 0, int(hbarre*0.7), 0, WHITE)
        if not self.gagnant:
            self.proprio.croix.dessine((xf-hbarre, int(hbarre*0.05)))
            self.proprio.rouage.dessine((int(xf-hbarre*2.05), int(hbarre*0.05)))

    def incrementTour(self) -> None:
        """Incrémente le compteur de tour
        """
        self.tour = self.tour + 1

    def stats(self, joueur: Joueur) -> None:
        """Affiche les statistiques du joueurs de l'indice passé en paramètre.

        Args:
            joueur (Joueur): Joueur dont les stats doivent être affichés.
        """
        l = ["Nb. Cases Touchees", "Touches", "Rates"]
        lv = joueur.getStats()
        x = int(xf*0.005)
        denivX = int(-xf*0.06)
        y = int(yf*0.115)
        taille = int(yf*0.03)
        texte = ""
        for i in range(len(l)):
            if type(lv[i]) != list:
                t = f"{l[i]} : {lv[i]}"
            else:
                t = f"{l[i]} : {lv[i][0]} ({lv[i][1]}%)"
            if i < len(l)-1:
                t = t + "\n"
            texte += t
        tt = measure_text_ex(police2, texte, taille, 0)
        draw_rectangle_rounded((denivX, y, int(tt.x*1.13+denivX*-1), int(tt.y*1.2)), 
                                0.2, 30, [255, 255, 255, 50])
        draw_rectangle_rounded_lines((denivX, y, int(tt.x*1.13+denivX*-1), int(tt.y*1.2)), 0.2, 30, 3, WHITE)
        y += int(tt.y*0.1)
        draw_text_pro(police2, texte, (x, y), (0, 0), 0, taille, 0, WHITE)

    def dessineViseur(self, coo: tuple, case: tuple) -> str:
        """Dessine le curseur aux coordonnées passés en paramètres.

        Args:
            coo (tuple): Là où apparaitra le curseur (les coordonnées de la case).
            case (tuple): La case survolée.
        """
        draw_rectangle_lines_ex([coo[0], coo[1], tailleCase, tailleCase], 3, WHITE)
        draw_texture(viseur, int(coo[0]+tailleCase/2-viseur.width/2), int(coo[1]+tailleCase/2-viseur.height/2), 
                     WHITE)
        if case[1] == '':
            texte = case[0]
            couleur = WHITE
        else:
            texte = "X"
            couleur = ORANGE
        longueurTexte = measure_text_ex(police2, texte, 20, 0)
        draw_text_pro(police2, texte, (int(coo[0]+tailleCase/2-longueurTexte.x/2), 
                      int(coo[1]+tailleCase/2-longueurTexte.y/2)), (0, 0), 0, 20, 0, couleur)
        return texte
    
    def localiseCurseur(self, plateau: list, codeJ: int) -> tuple:
        """Regarde la position du curseur sur le plateau et renvoie le code de la case corespondante.

        Args:
            plateau (list): Informations importantes sur le plateau.
            codeJ (int): Le joueur en train de jouer.

        Returns:
            tuple: La case sur laquelle se trouve le curseur.
        """
        x = get_mouse_x()
        y = get_mouse_y()
        rep = False
        plat = self.plateaux[codeJ]
        dims = plat.getDimensions()
        if x >= plateau[0] and x < plateau[0]+dims[0]*plateau[2]:
            if y >= plateau[1] and y < plateau[1]+dims[1]*plateau[2]:
                indicey = int((y-plateau[1])/plateau[2])
                ligne = plat.getLigne(plat.alphabet[indicey])
                indicex = int((x-plateau[0])/plateau[2])
                rep = ligne[indicex]
        if rep:
            rep = ((int(plateau[0]+indicex*plateau[2]), int(plateau[1]+indicey*plateau[2])), 
                   plat.cases[indicey][indicex])
        return rep

    def tire(self, texte: str, codeJ: int) -> list:
        """Définit ce qui se passe quand le joueur tire sur une case.

        Args:
            texte (str): Le texte écrit sur le viseur.
            codeJ (int): L'indice du joueur qui a tiré.
        """
        if texte.lower() != 'x':
            plat = self.plateaux[codeJ]
            trouve = False
            i = 0
            while i < plat.getDimensions()[0] and not trouve:
                j = 0
                while j < plat.getDimensions()[1] and not trouve:
                    if plat.cases[i][j][0] == texte:
                        symbole = 'o'
                        k = 0
                        touche = False
                        while k < len(self.liBat) and not touche:
                            if self.liBat[k].estTouche(texte):
                                symbole = 'x'
                                touche = True
                            else:
                                k = k + 1
                        if k >= len(self.liBat):
                            k = len(self.liBat)-1
                        plat.cases[i][j][1] = symbole
                        trouve = True
                    else:
                        j = j + 1
                i = i + 1
            return [touche, k, symbole]

    def getDefaite(self, joueur: Joueur) -> bool:
        """Vérifie si le joueur a encore des bateaux non-coulés.

        Args:
            joueur (Joueur): Le joueur testé.

        Returns:
            bool: True si tous les bateaux du joueur ont coulés.
        """
        rep = True
        i = 0
        libat = joueur.getBateaux()
        while i < len(libat) and rep:
            if not libat[i].estCoule():
                rep = False
            i = i + 1
        return rep

    def startNotif(self, bateau: Bateau, case: str) -> None:
        """Lance l'affichage de la notif.

        Args:
            bateau (Bateau): Le bateau touché.
            case (str): La case touché.
        """
        titre = "Touche"
        if bateau.estCoule():
            titre = "Coule"
        texte = f"{titre} En {case}"
        self.notifs.append(Notification(texte, 'g', [0, 50, 240, 255]))

    def monter(self):
        """Fait descendre les plateaux (animations)
        """
        pas = int(yf*0.02)
        self.yPlateau = self.yPlateau - pas
        if self.yPlateau <= self.plateauYCible-yf:
            self.yPlateau = self.plateauYCible-yf
            self.viseur = True
            self.joueurActuel = self.j2
            self.liBat = self.j1.getBateaux()

    def descendre(self):
        """Fait monter les plateaux (animations)
        """
        pas = int(yf*0.02)
        self.yPlateau = self.yPlateau + pas
        if self.yPlateau >= self.plateauYCible:
            self.yPlateau = self.plateauYCible
            self.viseur = True
            self.joueurActuel = self.j1
            self.liBat = self.j2.getBateaux()
            self.incrementTour()

    def rejouer(self) -> None:
        """Réinitialise certains paramètre de la partie pour rejouer.
        """
        for i in range(len(self.plateaux)):
            self.plateaux[i].reinitialise()
        self.tour = 1
        self.play = True
        self.gagnant = False
        self.viseur = True
        self.yPlateau = self.plateauYCible
        self.joueurActuel = self.j1
        self.liBat = self.j2.getBateaux()
        self.notifs = []