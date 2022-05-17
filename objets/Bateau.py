from random import choice
from systeme.FondMarin import *

class Bateau:
    def __init__(self, nom: str, taille: int, image: str, proprietaire: object):
        """Crée un bateau.

        Args:
            nom (str): Le nom du bateau.
            taille (int): Le nombre de cases qu'occupe le bateau sur le plateau.
            image (str): Chemin d'accès à l'image du bateau.
            proprietaire (Joueur): Propriétaire du bateau.
        """
        self.taille = taille
        self.orient = 'h'
        self.nom = nom
        self.pos = False
        self.defil = False
        self.proprio = proprietaire
        self.etatSeg = ['o']*taille
        self.coule = False
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Images
        originale = load_image(image)
        image_resize(originale, int(originale.width*(tailleCase*0.88)*self.taille/originale.width), 
                     int(originale.height*(tailleCase*0.88)*self.taille/originale.width))
        self.horiz = load_texture_from_image(originale)
        lirot = [1, 3]
        for i in range(choice(lirot)):
            image_rotate_cw(originale)
            self.verti = load_texture_from_image(originale)
        # /Images

    def dessine(self, x: int, y: int):
        """Dessine le bateau.

        Args:
            x (int): Coordonné des absicesses de l'origine de l'image.
            y (int): Coordonné des ordonnées de l'origine de l'image.
        """
        image = self.horiz
        if self.orient == 'v':
            image = self.verti
        draw_texture(image, x, y, WHITE)

    def estTouche(self, position: str) -> bool:
        """Dit si le bateau passé en paramètres est sur la case qui est regardée.

        Args:
            position (str): Case à vérifier.

        Returns:
            bool: True si le bateau est sur la case touché.
        """
        a = False
        i = 0
        while i < self.taille and not a:
            b = self.pos[i][0:len(self.pos[i])-2]
            if b == position:
                self.etatSeg[i] = 'x'
                a = True
            i = i + 1
        return a

    def estCoule(self) -> bool:
        """Dit si le bateau est coulé ou non.

        Returns:
            bool: True si le bateau est coulé.
        """
        a = False
        if self.coule:
            a = True
        else:
            if 'o' not in self.etatSeg:
                self.coule = True
                a = True
        return a