from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from museeNoyee import vapeurD, vapeurG

class Notification:
    def __init__(self, texte: str, position: str, couleur: list) -> None:
        """Crée une notification.

        Args:
            texte (str): Déscription de la notif.
            position (str): Côté où doit apparaître la notification.
            couleur (list): Couleur d'accentuation de la notif.
        """
        self.lmax = int(xf*0.3)
        self.lmin = int(tlatba*0.4)
        self.largeurAdditionnelle = int(self.lmax*0.1)
        self.hauteur = int(yf*0.09)
        tt = measure_text_ex(police2, texte, self.hauteur*0.33, 0)
        if tt.x >= int(self.lmax*0.95):
            self.texte = BlocTexte(texte[:].upper(), police2, int(self.hauteur*0.33), [int(self.lmax), ''])
        else:
            self.texte = BlocTexte(texte[:].upper(), police2, int(self.hauteur*0.33))
        self.largeur = int(self.texte.getDims()[0]+self.lmax*0.05)
        if self.largeur < self.lmin:
            self.largeur = self.lmin+int(self.lmax*0.05)
        self.mode = True
        self.fini = False
        self.horloge = 0
        self.couleur = [[30, 30, 30, 200], couleur, list(WHITE)]
        self.pas = 16
        # Position
        droite = ['d', 'droite', '->', '>']
        gauche = ['g', 'gauche', '<-', '<']
        self.cote = 1
        if type(position) == str:
            cote = position.lower()
            if cote in droite:
                self.cote = 1
            elif cote in gauche:
                self.cote = 0
        # Apparence
        if self.cote == 0:
            self.deco = vapeurG
        else:
            self.deco = vapeurD
        self.setVariable()

    def setVariable(self) -> None:
        """Redéfinit certaines variables utiles à la création de la notification.
        """
        if self.cote == 0:
            self.x = -self.largeur
            self.xDeco = self.x-self.pas
            self.xT = self.x+int(self.largeur*0.01)
            self.max = 0
        else:
            self.x = xf
            self.xDeco = int(self.x+self.largeur-self.deco.width+self.pas)
            self.xT = self.x+int(self.largeur*0.99-self.texte.getDims()[0])
            self.max = xf-self.largeur

    def dessine(self, y: int) -> None:
        """Dessine la notification à l'écran.

        Args:
            y (int): Position y de l'origine de la notif.
        """
        tt = self.texte.getDims()
        if tt[1] > self.hauteur:
            self.hauteur = int(tt[1]+yf*0.02)
        decalage = 0
        if self.cote == 0:
            decalage = self.largeurAdditionnelle
        draw_rectangle_rounded((self.x-decalage, y, self.largeur+self.largeurAdditionnelle, self.hauteur), 
                               0.15, 30, self.couleur[0])
        draw_texture(self.deco, self.xDeco, int(y+self.hauteur-self.deco.height), self.couleur[1])
        self.texte.dessine([[self.xT, y+int(self.hauteur/2-tt[1]/2)], 'no'], self.couleur[2], 'd')
        self.deplace()

    def deplace(self):
        """Gère l'animation relative aux notification.
        """
        if self.mode and self.horloge == 0:
            if self.x < self.max and self.cote == 0:
                self.x = self.x + self.pas
                self.xT = self.xT + self.pas
                self.xDeco = self.xDeco + self.pas
            elif self.x > self.max and self.cote == 1:
                self.x = self.x - self.pas
                self.xT = self.xT - self.pas
                self.xDeco = self.xDeco - self.pas
            else:
                self.mode = False
                self.horloge = self.horloge + 1
        elif self.horloge > 0:
            if self.horloge < 80:
                self.horloge = self.horloge + 1
            else:
                self.horloge = 0
        else:
            if not self.invisible():
                self.fondu()
            else:
                self.fin()

    def fin(self) -> None:
        """Définit ce qu'il se passe à la fin de l'animation.
        """
        self.mode = True
        self.fini = True
        self.setVariable()

    def fondu(self) -> None:
        """Rend les notification invisible.
        """
        for i in range(len(self.couleur)):
            if self.couleur[i][3] > 0:
                pas = 3
                if self.couleur[i][3] - pas < 0:
                    pas = self.couleur[i][3]
                self.couleur[i][3] -= pas

    def invisible(self) -> bool:
        """Vérifie si la notification est invisible.

        Returns:
            bool: True si la notif est invisible.
        """
        rep = True
        for i in range(len(self.couleur)):
            if self.couleur[i][3] > 0:
                rep = False
        return rep

    def getDisparition(self) -> bool:
        """Vérifie si l'animation est terminé.

        Returns:
            bool: True si l'animation est terminé.
        """
        rep = False
        if self.fini:
            rep = True
        return rep