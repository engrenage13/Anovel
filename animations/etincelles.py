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
        self.particules = []
        self.nbParticule = 10
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
        else:
            self.hmax = int(self.source[1]-self.source[3]*0.8)
        while i < len(self.particules):
            x = self.particules[i][0]
            y = self.particules[i][1]
            t = self.particules[i][2]
            draw_circle(x, y, t, self.particules[i][3])
            morte = self.bougeParticule(i)
            if not morte:
                i = i + 1
        if len(self.particules) < self.nbParticule:
            self.creeParticule(artifice)

    def bougeParticule(self, particule: int) -> bool:
        """Permet de deplacer et modifier les les étincelles.

        Args:
            particule (int): L'étincelle à modifier.

        Returns:
            bool: True si l'étincelle a disparue.
        """
        evo = randint(1, 10)
        rep = False
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
                    del self.particules[particule]
                    rep = True
            elif evo == 10:
                if t < self.tmax:
                    t = t + 1
                    self.particules[particule][2] = t
        else:
            del self.particules[particule]
            rep = True
        return rep

    def creeParticule(self, artifice: bool) -> None:
        """Crée une étincelle.

        Args:
            artifice (bool): Si True, modifie certaines des conditions de création (pour plus de spectacle).
        """
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
        self.particules.append(particule)