from systeme.FondMarin import *
from ui.clickIma import ClickIma

class Fenetre:
    def __init__(self, titre: str) -> None:
        self.titre = titre
        self.ouvert = False
        # Croix
        facteur = int(yf*0.06)
        cruzoff = load_image('images/ui/CroSom.png')
        image_resize(cruzoff, facteur, facteur)
        croixSombre = load_texture_from_image(cruzoff)
        cruzon = load_image('images/ui/CroLum.png')
        image_resize(cruzon, facteur, facteur)
        croixLumineuse = load_texture_from_image(cruzon)
        self.croix = ClickIma([self.ferme], [croixSombre, croixLumineuse])

    def dessine(self) -> None:
        if self.ouvert:
            l = int(xf*0.6)
            h = yf
            draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
            draw_rectangle(xf-l, 0, l, h, [0, 43, 54, 255])
            ttt = measure_text_ex(police1, self.titre, 30, 0)
            draw_text_ex(police1, self.titre, [xf-int(xf*0.03)-ttt.x, int(yf*0.06)], 30, 0, WHITE)
            self.croix.dessine((xf-l-int(self.croix.images[0].width*0.8), int(yf*0.07-self.croix.images[0].height/2)))

    def ouvre(self) -> None:
        self.ouvert = True

    def ferme(self) -> None:
        self.ouvert = False