from systeme.FondMarin import *
from ui.notif import Notification

class Bouton:
    def __init__(self, fonction, texte: str, couleurs: list) -> None:
        """Crée un bouton.

        Args:
            fonction (_type_): Fonction qu'appelle le bouton quand il est utilisé.
            texte (str): Ecritaut sur le bouton.
            couleurs (list): Liste des couleurs utilisés pour le bouton.
        """
        self.texte = texte
        self.couleur = couleurs
        self.etat = True
        self.fonction = fonction
        self.dims = [int(tlatba*0.8), int(yf*0.1)]
        self.notif = Notification("Option indisbonible", "Ce bouton est désactivé")
        self.notif.setPosition('gauche')
        self.etatNotif = False

    def dessine(self, coord: tuple) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple, optional): Coordonnées du centre du bouton.
        """
        tt = measure_text_ex(police1, self.texte, 30, 0)
        self.coords = [coord[0]-int(self.dims[0]/2), coord[1]-int(self.dims[1]/2), coord[0]+int(self.dims[0]/2), 
                       coord[1]+int(self.dims[1]/2)]
        couleur = self.couleur[0]
        if self.getContact():
            couleur = self.couleur[1]
        couleur2 = [int(couleur[0]*0.5), int(couleur[1]*0.5), int(couleur[2]*0.5), couleur[3]]
        draw_rectangle_rounded((self.coords[0], self.coords[1], self.dims[0], self.dims[1]), 0.2, 30, couleur)
        draw_rectangle_rounded_lines((self.coords[0], self.coords[1], self.dims[0], self.dims[1]), 0.2, 30, 4, 
                                     couleur2)
        draw_text_pro(police1, self.texte, (coord[0]-int(tt.x/2), coord[1]-int(tt.y/3)), (0, 0), 0, 30, 0, 
                      self.couleur[2])
        if self.etatNotif:
            self.notif.dessine()
            if self.notif.getDisparition():
                self.etatNotif = False
        self.execute()

    def execute(self) -> None:
        """Gère ce qui se passe quand on appuie sur le bouton.
        """
        if is_mouse_button_pressed(0):
            if self.getContact():
                if self.etat:
                    self.fonction()
                else:
                    self.etatNotif = True

    def getEtat(self) -> bool:
        """Retourne l'état du bouton.

        Returns:
            bool: état du bouton sous forme de Actif/Inactif -> True/False.
        """
        return self.etat

    def setEtat(self, etat: bool) -> None:
        """Permet de modifier l'etat du bouton (actif/inactif).

        Args:
            etat (bool): True pour le rendre actif, False pour le désactiver.
        """
        self.etat = etat

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
        if self.titre != "":
            self.notif.modifTitre(str(titre))
        if self.texte != "":
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