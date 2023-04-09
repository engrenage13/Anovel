from systeme.FondMarin import *
from jeux.Jeu_1.fonctions.jeu import TAILLECASE

class Element:
    def __init__(self, image: str, x: int = 0, y: int = 0) -> None:
        self.pos = (x, y)
        # Images
        originale = load_image(image)
        image_resize(originale, int(originale.width*TAILLECASE/originale.width), 
                     int(originale.height*TAILLECASE/originale.width))
        self.originale = originale
        self.image = load_texture_from_image(self.originale)
        unload_image(originale)
        # /Images
        self.dimensions = (self.image.width, self.image.height)
        self.coords = [int(x-self.dimensions[0]/2), int(y-self.dimensions[1]/2), 
                       self.image.width, self.image.height]

    def dessin(self) -> None:
        x = self.pos[0]
        y = self.pos[1]
        l = self.dimensions[0]
        h = self.dimensions[1]
        draw_texture(self.image, int(x-l/2), int(y-h/2), WHITE)

    def getContact(self) -> bool:
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[0]+self.coords[2]:
            if y >= self.coords[1] and y <= self.coords[1]+self.coords[3]:
                rep = True
        return rep