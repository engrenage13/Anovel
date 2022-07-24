from systeme.FondMarin import *
from ui.clickIma import ClickIma

class Fenetre:
    def __init__(self, titre: str) -> None:
        self.titre = titre
        self.ouvert = False
        # Croix
        facteur = int(yf*0.05)
        cruzoff = load_image('images/ui/CroSom.png')
        image_resize(cruzoff, facteur, facteur)
        croixSombre = load_texture_from_image(cruzoff)
        unload_image(cruzoff)
        cruzon = load_image('images/ui/CroLum.png')
        image_resize(cruzon, facteur, facteur)
        croixLumineuse = load_texture_from_image(cruzon)
        unload_image(cruzon)
        self.croix = ClickIma([self.ferme], [croixSombre, croixLumineuse])

    def dessine(self) -> None:
        if self.ouvert:
            l = int(xf*0.6)
            h = yf
            croix = [self.croix.images[0].width, self.croix.images[0].height]
            decalage = int(yf*0.001)
            draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
            draw_rectangle(xf-l, 0, l, h, [0, 43, 54, 255])
            ttt = measure_text_ex(police1, self.titre, 30, 0)
            draw_text_ex(police1, self.titre, [xf-int(xf*0.03)-ttt.x, int(yf*0.06)], 30, 0, WHITE)
            draw_rectangle(xf-l, int(yf*0.05-croix[1]*0.55-decalage*3), croix[0]+decalage*3, 
                           int(croix[1]*1.1+decalage*6), RED)
            draw_triangle((xf-l+croix[0]+decalage*3, int(yf*0.05-croix[1]*0.55-decalage*3)), 
                          (xf-l+croix[0]+decalage*3, int(yf*0.05+croix[1]*0.55+decalage*3)), 
                          (xf-l+int(croix[0]*1.5+decalage*6), int(yf*0.05-croix[1]*0.55-decalage*3)), RED)
            draw_rectangle(xf-l, int(yf*0.05-croix[1]*0.55-decalage), croix[0]+decalage, 
                           int(croix[1]*1.1+decalage*2), WHITE)
            draw_triangle((xf-l+croix[0]+decalage, int(yf*0.05-croix[1]*0.55-decalage)), 
                          (xf-l+croix[0]+decalage, int(yf*0.05+croix[1]*0.55+decalage)), 
                          (xf-l+int(croix[0]*1.5+decalage*2), int(yf*0.05-croix[1]*0.55-decalage)), WHITE)
            draw_rectangle(xf-l, int(yf*0.05-croix[1]*0.55), croix[0], int(croix[1]*1.1), RED)
            draw_triangle((xf-l+croix[0], int(yf*0.05-croix[1]*0.55)), 
                          (xf-l+croix[0], int(yf*0.05+croix[1]*0.55)), 
                          (xf-l+int(croix[0]*1.5), int(yf*0.05-croix[1]*0.55)), RED)
            self.croix.dessine((xf-int(l*0.995), int(yf*0.05-croix[1]/2)))

    def ouvre(self) -> None:
        self.ouvert = True

    def ferme(self) -> None:
        self.ouvert = False