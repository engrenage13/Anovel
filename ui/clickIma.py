from systeme.FondMarin import *
from ui.notif import Notification

class ClickIma:
    def __init__(self, fonctions: list, images: list) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            images (list): Liste des images utilisées.
        """
        self.images = images[:]
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
        self.notif = Notification("Option indisbonible", "Ce bouton est désactivé")
        self.notif.setPosition(1)
        self.etatNotif = False

    def dessine(self, coord: tuple) -> None:
        """Dessine la clickIma à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple): Coordonnées du centre de la clickIma.
        """
        self.coords = coord
        image = self.images[0]
        if self.getContact():
            image = self.images[1]
        draw_texture(image, self.coords[0], self.coords[1], WHITE)
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

    def getImages(self) -> list:
        """Retourne les images utilisés par la clickIma.

        Returns:
            list: image de base du fond, image de surbrillement.
        """
        return self.images

    def setImages(self, images: list) -> None:
        """Permet de modifier les images utilisés par la clickIma.

        Args:
            imagess (list): Première pour l'apparence de base, seconde pour le surbrillement.
        """
        self.images = images

    def getContact(self) -> bool:
        """Vérifie si le curseur est sur la clickIma.

        Returns:
            bool: True si le curseur est sur la clickIma, False dans le cas contraire.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[0]+self.images[0].width:
            if y >= self.coords[1] and y <= self.coords[1]+self.images[0].height:
                rep = True
        return rep