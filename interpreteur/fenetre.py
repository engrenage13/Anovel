from systeme.FondMarin import *
from ui.clickIma import ClickIma
from interpreteur.article import Article

class Fenetre:
    def __init__(self) -> None:
        self.ouvert = False
        self.titre = ""
        self.contenu = []
        self.largeur = int(xf*0.5)
        self.hauteurTitre = int(yf*0.08)
        self.espace = int(yf*0.03)
        self.hauteur = self.hauteurTitre + self.espace
        self.tailleTitre = int(self.hauteurTitre*0.6)
        self.evaluation = False
        # Croix
        facteur = int(self.hauteurTitre*0.8)
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
            if not self.evaluation:
                self.mesureTaille()
            l = self.largeur
            h = self.hauteur
            x = int(xf/2-l/2)
            y = int(yf/2-h/2)
            ph = y + self.hauteurTitre + self.espace
            draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
            draw_rectangle(x, y+5, l, h, [80, 80, 80, 255])
            draw_rectangle(x, y, l, h, [30, 30, 30, 255])
            for i in range(len(self.contenu)):
                self.contenu[i].dessine(int(x+l*0.025), ph)
                ph = ph + self.contenu[i].getDims()[1] + self.espace
            self.dessineTitre()

    def dessineTitre(self) -> None:
        h = self.hauteurTitre
        ht = self.hauteur
        ttit = self.tailleTitre
        croix = [self.croix.images[0].width, self.croix.images[0].height]
        draw_rectangle(int(xf/2-self.largeur/2), int(yf/2-ht/2), self.largeur, h, [0, 43, 54, 255])
        ttt = measure_text_ex(police1, self.titre, ttit, 0)
        draw_text_ex(police1, self.titre, [int(xf/2-ttt.x/2), int(yf/2-ht/2+h/2-ttt.y*0.4)], 
                     ttit, 0, WHITE)
        self.croix.dessine((int(xf/2+self.largeur/2-(croix[0]+h*0.1)), int(yf/2-ht/2+h*0.1)))

    def mesureTaille(self) -> None:
        for i in range(len(self.contenu)):
            dims = self.contenu[i].getDims()
            self.hauteur += int(dims[1] + self.espace)
        self.evaluation = True

    def ouvre(self) -> None:
        self.ouvert = True

    def ferme(self) -> None:
        self.ouvert = False

    def setTitre(self, titre: str) -> None:
        self.titre = titre
        tt = measure_text_ex(police1, self.titre, self.tailleTitre, 0)
        if int(tt.x + self.croix.images[0].width*3) > self.largeur:
            self.largeur = int(tt.x + self.croix.images[0].width*3)

    def ajouteContenu(self, contenu: Article) -> None:
        self.contenu.append(contenu)
        self.evaluation = False

    def redim(self, x: int, y: int) -> None:
        self.largeur = x
        self.hauteur = y