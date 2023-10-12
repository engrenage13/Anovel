from systeme.FondMarin import RED, BLUE
from random import randint
from jeux.archipel.objets.Joueur import Joueur

libat = ["gafteur", "ferpasseur"]
lij = [{"nom": "Lyra", "couleur": BLUE}, {"nom": "Will", "couleur": RED}]
c = randint(0, len(libat)-1)

def creeJoueur(nombre: int) -> Joueur:
    nombre = nombre % len(lij)
    if nombre == 0:
        bat = libat[c]
    else:
        bat = libat[len(libat)-1-c]
    j = Joueur(lij[nombre]["nom"], [bat], lij[nombre]["couleur"])
    return [j[0], j]