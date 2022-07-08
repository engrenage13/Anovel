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
        self.nom = nom
        self.defil = False
        self.proprio = proprietaire
        self.rejouer()
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Images
        originale = load_image(image)
        image_resize(originale, int(originale.width*(tailleCase*0.88)*self.taille/originale.width), 
                     int(originale.height*(tailleCase*0.88)*self.taille/originale.width))
        self.images = [load_texture_from_image(originale)]
        for i in range(3):
            image_rotate_cw(originale)
            self.images.append(load_texture_from_image(originale))
        self.direction = 0
        # /Images

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
        draw_texture(self.images[self.direction], x, y, WHITE)

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
            if self.pos[i] == position:
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

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du bateau pour rejouer une nouvelle partie.
        """
        self.orient = 'h'
        self.pos = False
        self.coule = False
        self.etatSeg = ['o']*self.taille