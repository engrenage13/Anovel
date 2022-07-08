from systeme.FondMarin import *
from objets.Bateau import Bateau

class BateauJoueur(Bateau):
    def __init__(self, nom: str, taille: int, image: str, proprietaire: object):
        """Crée un bateau lié à un joueur.

        Args:
            nom (str): Le nom du bateau.
            taille (int): Le nombre de cases qu'occupe le bateau sur le plateau.
            image (Ima): Apparence du bateau.
            propriétaire (Joueur): Propriétaire du bateau.
        """
        super().__init__(nom, taille, image, proprietaire)
        self.coord = [0, 0, 1, 1]

    def dessine(self, x: int, y: int):
        """Dessine le bateau.

        Args:
            x (int): Coordonné des absicesses de l'origine de l'image.
            y (int): Coordonné des ordonnées de l'origine de l'image.
        """
        if self.orient == 'h':
            if self.direction == 1:
                self.direction = 2
            elif self.direction == 3:
                self.direction = 0
        else:
            if self.direction == 0:
                self.direction = 1
            elif self.direction == 2:
                self.direction = 3
        image = self.images[self.direction]
        self.coord = [x, y, image.width, image.height]
        draw_texture(image, x, y, WHITE)

    def getContact(self) -> bool:
        """Vérifie si le curseur est sur le bateau.

        Returns:
            bool: True si le curseur est sur le bateau, False dans le cas contraire.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coord[0] and x <= self.coord[0]+self.coord[2]:
            if y >= self.coord[1] and y <= self.coord[1]+self.coord[3]:
                rep = True
        return rep

    def switchMode(self) -> bool:
        """Sélectionne et déselectionne le bateau.

        Returns:
            bool: True si le bateau entre en phase de placement, False s'il est relâché.
        """
        if self.defil:
            self.immobile()
            rep = False
        else:
            self.declenMouv()
            rep = True
        return rep

    def immobile(self):
        """Désélectionne le bateau.
        """
        self.defil = False
        if not self.pos or False in self.pos:
            self.pos = False
            self.orient = 'h'
            if self.direction != 0:
                self.direction = 0

    def declenMouv(self):
        """Sélectionne le bateau.
        """
        self.defil = True

    def setPosition(self, coord: list, zone: int) -> None:
        """Modifie la position du bateau sur le plateau.

        Args:
            coord (list): Liste des cases ciblé.
            zone (int): Zone de l'écran où se trouve le bateau.
        """
        pos = []
        if zone == 1:
            for i in range(self.taille-len(coord)):
                pos.append(False)
            for i in range(len(coord)):
                pos.append(coord[len(coord)-1-i])
        elif zone == 2:
            pos = coord
        else:
            pos = coord
            for i in range(self.taille-len(coord)):
                pos.append(False)
        self.pos = pos

    def tourne(self):
        """Fait tourner le bateau.
        """
        if self.defil:
            if self.orient == 'h':
                self.orient = 'v'
            else:
                self.orient = 'h'