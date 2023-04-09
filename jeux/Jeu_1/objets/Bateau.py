from systeme.FondMarin import *

class Bateau:
    def __init__(self, image: str):
        """Crée un bateau.

        Args:
            image (str): Chemin d'accès à l'image du bateau.
            proprietaire (Joueur): Propriétaire du bateau.
        """
        self.rejouer()
        # Images
        originale = load_image(image)
        image_resize(originale, int(originale.width*(yf*0.1)/originale.width), 
                     int(originale.height*(yf*0.1)/originale.width))
        self.originale = originale
        self.image = load_texture_from_image(self.originale)
        # /Images
        self.coords = [0, 0, self.image.width, self.image.height]
        # Cercles
        RC = int(xf*0.06)
        self.RCD = RC*2
        self.RCA = RC*3

    def dessine(self) -> None:
        """Dessine le bateau.
        """
        x = int((self.coords[2]-self.coords[0])/2+self.coords[0])
        y = int((self.coords[3]-self.coords[1])/2+self.coords[1])
        if self.actif:
            draw_circle_lines(int(x-self.image.width*0.04), y, self.RCA, ORANGE)
            draw_circle_lines(int(x-self.image.width*0.04), y, self.RCD, LIME)
        draw_texture(self.image, int(x-self.image.width/2), int(y-self.image.height/2), WHITE)
        if int((self.coords[2]-self.coords[0])/2+self.coords[0]) != self.pos[0] or int((self.coords[3]-self.coords[1])/2+self.coords[1]) != self.pos[1]:
            self.deplace()
    
    def tourne(self) -> None:
        image_rotate_cw(self.originale)
        self.image = load_texture_from_image(self.originale)

    def setPos(self, x: int, y: int) -> None:
        self.pos = [x, y]

    def deplace(self) -> None:
        if self.place:
            max = 4
            x = (self.coords[2]-self.coords[0])/2+self.coords[0]
            y = (self.coords[3]-self.coords[1])/2+self.coords[1]
            if x < self.pos[0]:
                a = (self.pos[0]-x)%max
                if a == 0:
                    a = max
                self.coords[0] += a
                self.coords[2] += a
            elif x > self.pos[0]:
                a = (x-self.pos[0])%max
                if a == 0:
                    a = max
                self.coords[0] -= a
                self.coords[2] -= a
            if y < self.pos[1]:
                a = (self.pos[1]-y)%max
                if a == 0:
                    a = max
                self.coords[1] += a
                self.coords[3] += a
            elif y > self.pos[1]:
                a = (y-self.pos[1])%max
                if a == 0:
                    a = max
                self.coords[1] -= a
                self.coords[3] -= a
        else:
            self.coords[0] = int(self.pos[0]-self.image.width/2)
            self.coords[1] = int(self.pos[1]-self.image.height/2)
            self.coords[2] = int(self.pos[0]+self.image.width/2)
            self.coords[3] = int(self.pos[1]+self.image.height/2)
            self.place = True

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du bateau pour rejouer une nouvelle partie.
        """
        self.pos = []
        self.place = False
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