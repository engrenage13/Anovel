from systeme.FondMarin import *
from ui.clickIma import ClickIma
from interpreteur.article import Article
from ui.blocTexte import BlocTexte

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
        self.types = ['cad', 'ast', 'imp']
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
        if not self.evaluation:
            self.mesureTaille()
        l = self.largeur
        h = self.hauteur
        x = int(xf/2-l/2)
        y = int(yf/2-h/2)
        ph = y + self.hauteurTitre + self.espace
        draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
        draw_rectangle(x, y+4, l, h, [20, 20, 20, 255])
        draw_rectangle(x, y, l, h, [30, 30, 30, 255])
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                self.contenu[i].dessine(int(x+l*0.025), ph)
                ph = int(ph + self.contenu[i].getDims()[1] + self.espace)
            else:
                typ = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                pt = [int(x+l*0.025), ph]
                if typ in self.types:
                    couleur = [20, 20, 20, 165]
                    if typ == 'ast':
                        couleur = [82, 73, 245, 165]
                    elif typ == 'imp':
                        couleur = [244, 80, 77, 165]
                    draw_rectangle(int(x+l*0.025), ph, int(l*0.95), int(tt[1]+self.espace), couleur)
                    pt = [int(x+l*0.05), int(ph+self.espace/2)]
                alig = 'g'
                if typ in self.types and contenu.getNbLignes() == 1:
                    alig = 'c'
                contenu.dessine([pt, 'no'], alignement=alig)
                nbEspace = 1
                if typ in self.types:
                    nbEspace = 2
                ph = int(ph + tt[1] + self.espace*nbEspace)
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

    def decodeur(self, ligne: str) -> list:
        rep = False
        if len(ligne) > 0 and ligne[0] == "#":
            li = ligne.split(" ")
            del li[0]
            self.setTitre(" ".join(li))
        elif ligne == "//fen_":
            rep = True
        return rep

    def mesureTaille(self) -> None:
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                dims = self.contenu[i].getDims()
                self.hauteur += int(dims[1] + self.espace)
            elif type(self.contenu[i]) == list:
                nbEspace = 1
                if self.contenu[i][0] in self.types:
                    nbEspace = 2
                dims = self.contenu[i][1].getDims()
                self.hauteur += int(dims[1] + self.espace*nbEspace)
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