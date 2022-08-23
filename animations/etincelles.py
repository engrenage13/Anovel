from systeme.FondMarin import *
from random import randint, choice

class Etincelles:
    def __init__(self, source: list, couleur: list) -> None:
        """Crée un créateur d'étincelles.

        Args:
            source (list): Une zone rectangulaire d'où les étincelles doivent partir.
            couleur (list): La ou les couleurs souhaitées pour les étincelles.
        """
        self.source = source
        self.couleur = couleur[0]
        coPLus = couleur[0]
        if len(couleur) == 2:
            coPLus = couleur[1]
        self.couleurSup = coPLus
        self.nbParticule = 10
        self.particules = ['x']*self.nbParticule
        self.tmax = 5
        self.tmin = 1

    def dessine(self, artifice: bool) -> None:
        """Permet d'afficher les étincelles à l'écran.

        Args:
            artifice (bool): Si True, les étincelles seront plus importantes.
        """
        i = 0
        if artifice:
            self.hmax = int(self.source[1]-self.source[3]*1.2)
            boost = 1
        else:
            self.hmax = int(self.source[1]-self.source[3]*0.8)
            boost = 0
        while i < len(self.particules):
            if type(self.particules[i]) == list:
                x = self.particules[i][0]
                y = self.particules[i][1]
                t = self.particules[i][2]
                draw_circle(x, y, t, self.particules[i][3])
                self.bougeParticule(i, boost)
            else:
                self.creeParticule(artifice)
            i = i + 1

    def bougeParticule(self, particule: int, booster: int) -> None:
        """Permet de deplacer et modifier les les étincelles.

        Args:
            particule (int): L'étincelle à modifier.
            booster (int): Boost de vitesse accorder à l'étincelle.
        """
        evo = randint(1, 10)
        y = self.particules[particule][1]
        t = self.particules[particule][2]
        if y > self.hmax:
            pas = self.tmax - t + 1 + booster
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

    def creeParticule(self, artifice: bool) -> None:
        """Crée une étincelle.

        Args:
            artifice (bool): Si True, modifie certaines des conditions de création (pour plus de spectacle).
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
        if artifice:
            c = choice([self.couleur, self.couleurSup])
        else:
            c = self.couleur
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