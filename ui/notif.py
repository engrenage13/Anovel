from systeme.FondMarin import *

class Notification:
    def __init__(self, texte: str, position: str, fond: list) -> None:
        """Crée une notification.

        Args:
            texte (str): Déscription de la notif.
            position (str): Côté où doit apparaître la notification.
            fond (list): Couleur du fond de la notif.
        """
        self.texte = texte[:]
        self.mode = True
        self.fini = False
        self.horloge = 0
        self.couleur = [fond, list(WHITE)]
        self.longueur = int(xf*0.3)
        self.hauteur = int(yf*0.13)
        self.pas = 16
        # Position
        droite = ['d', 'droite', '->']
        gauche = ['g', 'gauche', '<-']
        self.cote = 1
        if type(position) == str:
            cote = position.lower()
            if cote in droite:
                self.cote = 1
            elif cote in gauche:
                self.cote = 0
        self.setVariable()

    def setVariable(self) -> None:
        """Redéfinit certaines variables utiles à la création de la notification.
        """
        if self.cote == 0:
            self.x = -self.longueur
            self.max = int(xf*0.02)
        else:
            self.x = xf
            self.max = xf-int(xf*0.02)-self.longueur

    def dessine(self, y: int) -> None:
        """Dessine la notification à l'écran.

        Args:
            y (int): Position y de l'origine de la notif.
        """
        tt = measure_text_ex(police2, self.texte, 22, 0)
        orixt = self.x + int(self.longueur/2)
        draw_rectangle_rounded((self.x, y, self.longueur, self.hauteur), 0.2, 30, self.couleur[0])
        draw_text_pro(police2, self.texte, (orixt-int(tt.x/2), y+int(self.hauteur*0.5)), (0, 0), 0, 22, 0, 
                      self.couleur[1])
        self.deplace()

    def deplace(self):
        """Gère l'animation relative aux notification.
        """
        if self.mode and self.horloge == 0:
            if self.x < self.max and self.cote == 0:
                self.x = self.x + self.pas
            elif self.x > self.max and self.cote == 1:
                self.x = self.x - self.pas
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