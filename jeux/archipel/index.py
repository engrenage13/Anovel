from jeux.archipel.scene import Scene
from jeux.archipel.menu import Menu
from jeux.archipel.config import config
from jeux.archipel.jeu.archipel import Archipel as archi

arch = archi

class Archipel:
    """La porte d'entrée vers le jeu.
    """
    def __init__(self) -> None:
        """Initialise le système de lien entre les différentes fenêtres.
        """
        # Between the worlds
        self.play = False
        self.message = ""
        self.lu = True

    def dessine(self) -> None:
        """Dessine la partie active du jeu.
        """
        self.scene.dessine()
        if self.actif != self.scene:
            self.actif.dessine()
        if not self.actif.lu:
            if self.actif.message in ("QUITTE", "ANOVEL_OPTIONS", "ANOVEL_MENU"):
                self.actif.lu = True
                self.nouveauMessage(self.actif.message)
            else:
                if self.actif == self.scene:
                    self.actif.lu = True
                    self.actif.setPlay(False)
                    if self.actif.message == "ARCHIPEL_MENU":
                        self.actif = self.menu
                    self.actif.play = True
                else:
                    if self.actif.ok:
                        if not self.actif.playAnim:
                            self.actif.playAnim = True
                    else:
                        self.actif.lu = True
                        self.actif.play = False
                        self.actif = self.scene
                        self.actif.setPlay(True)

    def initialise(self) -> None:
        """Crée les différentes fenêtres du jeu et désigne laquelle doit s'activer en première.
        """
        self.scene = Scene()
        self.menu = Menu()
        self.scene.setPlay(True)
        if config['dev'] == 'menu':
            self.actif = self.menu
        else:
            self.actif = self.scene

    # Between the worlds
    def nouveauMessage(self, message: str) -> None:
        """Rédige un message addressé au système d'Anovel.

        Args:
            message (str): Le message à envoyer.
        """
        self.message = message
        self.lu = False