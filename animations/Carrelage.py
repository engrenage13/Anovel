from random import randint, choice
from FondMarin import fond, xf, yf, gris, mer
from animations.Paillette import Paillette

class Etincelle:
    def __init__(self, nombre: int = 10, couleurs: list = [gris]+mer) -> None:
        self.liste = []
        self.couleurs = couleurs
        self.run = True
        for i in range(nombre):
            self.liste.append(Paillette(i+1))

    def eblouissement(self) -> None:
        """Gère l'intégralité de l'animation avec les paillettes.
        """
        for i in range(len(self.liste)):
            if not self.liste[i].getEtat() and self.run:
                t = randint(int(yf/40), int(yf/30))
                x = randint(0, xf-t)
                y = randint(0, yf-t)
                self.liste[i].dessine(x, y, choice(self.couleurs))
        if self.run:
            fond.after(50, self.eblouissement)
        
    def fin(self) -> None:
        """Met fin à l'animation des paillettes.
        """
        self.run = False