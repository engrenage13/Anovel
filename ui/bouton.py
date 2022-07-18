from systeme.FondMarin import *
from ui.notif import Notification
from ui.blocTexte import BlocTexte

class Bouton:
    def __init__(self, fonctions: list, couleurs: list, texte:str=None, icone:str=None) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            couleurs (list): Liste des couleurs utilisés pour le bouton.
            texte (str, optional): Ecritaut sur le bouton.. Defaults to None.
            icone (str, optional): Icône sur le bouton. Defaults to ['', 'e'].
        """
        self.lset = int(tlatba*0.7)
        self.hset = int(yf*0.075)
        self.texte = texte
        self.couleurs = couleurs
        self.coloPreset = 'max'
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
        self.notif = Notification("Option indisbonible", "Ce bouton est désactivé")
        self.notif.setPosition(1)
        self.etatNotif = False
        # Icône
        if icone != None:
            self.iconeOriginale = load_image(icone)
        else:
            self.iconeOriginale = None
        self.icoCharge = False

    def dessine(self, coord: tuple, limites: bool, important:bool=False) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple): Coordonnées du centre du bouton.
            limites (bool): Si True, le bouton sera bloqué à une taille prédéfinie.
            important (bool, optional): Le bouton doit-il attirer l'attention. Defaults to False.
        """
        dims = self.mesurePlus(limites)
        if len(dims) == 1:
            l = dims[0][0]
            h = dims[0][1]
            self.coords = [coord[0]-int(l/2), coord[1]-int(h/2), coord[0]+int(l/2), coord[1]+int(h/2)]
        else:
            l = dims[0][0] + dims[1][0]
            h = dims[0][1]
            if h < dims[1][1]:
                h = dims[1][1]
            self.coords = [coord[0]-int(l/2), coord[1]-int(h/2), coord[0]+int(l/2), coord[1]+int(h/2)]    
        if important:
            if not self.getContact():
                self.couleur = [255, 221, 0, 255]
            else:
                self.Important()
                draw_rectangle_rounded((self.coords[0]-self.lumi, self.coords[1]-self.lumi, l+self.lumi*2, h+self.lumi*2), 
                                       0.2, 30, [self.couleur[0], self.couleur[1], self.couleur[2], 200])
        else:
            self.couleur = self.couleurs[0]
            if self.getContact():
                self.couleur = self.couleurs[1]
        draw_rectangle_rounded((self.coords[0]+2, self.coords[1]+2, l, h), 0.2, 30, BLACK)
        draw_rectangle_rounded((self.coords[0], self.coords[1], l, h), 0.2, 30, self.couleur)
        if self.texte != None:
            coloTex = WHITE
            if (self.couleur[0] > 160 and self.couleur[1] > 160 and self.couleur[2] > 160) or important:
                coloTex = BLACK
            self.blocTexte.dessine([[int(self.coords[0]+dims[0][0]/2), int(self.coords[1]+dims[0][1]/2)], 'c'], 
                                   coloTex)
        if len(dims) == 2:
            image = dims[1][2]
            draw_texture(image, self.coords[2]-image.width, 
                         self.coords[1]+int((self.coords[3]-self.coords[1]-image.height)/2), WHITE)
        if self.etatNotif:
            self.notif.dessine()
            if self.notif.getDisparition():
                self.etatNotif = False
        self.execute()

    def mesurePlus(self, limites: bool) -> list:
        dims = [[self.lset, self.hset]]
        if self.iconeOriginale != None:
            if not self.icoCharge:
                ico = self.redimIc()
                self.icone = ico
            else:
                ico = self.icone
            dicone = [ico.width, ico.height, ico]
        if self.texte != None:
            if limites:
                taille = [dims[0][0]-40, dims[0][1]-20]
                if self.iconeOriginale != None:
                    taille[0] -= dicone[0]
            else:
                taille = []
            self.blocTexte = BlocTexte(self.texte, police1, int(self.hset*0.45), taille)
            if not limites:
                ditexte = [self.blocTexte.tCadre[0]+40, self.blocTexte.tCadre[1]+20]
                dims = ditexte
            if self.iconeOriginale != None:
                dims[0][0] -= dicone[0]
        if self.iconeOriginale != None:
            dims.append(dicone)
        return dims

    def redimIc(self) -> object:
        facteur = self.hset/self.iconeOriginale.height
        ico = self.iconeOriginale
        image_resize(ico, int(ico.width*facteur), int(ico.height*facteur))
        self.icoCharge = True
        return load_texture_from_image(ico)

    def Important(self) -> None:
        min = [173, 144, 50, 255]
        max = [255, 221, 0, 255]
        comparateur = max
        if self.coloPreset == 'max':
            if self.couleur != max:
                comparateur = max
            else:
                self.coloPreset = 'min'
        elif self.coloPreset == 'min':
            if self.couleur != min:
                comparateur = min
            else:
                self.coloPreset = 'max'
        colo = []
        for i in range(len(self.couleur)):
            if self.couleur[i] < comparateur[i]:
                colo.append(self.couleur[i] + 1)
            elif self.couleur[i] > comparateur[i]:
                colo.append(self.couleur[i] - 1)
            else:
                colo.append(self.couleur[i])
        self.couleur = colo
        pourc = (self.couleur[0] - min[0])/(max[0] - min[0])
        self.lumi = int(7*pourc)

    def execute(self) -> None:
        """Gère ce qui se passe quand on appuie sur le bouton.
        """
        if is_mouse_button_pressed(0):
            if self.getContact():
                if self.verifFonction():
                    self.fonction()
                else:
                    self.etatNotif = True

    def verification(self) -> bool:
        """Fonction par défaut pour la vérification d'instruction spéciale.

        Returns:
            bool: True.
        """
        return True

    def getTexte(self) -> str:
        """Retourne le texte écrit sur le bouton du bouton.

        Returns:
            str: Texte du bouton.
        """
        return self.texte

    def setTexte(self, texte: str) -> None:
        """Permet de modifier le texte du bouton.

        Args:
            texte (str): Modifie le texte affiché sur le bouton.
        """
        self.texte = texte

    def setTexteNotif(self, titre: str="", texte: str="") -> None:
        """Permet de modifier le texte de la notification liée.

        Args:
            titre (str): Modifie le titre de la notif.
            texte (str): Modifie le message de la notif.
        """
        if titre != "":
            self.notif.modifTitre(str(titre))
        if texte != "":
            self.notif.modifTexte(str(texte))

    def getCouleurs(self) -> list:
        """Retourne les couleurs utilisés par le bouton.

        Returns:
            list: couleur de base du fond, couleur de surbrillement et couleur du texte.
        """
        return self.couleur

    def setCouleurs(self, couleurs: list) -> None:
        """Permet de modifier les couleurs utilisées par le bouton.

        Args:
            couleurs (list): Première pour le fond du bouton, seconde pour surbrillement et 
            troisième pour le texte.
        """
        self.couleur = couleurs

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