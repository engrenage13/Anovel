from systeme.FondMarin import *
from systeme.erreurs import e100
from systeme.set import trouveParam
from ui.blocTexte import BlocTexte

class PosiJauge:
    def __init__(self, points: list, prop: float=1) -> None:
        """Permet de créer une jauge à points.

        Args:
            points (list): Liste des points de la jauge.
            prop (float): multiplicateur pour la longueur passée en paramètres de 'dessine'. Default to 1.
        """
        self.origine = None
        self.hauteur = int(yf*0.01)
        self.prop = prop
        self.longueur = int(xf*prop)
        self.erreurs = []
        self.lu = True
        # Curseur
        self.posMin = self.hauteur
        self.posMax = self.longueur-self.hauteur
        self.posCurseur = self.posMin
        self.largeur = self.hauteur*2
        self.defil = False
        self.couleurCurseur = [(0, 24, 48), (12, 48, 47), [0, 24, 48]]
        # Points
        self.valeur = None
        self.ptOriginaux = points
        self.points = []
        self.set = False
        self.transparenceCurseur = [0, 135, 0, True]
        self.lMaxPSelect = int(self.hauteur*2.5)
        self.largeurPSelect = 0
        self.largeurRing = int(self.largeur/2)
        self.placePoints(points)

    def dessine(self, x: int, y: int, longueurMax: int) -> None:
        """Permet de dessiner la jauge à l'écran.

        Args:
            x (int): La position des abcisses du point en haut à gauche de la jauge.
            y (int): La position des ordonnées du point en haut à gauche de la jauge.
            longueur (int): La longueur voulue pour la barre.
        """
        h = int(self.hauteur/2)
        self.setPosAndTaille([x, y], int(longueurMax*self.prop))
        draw_rectangle_rounded([self.origine[0], self.origine[1], self.longueur, self.hauteur], 1, 30, 
                               GRAY)
        couleur = (self.couleurCurseur[2][0]*5, self.couleurCurseur[2][1]*5, self.couleurCurseur[2][2]*5, 255)
        for i in range(len(self.points)):
            point = self.points[i]
            if self.valeur == point[1] and not self.defil:
                rayon = self.largeurPSelect
                if self.largeurRing > 0 and trouveParam("anims") >= 2:
                    draw_ring((self.origine[0]+point[2], int(self.origine[1]+self.hauteur/2)), 
                                int(self.largeurPSelect*1.8+self.largeur/2-self.largeurRing), 
                                int(self.largeurPSelect*1.8+self.largeur/2), 0, 360, 100, WHITE)
                    if self.largeurPSelect == self.lMaxPSelect:
                        self.changeTailleRing()
            else:
                rayon = int(self.largeur*0.6)
            if self.posCurseur >= point[2] and (self.valeur != point[1] or self.defil):
                colPt = BLUE
                couleurTexte = GRAY
                if point[0].police != police2:
                    point[0].setPolice(police2)
            elif self.valeur == point[1] and not self.defil:
                colPt = [255, 255, 255, self.transparenceCurseur[2]]
                couleurTexte = WHITE
                if point[0].police != police1i:
                    point[0].setPolice(police1i)
            else:
                colPt = GRAY
                couleurTexte = GRAY
                if point[0].police != police2:
                    point[0].setPolice(police2)
            draw_circle(self.origine[0]+point[2], int(self.origine[1]+self.hauteur/2), rayon, colPt)
            point[0].dessine([[self.origine[0]+point[2], int(self.origine[1]-self.lMaxPSelect*1.5)], 'c'], 
                             couleurTexte)
        draw_rectangle_rounded([self.origine[0], self.origine[1], self.posCurseur, self.hauteur], 1, 30, 
                                BLUE)
        draw_circle(int(self.origine[0]+self.posCurseur), self.origine[1]+h, self.largeur, couleur)
        self.changePosCurseur()
        self.changeCouleurCurseur()
        if trouveParam("anims") >= 1:
            self.changeTaillePoint()
            if self.largeurPSelect == self.lMaxPSelect:
                self.changeNiveauSurbrillance()

    def setPosAndTaille(self, coords: list, longueur: int) -> None:
        if coords != self.origine:
            if self.points[0][0].getDims()[0]/2 > self.lMaxPSelect/2:
                x = int(coords[0]+self.points[0][0].getDims()[0]/2-self.lMaxPSelect/2)
            else:
                x = int(coords[0]+self.lMaxPSelect*0.65)
            self.origine = [x, int(coords[1]+self.lMaxPSelect*1.5)]
        if longueur != self.longueur:
            self.longueur = longueur
            self.posMax = self.longueur-self.hauteur
            self.placePoints(self.ptOriginaux)

    def changeNiveauSurbrillance(self) -> None:
        """Animation qui change l'opacité du cercle de surbrillance du point sélectionné.
        """
        if self.transparenceCurseur[3]:
            if self.transparenceCurseur[2] < self.transparenceCurseur[1]:
                self.transparenceCurseur[2] += 1
            else:
                self.transparenceCurseur[3] = False
        else:
            if self.transparenceCurseur[2] > self.transparenceCurseur[0]:
                self.transparenceCurseur[2] -= 1
            else:
                self.transparenceCurseur[3] = True

    def changeTaillePoint(self) -> None:
        """Change la taille du cercle de surbrillance du point sélectionné.
        """
        if self.defil and self.largeurPSelect > 0:
            self.largeurPSelect = 0
            self.largeurRing = int(self.largeur/2)
            self.transparenceCurseur[2] = self.transparenceCurseur[1]
        else:
            if self.largeurPSelect < self.lMaxPSelect:
                self.largeurPSelect += 1

    def changeTailleRing(self) -> None:
        """Change la taille de l'anneau.
        """
        if self.largeurRing > 0:
            self.largeurRing -= 1

    def changeCouleurCurseur(self) -> None:
        """Change la couleur du curseur selon si l'utilisateur l'utilise ou non.
        """
        if self.defil or self.getContactCurseur() or self.getContact():
            if self.couleurCurseur[2] != self.couleurCurseur[1]:
                couleur = self.couleurCurseur[2]
                cible = self.couleurCurseur[1]
                for i in range(len(couleur)):
                    if couleur[i] < cible[i]:
                        couleur[i] += 1
        else:
            if self.couleurCurseur[2] != self.couleurCurseur[0]:
                couleur = self.couleurCurseur[2]
                cible = self.couleurCurseur[0]
                for i in range(len(couleur)):
                    if couleur[i] > cible[i]:
                        couleur[i] -= 1

    def placePoints(self, points: list) -> None:
        """Définit la position des points sur la jauge.

        Args:
            points (list): Listes des points à placer.
        """
        if len(points) >= 2:
            self.points = []
            nbPtCentre = len(points)-2
            divisions = nbPtCentre + 1
            l = int(self.longueur/divisions)
            self.points.append([BlocTexte(points[0], police1i, 20), 0, self.posMin])
            for i in range(nbPtCentre):
                self.points.append([BlocTexte(points[i+1], police2, 20), i+1, l*(i+1)])
            self.points.append([BlocTexte(points[len(points)-1], police2, 20), len(points)-1, self.posMax])
            self.valeur = self.points[0][1]
            self.lu = False
        else:
            self.erreurs.append([BlocTexte(e100[0], police1, int(yf*0.035*1.2)), 
                BlocTexte("Une \"PosiJauge\" doit posseder au moins 2 points.", police2, int(yf*0.035))])

    def changePosCurseur(self) -> None:
        """Permet de déplacer le curseur sur la jauge.
        """
        if not self.defil:
            if self.getContactCurseur():
                if is_mouse_button_down(0):
                    self.defil = True
        else:
            self.AttribuerPosition()
            if is_mouse_button_up(0):
                self.aimantsPoints()
                self.defil = False
        if not self.defil and self.getContact():
            if is_mouse_button_pressed(0):
                self.AttribuerPosition()
                self.aimantsPoints()

    def AttribuerPosition(self) -> None:
        """Permet de modifier la position du curseur.
        """
        x = get_mouse_x()
        position = int(x-self.origine[0])
        if position < self.posMin:
            position = self.posMin
        elif position > self.posMax:
            position = self.posMax
        self.posCurseur = position

    def aimantsPoints(self) -> None:
        """Permet de modifier la position du curseur vers le point le plus proche.
        """
        min = 0
        max = 1
        localise = False
        i = 0
        while i < len(self.points)-1 and not localise:
            point = self.points[i]
            if point[2] <= self.posCurseur:
                min = i
                max = i+1
            else:
                localise = True
            i = i + 1
        l = self.points[max][2] - self.points[min][2]
        p = (self.posCurseur-self.points[min][2])/l
        if p <= 0.5:
            self.posCurseur = self.points[min][2]
            self.valeur = self.points[min][1]
        else:
            self.posCurseur = self.points[max][2]
            self.valeur = self.points[max][1]
        self.lu = False

    def getContactCurseur(self) -> bool:
        """Vérifie si le pointeur de la souris est sur le curseur.

        Returns:
            bool: True si le pointeur est sur le curseur.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= self.origine[1]-self.hauteur/2 and y <= self.origine[1]+self.hauteur*2:
            if x >= self.origine[0]+self.posCurseur-self.hauteur and x <= self.origine[0]+self.posCurseur+self.hauteur:
                rep = True
        return rep

    def getContact(self) -> bool:
        """Vérifie si le pointeur de la souris est sur la jauge.

        Returns:
            bool: True si le pointeur est sur la jauge.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= self.origine[1] and y <= self.origine[1]+self.hauteur:
            if x >= self.origine[0] and x <= self.origine[0]+self.longueur:
                rep = True
        return rep

    def getDims(self) -> list:
        """Renvoie les dimensions de la jauge.

        Returns:
            list: [longueur de la jauge, hauteur de la jauge]
        """
        l = int(self.longueur+self.points[0][0].getDims()[0]/2+self.points[len(self.points)-1][0].getDims()[0]/2)
        h = int(self.lMaxPSelect+self.points[0][0].getDims()[1])
        return [l, h]

    def getLu(self) -> bool:
        """Dit si l'état de la jauge a était lu ou non.

        Returns:
            bool: True si l'état a était lu.
        """
        return self.lu

    def getValeur(self) -> int:
        """Retourne la valeur du point actuellment sélectionné.

        Returns:
            int: Valeur comprise entre 0 et nombre de points -1.
        """
        return self.valeur

    def marqueCommeLu(self) -> None:
        """Permet de dire que la valeur de la jauge a était lue.
        """
        self.lu = True

    def setPosCurseur(self, valeur: int) -> None:
        """Permet de modifier la position du curseur selon la valeur qui doit être sélectionné.

        Args:
            valeur (int): La valeur voulue.
        """
        self.valeur = valeur
        self.posCurseur = self.points[valeur][2]