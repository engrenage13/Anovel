from systeme.FondMarin import *

class Notification:
    def __init__(self, titre: str, texte: str) -> None:
        """Crée une notification.

        Args:
            titre (str): Le titre de la notif.
            texte (str): Déscription de la notif.
        """
        self.titre = titre[:]
        self.texte = texte[:]
        self.mode = True
        self.fini = False
        self.horloge = 0
        self.couleur = [list(DARKGRAY), list(BLUE), list(WHITE)]
        self.longueur = int(xf*0.3)
        self.hauteur = int(yf*0.13)
        self.pas = 4
        self.pos = 0
        self.setVariable()

    def setVariable(self) -> None:
        """Redéfinit certaines variables utiles à la création de la notification.
        """
        if self.pos == 0:
            self.x = int(xf/2)-int(self.longueur/2)
            self.y = yf
            self.max = [self.x, int(yf*0.75)]
        elif self.pos == 1:
            self.x = -self.longueur
            self.y = int(yf-self.hauteur*1.06)
            self.max = [int(xf*0.02), int(yf*0.82)]
        else:
            self.x = xf
            self.y = int(yf-self.hauteur*1.06)
            self.max = [xf-int(xf*0.02)-self.longueur, int(yf*0.82)]

    def dessine(self) -> None:
        """Dessine la notification à l'écran.
        """
        tt1 = measure_text_ex(police2, self.titre, 35, 0)
        tt2 = measure_text_ex(police2, self.texte, 22, 2)
        orixt = self.x + int(self.longueur/2)
        draw_rectangle_rounded((self.x, self.y, self.longueur, self.hauteur), 0.2, 30, self.couleur[0])
        draw_text_pro(police2, self.titre, (orixt-int(tt1.x/2), self.y+int(tt1.y*0.2)), (0, 0), 0, 35, 0, 
                      self.couleur[1])
        draw_text_pro(police2, self.texte, (orixt-int(tt2.x/2), self.y+int(tt1.y*1.7)), (0, 0), 0, 22, 0, 
                      self.couleur[2])
        self.deplace()

    def deplace(self):
        """Gère l'animation relative aux notification.
        """
        if self.mode and self.horloge == 0:
            self.fini = False
            if self.x < self.max[0] and self.pos == 1:
                self.x = self.x + self.pas*4
            elif self.x > self.max[0] and self.pos == 2:
                self.x = self.x - self.pas*4
            elif self.y > self.max[1]:
                self.y = self.y - self.pas
            else:
                self.mode = False
                self.horloge = self.horloge + 1
        elif self.horloge > 0:
            if self.horloge < 80:
                self.horloge = self.horloge + 1
                if self.pos > 0:
                    self.y = self.y - self.horloge%2
                    self.max[1] = self.y
            else:
                self.horloge = 0
        else:
            if self.pos == 0:
                if self.y < yf:
                    self.y = self.y + self.pas
                else:
                    self.fin()
            elif not self.invisible():
                self.fondu()
            else:
                self.fin()

    def fin(self) -> None:
        """Définit ce qu'il se passe à la fin de l'animation.
        """
        self.mode = True
        self.fini = True
        self.setVariable()
        self.modifCouleur([list(DARKGRAY), list(BLUE), list(WHITE)])

    def fondu(self) -> None:
        """Rend les notification invisible.
        """
        for i in range(len(self.couleur)):
            if self.couleur[i][3] > 0:
                pas = 3
                if self.couleur[i][3] - pas < 0:
                    pas = self.couleur[i][3]
                self.couleur[i][3] -= pas
        self.y = self.y - self.couleur[0][3]%2
        self.max[1] = self.y

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

    def modifTitre(self, titre: str) -> None:
        """Permet de modifier le titre de la notification.

        Args:
            titre (str): Nouveau titre.
        """
        self.titre = titre

    def modifTexte(self, texte: str) -> None:
        """Permet de modifier le message de la notification.

        Args:
            texte (str): Nouveau message.
        """
        self.texte = texte

    def modifCouleur(self, couleur: list) -> None:
        """Permet de modifier les couelurs de la notif.

        Args:
            couleur (list): 1. Fond de la notif. 2. Couleur du titre. 3. Couleur du texte.
        """
        self.couleur = couleur

    def setPosition(self, position: int) -> None:
        """Permet de déinir la position souhaité pour la notification.

        Args:
            position (int): 0 : Milieu. 1 : Gauche. 2 : Droite.
        """
        self.pos = position
        self.setVariable()

    def getDisparition(self) -> bool:
        """Vérifie si l'animation est terminé.

        Returns:
            bool: True si l'animation est terminé.
        """
        rep = False
        if self.fini:
            rep = True
        return rep