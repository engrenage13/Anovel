from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from animations.etincelles import Etincelles

class PtiBouton:
    def __init__(self, fonctions: list, couleur: list, texte:str=None, icone:str=None) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            couleur (list): Couleur de fond du bouton.
            texte (str, optional): Ecritaut sur le bouton.. Defaults to None.
            icone (str, optional): Icône sur le bouton. Defaults to ['', 'e'].
        """
        self.hauteur = int(yf*0.075)
        self.largeur = int(tlatba*0.31)
        self.texte = None
        if type(texte) == str and texte != "":
            self.texte = BlocTexte(texte, police1, int(self.hauteur*0.4), [self.largeur, ''])
        self.couleur = couleur
        self.coloPreset = 'max'
        # Fonctions
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
        # Icône
        if icone != None:
            self.iconeOriginale = load_image(icone)
        else:
            self.iconeOriginale = None
        self.icoCharge = False
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
        if self.iconeOriginale != None:
            if not self.icoCharge:
                ico = self.redimIc()
                self.icone = ico
                self.icoCharge = True
        l = self.largeur
        h = self.hauteur
        self.coords = [coord[0]-int(l/2), coord[1]-int(h/2), coord[0]+int(l/2), coord[1]+int(h/2)]
        if self.etincelles == None:
            self.etincelles = Etincelles([self.coords[0], self.coords[1], l, h], 
                                         [self.couleur, [246, 203, 33, 255]])
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
        # Icône
        if self.icoCharge:
            image = self.icone
            y = int(self.coords[1]+(self.coords[3]-self.coords[1]-image.height)/2)
            if self.texte != None:
                y = int(y - self.texte.getDims()[1]*0.65)
            draw_texture(image, int(self.coords[0]+l/2-image.width*0.5), y, WHITE)
        # Texte
        if self.texte != None:
            coloTex = WHITE
            if couleur[0] > 170 and couleur[1] > 170 and couleur[2] > 170:
                coloTex = BLACK
            self.texte.dessine([[int(self.coords[0]+l/2), 
                               int(self.coords[1]+h*0.98-self.texte.getDims()[1]/2)], 'c'], coloTex)
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
        facteur = self.hauteur*0.8/self.iconeOriginale.height
        ico = self.iconeOriginale
        image_resize(ico, int(ico.width*facteur), int(ico.height*facteur))
        self.icoCharge = True
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