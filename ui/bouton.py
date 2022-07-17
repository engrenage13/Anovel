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
            icone (str, optional): Icône sur le bouton. Defaults to None.
        """
        self.lset = int(tlatba*0.7)
        self.hset = int(yf*0.075)
        self.texte = texte
        self.icone = icone
        self.couleur = couleurs
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
        self.notif = Notification("Option indisbonible", "Ce bouton est désactivé")
        self.notif.setPosition(1)
        self.etatNotif = False
        # Affichage
        #bouton = load_image('images/ui/bouton.png')
        #image_resize(bouton, int(bouton.width*0.13), int(bouton.height*0.13))
        #self.fond = load_texture_from_image(bouton)

    def dessine(self, coord: tuple, limites: bool) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple): Coordonnées du centre du bouton.
            limites (bool): Si True, le bouton sera bloqué à une taille prédéfinie.
        """
        dims = self.mesureTaille(limites)
        self.coords = [coord[0]-int(dims[0]/2), coord[1]-int(dims[1]/2), coord[0]+int(dims[0]/2), 
                       coord[1]+int(dims[1]/2)]
        couleur = self.couleur[0]
        if self.getContact():
            couleur = self.couleur[1]
        draw_rectangle_rounded((self.coords[0]+2, self.coords[1]+2, dims[0], dims[1]), 0.2, 30, BLACK)
        draw_rectangle_rounded((self.coords[0], self.coords[1], dims[0], dims[1]), 0.2, 30, couleur)
        if type(self.texte) != None:
            self.blocTexte.dessine([coord, 'c'])
        if self.etatNotif:
            self.notif.dessine()
            if self.notif.getDisparition():
                self.etatNotif = False
        self.execute()

    def mesureTaille(self, limites: bool) -> list:
        dims = [self.lset, self.hset]
        if self.texte != None:
            if limites:
                taille = [dims[0]-40, dims[1]-20]
            else:
                taille = []
            self.blocTexte = BlocTexte(self.texte, police1, int(self.hset*0.45), taille)
            if not limites:
                dims = [self.blocTexte.tCadre[0]+40, self.blocTexte.tCadre[1]+20]
        return dims

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