from random import randint
from systeme.FondMarin import *

DISTANCEPOINTS = int(yf*0.01)
TAILLECASE = int(xf*0.13)
TAILLEPETITECASE = int(xf*0.035)
EAUX = [[48, 201, 201, 255], [48, 140, 201, 255], [29, 79, 171, 255]]

def marqueCases(plateau: list[list], pourcentMin: int, pourcentMax: int) -> None:
    nbTour = definiNombreTour(plateau, pourcentMin, pourcentMax)
    for i in range(nbTour):
        x = randint(0, plateau.nbCases-1)
        y = randint(0, plateau.nbCases-1)
        if not plateau.cases[x][y].marqueur:
            +plateau.cases[x][y]

def definiNombreTour(plateau: list[list], pourcentMin: int, pourcentMax: int) -> int:
    nbCases = plateau.nbCases*plateau.nbCases
    pourcent = randint(pourcentMin, pourcentMax)
    multi = pourcent/100
    return int(nbCases*multi)