from systeme.FondMarin import *
from ui.blocTexte import BlocTexte

class Interrupteur:
    def __init__(self, titre: int) -> None:
        """Permet de créer un interrupteur (bouton switch).

        Args:
            titre (int): Déscription de l'action contrôlée par l'interrupteur.
        """
        self.origine = None
        self.largeur = int(xf*0.04)
        self.hauteur = int(yf*0.04)
        self.marge = int(yf*0.006)
        self.etat = 0
        self.lu = True
        self.erreurs = []
        # Curseur
        diametre = int(self.hauteur-self.marge*2)
        self.posMin = int(diametre/2)
        self.pos = int(diametre/2)
        self.posMax = int(self.largeur-diametre/2-self.marge*2)
        # Texte
        self.texte = BlocTexte(titre.upper(), police2, int(yf*0.035), [int(xf*0.5), ''])

    def dessine(self, x: int, y: int) -> None:
        """Dessine l'interrupteur à l'écran.

        Args:
            x (int): Position x du coin supérieur gauche du cadre.
            y (int): Position y du coin supérieur gauche du cadre.
        """
        diametre = int(self.hauteur-self.marge*2)
        if self.etat:
            couleur = DARKBLUE
            couleur2 = WHITE
        else:
            couleur = GRAY
            couleur2 = LIGHTGRAY
        h = self.hauteur
        if self.texte.getDims()[1] > h:
            h = self.texte.getDims()[1]
        if self.texte.texte not in ("", " "):
            draw_rectangle_rounded([x, y, int(self.texte.getDims()[0]+self.largeur+xf*0.03), int(h+yf*0.02)], 
                                    0.2, 30, [80, 80, 80, 170])
            x = x + int(xf*0.01)
            y = y + int(yf*0.01)
            self.texte.dessine([[x, y], 'no'], alignement='g')
            x = x + self.texte.getDims()[0] + int(xf*0.01)
        draw_rectangle_rounded((x, y, self.largeur, self.hauteur), 1, 60, couleur)
        draw_circle(int(x+self.marge+self.pos), int(y+self.marge+diametre/2), diametre/2, couleur2)
        if self.origine != [x, y]:
            self.origine = [x, y]
        if self.getContact() and is_mouse_button_pressed(0):
            self.switch()
        self.bougeCurseur()

    def switch(self) -> None:
        """Change l'état de l'interrupteur.
        """
        if not self.etat:
            self.etat = 1
        else:
            self.etat = 0
        self.lu = False

    def bougeCurseur(self) -> None:
        """Déplace le curseur en fonction de l'état de l'interrupteur.
        """
        pas = int((self.posMax-self.posMin)/10)
        if not self.etat and self.pos != self.posMin:
            self.pos -= pas
        elif self.etat and self.pos != self.posMax:
            self.pos += pas

    def getContact(self) -> bool:
        """Vérifie si le pointeur de la souris est sur la jauge.

        Returns:
            bool: True si le pointeur est sur la jauge.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= self.origine[1] and y <= self.origine[1]+self.hauteur:
            if x >= self.origine[0] and x <= self.origine[0]+self.largeur:
                rep = True
        return rep

    def getDims(self) -> tuple:
        """Renvoie les dimensions du cadre.

        Returns:
            tuple: 1. longueur. 2. hauteur.
        """
        h = self.hauteur
        if self.texte.getDims()[1] > h:
            h = self.texte.getDims()[1]
        l = self.texte.getDims()[0]+self.largeur+int(xf*0.01)
        if self.texte.texte not in ("", " "):
            l += int(xf*0.02)
            h += int(yf*0.02)
        return (l, h)

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
        return self.etat

    def marqueCommeLu(self) -> None:
        """Permet de dire que la valeur de la jauge a était lue.
        """
        self.lu = True