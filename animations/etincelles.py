from systeme.FondMarin import *
from random import randint, choice

class Etincelles:
    def __init__(self, source: list, couleurs: list) -> None:
        """Crée un créateur d'étincelles.

        Args:
            source (list): Une zone rectangulaire d'où les étincelles doivent partir.
            couleurs (list): La ou les couleurs souhaitées pour les étincelles.
        """
        self.source = source
        self.couleurs = couleurs
        self.nbParticule = 10
        self.particules = ['x']*self.nbParticule
        self.tmax = 5
        self.tmin = 1

    def dessine(self) -> None:
        """Permet d'afficher les étincelles à l'écran.
        """
        i = 0
        self.hmax = int(self.source[1]-self.source[3]*50)
        while i < len(self.particules):
            if type(self.particules[i]) == list:
                x = self.particules[i][0]
                y = self.particules[i][1]
                t = self.particules[i][2]
                draw_circle(x, y, t, self.particules[i][3])
                self.bougeParticule(i)
            else:
                self.creeParticule()
            i = i + 1

    def bougeParticule(self, particule: int) -> None:
        """Permet de deplacer et modifier les les étincelles.

        Args:
            particule (int): L'étincelle à modifier.
        """
        evo = randint(1, 10)
        y = self.particules[particule][1]
        t = self.particules[particule][2]
        if y > self.hmax:
            pas = self.tmax - t + 1
            y = y - pas
            self.particules[particule][1] = y
            if evo <= 3:
                t = t - 1
                self.particules[particule][2] = t
                if t == 0:
                    self.particules[particule] = 'x'
            elif evo == 10:
                if t < self.tmax:
                    t = t + 1
                    self.particules[particule][2] = t
        else:
            self.particules[particule] = 'x'

    def creeParticule(self) -> None:
        """Crée une étincelle.
        """
        position = -1
        i = 0
        while i < len(self.particules) and position < 0:
            if type(self.particules[i]) == str:
                position = i
            else:
                i = i + 1
        x = self.source[0]
        y = self.source[1]
        l = self.source[2]
        h = self.source[3]
        c = choice(self.couleurs)
        particule = []
        particule.append(randint(x, x+l))
        particule.append(randint(y, y+h))
        particule.append(randint(self.tmin, self.tmax))
        particule.append(c)
        self.particules[position] = particule

    def setCoordSource(self, coord: list) -> None:
        """Permet de modifier la position de la source des étincelles.

        Args:
            coord (list): Les nouvelles coordonnées.
        """
        if len(coord) == 4:
            self.source = coord