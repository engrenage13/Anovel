from systeme.FondMarin import *

class Bateau:
    def __init__(self, image: str):
        """Crée un bateau.

        Args:
            image (str): Chemin d'accès à l'image du bateau.
            proprietaire (Joueur): Propriétaire du bateau.
        """
        self.rejouer()
        self.portee = int(xf*0.1)
        # Images
        originale = load_image(image)
        image_resize(originale, int(originale.width*(yf*0.1)/originale.width), 
                     int(originale.height*(yf*0.1)/originale.width))
        self.originale = originale
        self.image = load_texture_from_image(self.originale)
        # /Images
        self.coords = [0, 0, self.image.width, self.image.height]

    def dessine(self) -> None:
        """Dessine le bateau.
        """
        x = self.pos[0]
        y = self.pos[1]
        if self.actif:
            draw_circle_lines(x, y, self.portee, WHITE)
        draw_texture(self.image, int(x-self.image.width/2), int(y-self.image.height/2), WHITE)
        if self.coords != [int(x-self.image.width/2), int(y-self.image.height/2), int(x+self.image.width/2), int(y+self.image.height/2)]:
            self.coords = [int(x-self.image.width/2), int(y-self.image.height/2), int(x+self.image.width/2), int(y+self.image.height/2)]
    
    def tourne(self) -> None:
        image_rotate_cw(self.originale)
        self.image = load_texture_from_image(self.originale)

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
        self.pos = []
        self.coule = False
        self.actif = False

    def getContact(self) -> bool:
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[2]:
            if y >= self.coords[1] and y <= self.coords[3]:
                rep = True
        return rep

    def __pos__(self) -> None:
        self.actif = True

    def __neg__(self) -> None:
        self.actif = False