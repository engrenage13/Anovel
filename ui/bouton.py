from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from animations.etincelles import Etincelles

class Bouton:
    def __init__(self, fonctions: list, couleur: list, texte:str=None, icone:list=None) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            couleur (list): Couleur de fond du bouton.
            texte (str, optional): Ecritaut sur le bouton.. Defaults to None.
            icone (list, optional): 1. Adresse de l'icône sur le bouton. 2. Position de l'icône. Defaults to None.
        """
        self.largeur = int(tlatba*0.7)
        self.hauteur = int(yf*0.075)
        self.couleur = couleur
        # Fonctions
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
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
        if texte != None:
            taille = [int(self.largeur*0.9), int(self.hauteur*0.9)]
            if self.iconeOriginale != None:
                taille[0] -= dicone[0]
            self.texte = BlocTexte(texte, police1, int(self.hauteur*0.45), taille)
        # Couleur +
        self.maxEchelle = 51
        self.minEchelle = 0
        self.posEchelle = None
        self.monte = True
        # Animations
        self.etincelles = None

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
        if important:
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

    def actif(self) -> list:
        """Gère l'évolution de la couleur du bouton lorsque celui-ci est survolé.

        Returns:
            list: La couleur évolué pour l'afficher.
        """
        colo = []
        val = self.couleur[0]
        pos = 0
        for i in range(3):
            if val < self.couleur[i]:
                val = self.couleur[i]
                pos = i
        if self.posEchelle == None:
            self.posEchelle = int(val/5)
        else:
            if self.monte:
                if self.posEchelle < self.maxEchelle:
                    self.posEchelle += 1
                else:
                    self.monte = False
            else:
                if self.posEchelle > self.minEchelle:
                    self.posEchelle -= 1
                else:
                    self.monte = True
        for i in range(len(self.couleur)):
            if pos == i:
                pigment = self.posEchelle*5
            else:
                pigment = self.couleur[i]
            colo.append(pigment)
        return colo

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

    def execute(self) -> None:
        """Gère ce qui se passe quand on appuie sur le bouton.
        """
        if is_mouse_button_pressed(0):
            if self.getContact():
                if self.verifFonction():
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
        """Retourne les dimensions du bouton.

        Returns:
            list: 1. Largeur. 2. Hauteur.
        """
        return [self.largeur, self.hauteur]