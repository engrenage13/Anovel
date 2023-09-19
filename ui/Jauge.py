from systeme.FondMarin import *

class PosiJauge:
    def __init__(self, longueur: int) -> None:
        """Permet de créer une jauge.

        Args:
            longueur (int): La longueur que doit mesurer la jauge à l'affichage.
        """
        self.origine = None
        self.hauteur = int(yf*0.01)
        self.longueur = longueur
        # Curseur
        self.posMin = self.hauteur
        self.posMax = self.longueur-self.hauteur
        self.posCurseur = self.posMin
        self.largeur = self.hauteur*2
        self.defil = False

    def dessine(self, x: int, y: int) -> None:
        """Permet de dessiner la jauge à l'écran.

        Args:
            x (int): La position des abcisses du point en haut à gauche de la jauge.
            y (int): La position des ordonnées du point en haut à gauche de la jauge.
        """
        h = int(self.hauteur/2)
        self.origine = [x, y]
        draw_rectangle_rounded([self.origine[0], self.origine[1], self.longueur, self.hauteur], 1, 30, 
                               GRAY)
        if self.getContactCurseur() or self.defil:
            couleur = WHITE
        else:
            couleur = BLUE
        draw_rectangle_rounded([self.origine[0], self.origine[1], self.posCurseur, self.hauteur], 1, 30, 
                                BLUE)
        draw_circle(int(self.origine[0]+self.posCurseur), self.origine[1]+h, self.largeur, couleur)
        self.changePosCurseur()

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
                self.defil = False
        if not self.defil and self.getContact():
            if is_mouse_button_pressed(0):
                self.AttribuerPosition()

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
        return [self.longueur, self.hauteur]