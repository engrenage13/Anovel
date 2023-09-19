from systeme.FondMarin import *
from ui.bouton.taille import Taille
from ui.bouton.apparence import Apparence
from ui.blocTexte import BlocTexte
from animations.Paillette import Paillette

class BoutonPression:
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
        # jauge
        self.pourcentage = 0.0
        # Largeur
        self.setLargeur()
        # Paillettes
        self.paillettes = []
        self.tEtoiles = 0

    def dessine(self, x: int, y: int) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            x (int): Abcisse du centre du bouton.
            y (int): Ordonnée du centre du bouton.
        """
        h = self.taille.hauteur
        l = self.largeur
        self.coords = [x-int(l/2), y-int(h/2), x+int(l/2), y+int(h/2)]
        couleur = self.apparence.couleur1
        if self.getContact() and self.apparence.couleur2:
            couleur = self.apparence.couleur2
        multip = self.pourcentage
        if self.actif:
            multip = 1
        if self.verifFonction():
            draw_rectangle_rounded((self.coords[0], self.coords[1], l, h), 0.15, 30, couleur)
            draw_rectangle_rounded((self.coords[0], self.coords[1], l*multip, h), 0.15, 30, [18, 204, 27, 255])
        draw_rectangle_rounded_lines((self.coords[0], self.coords[1], l, h), 0.15, 30, 2, BLACK)
        # Texte & Icône
        coloTex = WHITE
        if couleur[0] > 170 and couleur[1] > 170 and couleur[2] > 170:
            coloTex = BLACK
        if self.icone:
            image = self.icone
            if not self.apparence.texte:
                draw_texture(image, x-int(image.width/2), y-int(image.height/2), WHITE)
            else:
                tt = self.texte.getDims()
                xt = x+int(image.width/2)
                self.texte.dessine([[xt, y-int(tt[1]*0.1)], 'c'], coloTex)
                draw_texture(image, xt-int(tt[0]/2+image.width*1.1), y-int(image.height/2), WHITE)
        else:
            self.texte.dessine([[x, y-int(self.texte.getDims()[1]*0.1)], 'c'], coloTex)
        if self.verifFonction():
            self.execute()
        if self.actif:
            for i in range(len(self.paillettes)):
                self.paillettes[i].dessine()
            if self.tEtoiles < 90:
                self.tEtoiles += 1
            else:
                self.actif = False
                self.tEtoiles = 0
                self.fonction()

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
        if self.getContact() and is_mouse_button_down(0):
            if self.pourcentage < 1.0:
                self.pourcentage += 0.015
                if self.pourcentage > 1.0:
                    self.pourcentage = 1.0
            else:
                if len(self.paillettes) == 0:
                    for i in range(8):
                        self.paillettes.append(Paillette(self.coords, 
                            [(104, 235, 100, 255), (131, 222, 62, 255), (25, 181, 20, 255)]))
                self.actif = True
        else:
            if self.pourcentage > 0.0:
                self.pourcentage -= 0.02
                if self.pourcentage < 0.0:
                    self.pourcentage = 0.0

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