from systeme.FondMarin import *
from ui.clickIma import ClickIma
from interpreteur.article import Article

class Fenetre:
    def __init__(self, dims: tuple, redim: bool) -> None:
        self.ouvert = False
        self.titre = ""
        self.contenu = []
        self.largeur = dims[0]
        self.hauteurTitre = int(yf*0.08)
        self.espace = int(yf*0.03)
        self.hauteur = self.hauteurTitre + self.espace
        self.redimPossible = redim
        if not self.redimPossible:
            self.hauteur = dims[1]
        self.tailleTitre = int(self.hauteurTitre*0.6)
        self.evaluation = False
        self.types = ['cad', 'ast', 'imp']
        self.fond = None
        self.imaFond = None
        # Contenu
        self.largeurContenu = int(self.largeur*0.95)
        self.pasx = int(xf*0.0125)
        self.oyc = self.hauteurTitre + self.espace
        self.hauteurContenu = self.hauteur
        self.pasy = int(yf*0.05)
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
        ph = y + self.oyc
        draw_rectangle(0, 0, xf, yf, [0, 0, 0, 210])
        draw_rectangle(x, y+4, l, h, [20, 20, 20, 255])
        draw_rectangle(x, y, l, h, [30, 30, 30, 255])
        if self.fond != None and self.imaFond == None:
            image = self.fond
            reduc = h/image.height
            image_resize(image, int(image.width*reduc), int(image.height*reduc))
            image_crop(image, [image.width-l, 0, l, h])
            self.imaFond = load_texture_from_image(image)
        if self.imaFond:
            draw_texture(self.imaFond, x, y, WHITE)
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                dims = self.contenu[i].getDims()
                self.contenu[i].dessine(x+self.pasx, ph)
                ph = int(ph + dims[1] + self.espace)
            else:
                typ = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                pt = [x+self.pasx, ph]
                if typ in self.types:
                    couleur = [20, 20, 20, 165]
                    if typ == 'ast':
                        couleur = [82, 73, 245, 165]
                    elif typ == 'imp':
                        couleur = [244, 80, 77, 165]
                    draw_rectangle(x+self.pasx, ph, self.largeurContenu, int(tt[1]+self.espace), couleur)
                    pt = [int(x+self.pasx*2), int(ph+self.espace/2)]
                alig = 'g'
                if typ in self.types and contenu.getNbLignes() == 1:
                    alig = 'c'
                contenu.dessine([pt, 'no'], alignement=alig)
                nbEspace = 1
                if typ in self.types:
                    nbEspace = 2
                ph = int(ph + tt[1] + self.espace*nbEspace)
        if self.hauteur == yf:
            self.dessineBarre()
        self.dessineTitre(l, h)
        self.bougeChariot(y)

    def dessineBarre(self) -> None:
        ymin = int(yf/2-self.hauteur/2+self.hauteurTitre+self.espace*0.8)
        l = int(self.pasx*0.4)
        ht = int(self.hauteur-ymin-self.espace)
        h = int(ht*((self.hauteur-self.hauteurTitre)/self.hauteurContenu))
        x = int(xf/2+self.largeur/2-self.pasx/2-l/2)
        ecart = int(round((self.oyc+self.hauteurContenu-self.hauteur)/self.hauteurContenu, 2)*100)
        if int(h*100/ht+ecart) > 100:
            ecart = int(100-h*100/ht)
        elif ecart < 0:
            ecart = 0
        y = int(ymin+ht-h-ht*(ecart/100))
        draw_rectangle(x, y, l, h, BLUE)

    def dessineTitre(self, largeur: int, hauteur: int) -> None:
        h = self.hauteurTitre
        l = largeur
        ht = hauteur
        ttit = self.tailleTitre
        croix = [self.croix.images[0].width, self.croix.images[0].height]
        draw_rectangle(int(xf/2-l/2), int(yf/2-ht/2), l, h, [0, 43, 54, 255])
        ttt = measure_text_ex(police1, self.titre, ttit, 0)
        draw_text_ex(police1, self.titre, [int(xf/2-ttt.x/2), int(yf/2-ht/2+h/2-ttt.y*0.4)], 
                     ttit, 0, WHITE)
        self.croix.dessine((int(xf/2+l/2-(croix[0]+h*0.1)), int(yf/2-ht/2+h*0.1)))

    def decodeur(self, ligne: str) -> list:
        rep = False
        if len(ligne) > 0 and ligne[0] == "#":
            li = ligne.split(" ")
            del li[0]
            self.setTitre(" ".join(li))
        elif len(ligne) > 0 and ligne[0] == "[" and ligne[len(ligne)-1] == "]":
            li = ""
            for i in range(len(ligne)):
                if ligne[i] not in ["[", "]"]:
                    li += ligne[i]
            if file_exists(li) and is_file_extension(li, '.png'):
                self.fond = load_image(li)
        elif ligne == "//fen_":
            rep = True
        return rep

    def bougeChariot(self, y: int) -> None:
        if self.hauteur == yf:
            roulette = int(get_mouse_wheel_move())
            roro = roulette
            if roro < 0:
                roro = roro*-1
            for i in range(roro):
                if roulette > 0:
                    if self.oyc < self.hauteurTitre + self.espace:
                        self.oyc = self.oyc + self.pasy
                elif roulette < 0:
                    if y + self.oyc + self.hauteurContenu > y + self.hauteur:
                        self.oyc = self.oyc - self.pasy

    def mesureTaille(self) -> None:
        h = 0
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                dims = self.contenu[i].getDims()
                h += int(dims[1] + self.espace)
            elif type(self.contenu[i]) == list:
                nbEspace = 1
                if self.contenu[i][0] in self.types:
                    nbEspace = 2
                dims = self.contenu[i][1].getDims()
                h += int(dims[1] + self.espace*nbEspace)
        if self.hauteur + h > yf:
            self.hauteur = yf
        else:
            self.hauteur += h
        self.hauteurContenu = h
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
        if self.redimPossible:
            if x >= xf:
                self.largeur = xf
            else:
                self.largeur = x
            if y >= yf:
                self.hauteur = yf
            else:
                self.hauteur = y