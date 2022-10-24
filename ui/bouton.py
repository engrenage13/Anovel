from systeme.FondMarin import *
from systeme.set import trouveParam
from ui.blocTexte import BlocTexte
from ui.ptiBouton import PtiBouton
from animations.etincelles import Etincelles

class Bouton(PtiBouton):
    def __init__(self, fonctions: list, couleur: list, texte:str=None, icone:list=None) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            couleur (list): Couleur de fond du bouton.
            texte (str, optional): Ecritaut sur le bouton.. Defaults to None.
            icone (list, optional): 1. Adresse de l'icône. 2. Position de l'icône. Defaults to None.
        """
        if icone == None:
            ico = None
        elif type(icone) == list:
            ico = icone[0]
        super().__init__(fonctions, couleur, texte, ico)
        self.largeur = int(tlatba*0.7)
        # Icône
        if icone != None:
            if file_exists(icone[0]):
                self.iconeOriginale = load_image(icone[0])
                if icone[1].lower() in ['d', 'droite', '->', '>']:
                    position = 'd'
                else:
                    position = 'g'
                self.positionIcone = position
                ico = self.redimIc()
                self.icone = ico
                dicone = [ico.width, ico.height]
            else:
                self.iconeOriginale = None
        else:
            self.iconeOriginale = None
        # Texte
        if type(texte) == str and texte != "":
            taille = [int(self.largeur*0.9), int(self.hauteur*0.9)]
            if self.iconeOriginale != None:
                taille[0] -= dicone[0]
            self.texte = BlocTexte(texte, police1, int(self.hauteur*0.45), taille)

    def dessine(self, coord: tuple, important:bool=False) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple): Coordonnées du centre du bouton.
            important (bool, optional): Le bouton doit-il attirer l'attention. Defaults to False.
        """
        l = self.largeur
        h = self.hauteur
        self.coords = [coord[0]-int(l/2), coord[1]-int(h/2), coord[0]+int(l/2), coord[1]+int(h/2)]
        if self.etincelles == None:
            self.etincelles = Etincelles([self.coords[0], self.coords[1], l, h], 
                                         [self.couleur, [246, 203, 33, 255]])
        self.etincelles.setCoordSource([self.coords[0], self.coords[1], l, h])
        if important and trouveParam("anims") >= 2:
            if self.getContact():
                artifice = True
            else:
                artifice = False
            self.etincelles.dessine(artifice)
        couleur = self.couleur
        if self.getContact():
            couleur = self.actif()
        draw_rectangle_rounded((self.coords[0]+2, self.coords[1]+2, l, h), 0.2, 30, BLACK)
        draw_rectangle_rounded((self.coords[0], self.coords[1], l, h), 0.2, 30, couleur)
        # Texte + Icône
        if self.texte != None:
            coloTex = WHITE
            if self.couleur[0] > 170 and self.couleur[1] > 170 and self.couleur[2] > 170:
                coloTex = BLACK
            ctx = int(self.coords[0]+l/2)
            if self.iconeOriginale != None:
                image = self.icone
                if self.positionIcone == 'd':
                    ctx -= int(self.icone.width/2)
                    ci = int(self.coords[2]-image.width*1.1)
                else:
                    ctx += int(self.icone.width/2)
                    ci = int(self.coords[0]+image.width*0.1)
                draw_texture(image, ci, 
                             self.coords[1]+int((self.coords[3]-self.coords[1]-image.height)/2), WHITE)
            self.texte.dessine([[ctx, int(self.coords[1]+h/2)], 'c'], coloTex)
        self.execute()

    def redimIc(self) -> object:
        """Redimensionne l'icône pour qu'elle s'adapte à la taille du bouton.

        Returns:
            object: La texture créée par l'icône.
        """
        facteur = self.hauteur*0.9/self.iconeOriginale.height
        ico = self.iconeOriginale
        image_resize(ico, int(ico.width*facteur), int(ico.height*facteur))
        ima = load_texture_from_image(ico)
        unload_image(self.iconeOriginale)
        return ima