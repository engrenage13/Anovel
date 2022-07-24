from systeme.FondMarin import *
from ui.clickIma import ClickIma
from interpreteur.article import Article
from interpreteur.categorie import Categorie

class Fenetre:
    def __init__(self, fichier: str) -> None:
        self.ouvert = False
        self.titre = None
        self.contenu = []
        self.dims = [int(xf*0.6), yf]
        # Fichier
        self.fichier = fichier
        self.decode = False
        self.position = 'fen'
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
            l = self.dims[0]
            h = self.dims[1]
            croix = [self.croix.images[0].width, self.croix.images[0].height]
            decalage = int(yf*0.001)
            draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
            draw_rectangle(xf-l, 0, l, h, [30, 30, 30, 255])
            self.dessine2()
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
    
    def dessine2(self) -> None:
        if not self.decode:
            self.decodeur()
        if len(self.contenu) > 0:
            self.dessineContenu()
        self.dessineTitre()

    def dessineTitre(self) -> None:
        ttit = int(yf*0.04)
        h = int(self.dims[1]*0.09)
        if self.titre != None:
            h = int(self.dims[1]*0.2)
        draw_rectangle(xf-self.dims[0], 0, self.dims[0], h, [0, 43, 54, 255])
        if self.titre != None:
            ttt = measure_text_ex(police1, self.titre, ttit, 0)
            draw_text_ex(police1, self.titre, [xf-int(xf*0.015)-ttt.x, int(yf*0.06)], ttit, 0, WHITE)

    def dessineContenu(self) -> None:
        y = int(self.dims[1]*0.1)
        if self.titre != None:
            y = int(self.dims[1]*0.22)
        contenu = self.contenu[len(self.contenu)-1]
        if type(contenu) == str:
            draw_text_ex(police2, self.contenu[len(self.contenu)-1], [xf-int(self.dims[0]*0.99), y], 
                         30, 0, WHITE)

    def decodeur(self) -> None:
        if file_exists(self.fichier):
            fic = load_file_text(self.fichier)
            fil = fic.split("\n")
            print(fil)
            while len(fil) > 0:
                #print(fil[0])
                if self.position == 'fen':
                    if len(fil[0]) > 0 and fil[0][0] == "#":
                        ligne = fil[0].split(" ")
                        del ligne[0]
                        self.titre = " ".join(ligne)
                    elif fil[0] == "_art//":
                        self.contenu.append(Article())
                        self.position = 'art'
                    elif fil[0] == "_cat//":
                        self.contenu.append(Categorie())
                        self.position = 'cat'
                elif self.position == 'art' or self.position == 'cat':
                    rep = self.contenu[len(self.contenu)-1].decodeur(fil[0])
                    if rep:
                        self.position = 'fen'
                del fil[0]
            self.decode = True

    def ouvre(self) -> None:
        self.ouvert = True

    def ferme(self) -> None:
        self.ouvert = False