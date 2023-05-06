from jeux.Jeu_1.scene import Scene
from jeux.Jeu_1.menu import Menu
from jeux.Jeu_1.config import config

class J1:
    def __init__(self) -> None:
        # Between the worlds
        self.play = False
        self.message = ""
        self.lu = True

    def dessine(self) -> None:
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
                    if self.actif.message == "J1_MENU":
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
        self.scene = Scene()
        self.menu = Menu()
        self.scene.setPlay(True)
        if config['dev'] == 'menu':
            self.actif = self.menu
        else:
            self.actif = self.scene

    # Between the worlds
    def nouveauMessage(self, message: str) -> None:
        self.message = message
        self.lu = False