from systeme.FondMarin import *
from ui.bouton.taille import Taille
from ui.bouton.apparence import Apparence
from ui.blocTexte import BlocTexte

class Bouton:
    def __init__(self, taille: Taille, apparence: Apparence, texte: str, icone: str, fonctions: list) -> None:
        self.taille = taille
        self.apparence = apparence
        # Icône
        self.icone = self.generIc(icone)
        # texte
        if self.apparence.texte:
            ht = int(self.taille.hauteur*0.55)
            if self.icone:
                if self.apparence.icone == 2:
                    ht = int(self.taille.hauteur*0.4)
        else:
            ht = int(yf*0.02)
        self.texte = BlocTexte(texte.upper(), self.apparence.police, ht, ['', ''])
        # infobulle
        self.delai = 100
        self.chrono = 0
        self.spectre = 0
        # fonctions
        self.actif = False
        if type(fonctions) == list and len(fonctions) > 0:
            self.fonction = fonctions[0]
            if len(fonctions) > 1 and fonctions[1] != '':
                self.verifFonction = fonctions[1]
            else:
                self.verifFonction = self.verification
        else:
            self.fonction = None
            self.verifFonction = self.verification
        # zoom & dezoom
        self.add = 0
        self.sou = 0
        self.activate = False
        self.wave = False
        # Largeur
        self.setLargeur()

    def dessine(self, x: int, y: int) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            x (int): Abcisse du centre du bouton.
            y (int): Ordonnée du centre du bouton.
        """
        h = self.taille.hauteur
        l = self.largeur
        modifie = int(self.add)-self.sou
        self.coords = [x-int(l/2+modifie), y-int(h/2+modifie), x+int(l/2+modifie), y+int(h/2+modifie)]
        couleur = self.apparence.couleur1
        if self.apparence.zoom:
            self.zoom()
        else:
            if self.getContact():
                couleur = self.apparence.couleur2
        draw_rectangle_rounded((self.coords[0], self.coords[1], l+modifie*2, h+modifie*2), 0.15, 30, couleur)
        # Texte & Icône
        coloTex = WHITE
        if couleur[0] > 170 and couleur[1] > 170 and couleur[2] > 170:
            coloTex = BLACK
        if self.icone:
            image = self.icone
            if not self.apparence.texte:
                draw_texture(image, x-int(image.width/2), y-int(image.height/2), WHITE)
                self.dessineTexteInfoBulle()
            else:
                tt = self.texte.getDims()
                if self.apparence.icone == 1:
                    xt = x+int(image.width/2)
                    self.texte.dessine([[xt, y-int(tt[1]*0.1)], 'c'], coloTex)
                    draw_texture(image, xt-int(tt[0]/2+image.width*1.1), y-int(image.height/2), WHITE)
                elif self.apparence.icone == 3:
                    xt = x-int(image.width/2)
                    self.texte.dessine([[xt, y-int(tt[1]*0.1)], 'c'], coloTex)
                    draw_texture(image, xt+int(tt[0]/2+image.width*1.1), y-int(image.height/2), WHITE)
                elif self.apparence.icone == 2:
                    yt = y+int(image.height/2)
                    self.texte.dessine([[x, yt], 'c'], coloTex)
                    draw_texture(image, x-int(image.width/2), yt-int(tt[1]/2+image.height*1.1), WHITE)
        else:
            self.texte.dessine([[x, y-int(self.texte.getDims()[1]*0.1)], 'c'], coloTex)
        self.execute()
        if self.activate:
            self.dezoom()

    def dessineTexteInfoBulle(self) -> None:
        tt = self.texte.getDims()
        X = get_mouse_x()
        Y = get_mouse_y()
        if self.getContact():
            if self.chrono != self.delai:
                self.chrono += 1
            else:
                if self.spectre < 51:
                    self.spectre += 1
        else:
            if self.spectre > 0:
                self.spectre -= 5
                if self.spectre < 0:
                    self.spectre = 0
            if self.chrono != 0:
                self.chrono = 0
        bordure = int(yf*0.005)
        m = (self.coords[2]-self.coords[0])/2+self.coords[0]
        l = int(tt[0]+bordure*2)
        x = int(m-l/2)
        if int(self.coords[1]-yf*0.008-tt[1]*1.2) < 0:
            y = int(self.coords[3]+yf*0.008)
            draw_triangle([m, self.coords[3]-yf*0.002], [int(m-yf*0.01), y], [int(m+yf*0.01), y], [0, 0, 0, self.spectre*5])
        else:
            y = int(self.coords[1]-yf*0.008-tt[1]*1.2)
            draw_triangle([int(m-yf*0.01), y+tt[1]*1.2], [m, self.coords[1]+yf*0.002], [int(m+yf*0.01), y+tt[1]*1.2], [0, 0, 0, self.spectre*5])
        if int(x+tt[0]+bordure*2) > xf:
            x -= int(x+tt[0]+bordure*2)-xf
        draw_rectangle_rounded([x, y, l, int(tt[1]*1.2)], 0.2, 20, [0, 0, 0, self.spectre*5])
        self.texte.dessine([[int(x+bordure), int(y+tt[1]*0.01)], 'no'], [255, 255, 255, self.spectre*5])

    def zoom(self) -> None:
        max = yf*0.002
        if self.getContact():
            if self.add < max:
                self.add += yf*0.0005
        else:
            if self.add > 0:
                self.add -= yf*0.0005

    def dezoom(self) -> None:
        max = int(yf*0.003)
        if not self.wave:
            if self.sou < max:
                self.sou += int(yf*0.001)
            else:
                self.wave = True
        else:
            if self.sou > 0:
                self.sou -= int(yf*0.001)
            else:
                self.activate = False
                self.wave = False

    def generIc(self, icone: str) -> object:
        """Redimensionne l'icône pour qu'elle s'adapte à la taille du bouton.

        Args:
            icone (str): l'icône a utiliser.

        Returns:
            object: La texture créée par l'icône redimensionnée.
        """
        if type(icone) == str and icone != '':
            if file_exists(icone):
                ico = load_image(icone)
                facteur = self.taille.tailleIcone/ico.height
                image_resize(ico, int(ico.width*facteur), int(ico.height*facteur))
                ima = load_texture_from_image(ico)
                unload_image(ico)
            else:
                ima = False
        else:
            ima = False
        return ima

    def execute(self) -> None:
        """Gère ce qui se passe quand on appuie sur le bouton.
        """
        if not self.actif:
            if is_mouse_button_pressed(0):
                if self.getContact():
                    self.activate = True
                    self.actif = True
        else:
            if self.verifFonction() and not self.activate:
                self.actif = False
                self.fonction()

    def verification(self) -> bool:
        """Fonction par défaut pour la vérification d'instruction spéciale.

        Returns:
            bool: True.
        """
        return True

    def getContact(self) -> bool:
        """Vérifie si le curseur est sur le bouton.

        Returns:
            bool: True si le curseur est sur le bouton, False dans le cas contraire.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[2]:
            if y >= self.coords[1] and y <= self.coords[3]:
                rep = True
        return rep

    def getDims(self) -> list:
        return [self.largeur, self.taille.hauteur]

    def setLargeur(self, largeur: int = 0) -> None:
        h = self.taille.hauteur
        if not self.apparence.texte or self.apparence.icone == 2:
            l = h
        else:
            if not self.icone:
                l = self.texte.getDims()[0] + int(h*0.5)
            else:
                l = int(h*1.6) + self.texte.getDims()[0]
        if l < largeur:
            self.largeur = largeur
        else:
            self.largeur = l