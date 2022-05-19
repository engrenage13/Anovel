from objets.Bateau import Bateau
from systeme.FondMarin import *
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
        # Joueurs
        self.j1 = joueur1
        self.j2 = joueur2
        self.joueurs = [joueur1, joueur2]
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
        self.notif = Notification("", "")
        self.affinotif = False
        # /Notification

    def dessine(self) -> None:
        draw_texture(mer, 0, 0, WHITE)
        for i in range(len(self.plateaux)):
            self.plateaux[i].dessine((tlatba, self.yPlateau+yf*i), tailleCase)
        self.stats(self.joueurActuel)
        self.barreTitre()
        if self.viseur:
            posiCurseur = self.localiseCurseur([tlatba, self.plateauYCible, tailleCase], 
                                               self.joueurs.index(self.joueurActuel))
            if posiCurseur:
                viseur = self.dessineViseur(posiCurseur[0], posiCurseur[1])
                if is_mouse_button_pressed(0):
                    tire = self.tire(viseur, self.joueurs.index(self.joueurActuel))
                    if self.getDefaite(self.joueurs[len(self.joueurs)-1-self.joueurs.index(self.joueurActuel)]):
                        self.proprio.nouvelleEtape()
                    elif viseur.lower() != 'x':
                        if tire[2] != 'o':
                            self.startNotif(self.liBat[tire[1]], viseur)
                        self.joueurActuel.toucheCase(tire[0])
                        self.viseur = False
        else:
            if self.affinotif:
                self.notif.dessine()
                if self.notif.getDisparition():
                    self.affinotif = False
            else:
                if self.joueurActuel == self.j1:
                    self.monter()
                else:
                    self.descendre()

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        ttour = measure_text_ex(police1, f"Tour {self.tour}", 25, 0)
        draw_rectangle_gradient_h(0, 0, xf, hbarre, [112, 31, 126, 120], [150, 51, 140, 100])
        draw_text_pro(police1, self.joueurActuel.getNom(), (int(hbarre/4), int(hbarre/4)), (0, 0), 0, 25, 0, WHITE)
        draw_text_pro(police1, f"Tour {self.tour}", (int(xf/2-ttour.x/2), int(hbarre/4)), 
                      (0, 0), 0, 25, 0, WHITE)
        self.proprio.croix.dessine((xf-hbarre, int(hbarre*0.05)))

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
        y = int(yf*0.09)
        for i in range(len(l)):
            if type(lv[i]) != list:
                t = f"{l[i]} : {lv[i]}"
            else:
                t = f"{l[i]} : {lv[i][0]} ({lv[i][1]}%)"
            longueur = measure_text_ex(police2, t, 20, 0)
            x = int(xf*0.99 - longueur.x)
            draw_text_pro(police2, t, (x, y), (0, 0), 0, 20, 0, WHITE)
            y = int(y + yf*0.05)

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
        titre = "Touche"
        if bateau.estCoule():
            titre = "Coule"
        texte = f"En {case}"
        self.notif.modifTitre(titre)
        self.notif.modifTexte(texte)
        self.affinotif = True

    def attaque(self, joueur: object, position: float) -> None:
        """Reboucle tant que le joueur n'a pas attaqué.

        Args:
            joueur (object): Le joueur qui doit attaqué.
            position (float): La position y du haut du plateau.
        """
        #fond.delete('pointeur')
        #d = fond.find_withtag('ecranFin')
        if not self.getEtatNotifs(joueur):
            a = self.localiseCurseur(joueur.cTire)
            #if a != None and len(d) == 0:
                #b = fond.coords(a)
                #self.dessineViseur(b, a)
        ligne = joueur.cTire.getLigne('a')
        #c = fond.coords(ligne[0])
        #if int(c[1]) == int(position) and len(d) == 0:
            #fond.after(50, self.attaque, joueur, c[1])
        #else:
            #fond.delete('pointeur')

    def getEtatNotifs(self, joueur: Joueur) -> bool:
        """Regarde si les notification d'un joueur son visible à l'écran.

        Args:
            joueur (Joueur): Propriétaire des informations à vérifier.

        Returns:
            bool: True s'il y a au moins une notif et False sinon.
        """
        rep = joueur.notifTouche.getEtat()
        if not rep:
            rep = joueur.notifCoule.getEtat()
        return rep

    def marquerCase(self, idCase: str, idplateau: str, joueurCible: Joueur, joueur: Joueur) -> None:
        """Marque les cases touchées.

        Args:
            idCase (str): Le code de la case.
            idplateau (str): Le plateau auquel elle correspond.
            joueurCible (Joueur): Le joueur victime du tir.
            joueur (Joueur): Le joueur qui est en train de jouer.
        """
        tag = idCase+idplateau
        #i = rate
        listeBateau = self.listeBateaux1
        if joueurCible == self.j2:
            listeBateau = self.listeBateaux2
        repTouche = joueurCible.estToucheBateau(idCase)
        #if repTouche[0]:
            #i = touche
        #fond.itemconfigure('i'+tag, image=i)
        bateaux = joueurCible.getBateaux()
        if bateaux[repTouche[1]].estCoule() and not listeBateau[repTouche[1]]:
            listeBateau[repTouche[1]] = True
            joueur.notifCoule.modifMessage(idCase)
            joueur.notifCoule.montre()
        elif repTouche[0]:
            joueur.notifTouche.modifMessage(idCase)
            joueur.notifTouche.montre()

    def getEtatCase(self, idCase: str, idPlateau: str="") -> bool:
        """Renvoie True si la case passée en paramètre est touchable.

        Args:
            idCase (str): Le code de la case à tester
            idPlateau (str, optional): Le code du plateau si l'on ne dispose que du nom de la case. Defaults to "".

        Returns:
            bool: Vrai ou Faux selon la possibilité de touché ou non la case.
        """
        tag = idCase+idPlateau
        rep = True
        #case = fond.itemcget('i'+tag, 'image')
        #if case != '':
            #rep = False
        return rep

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

    def monterOuQuitter(self):
        """Vérifie si le premier joueur a perdu, ou si le second joueur n'a pas de notif, 
           sinon il déclenche le tour du premier joueur.
        """
        if self.j1.aPerdu():
            #Fin(self.joueurs, 1, self.tour)
        #elif not self.getEtatNotifs(self.j2):
            self.monter(pasApas)
        #else:
            #fond.after(50, self.monterOuQuitter)

    def descendreOuQuitter(self):
        """Vérifie si le second joueur a perdu, ou si le premier joueur n'a pas de notif, 
           sinon il déclenche le tour du second joueur.
        """
        if self.j2.aPerdu():
            #Fin(self.joueurs, 0, self.tour)
        #elif not self.getEtatNotifs(self.j1):
            self.descendre(pasApas)
        #else:
            #fond.after(50, self.descendreOuQuitter)

    def deconnect(self):
        """Supprimme les événements liés au clic de la souris.
        """
        #fond.tag_unbind('pointeur', '<Button-1>')

    def connect(self):
        """(Re)crée les événements liés au clic de la souris.
        """
        #fond.tag_bind('pointeur', '<Button-1>', self.cliqueCurseur)

    def cliqueCurseur(self, event):
        """Réagis à un clique sur le curseur.

        Args:
            event (_type_): _description_
        """
        #t = fond.itemcget('affiTgVis', 'text')
        #if t != "X":
            #self.deconnect()
            #p1 = self.getEtatCase(t, 'c1')
            #p2 = self.getEtatCase(t, 'c2')
            #if p1 or p2:
                #ligne = self.j1.cTire.getLigne('a')
                #c = fond.coords(ligne[0])
                #if int(c[1]) == int(origyp):
                    #self.j1.toucheCase(self.j2.estToucheBateau(t)[0])
                    #self.affStats(0)
                    #self.marquerCase(t, 'c1', self.j2, self.j1)
                    #fond.after(1000, self.descendreOuQuitter)
                #else:
                    #self.j2.toucheCase(self.j1.estToucheBateau(t)[0])
                    #self.affStats(1)
                    #self.marquerCase(t, 'c2', self.j1, self.j2)
                    #fond.after(1000, self.monterOuQuitter)