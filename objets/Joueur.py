from random import *
from FondMarin import *
from objets.BateauJoueur import Bateau
from placement import placeLat
from objets.plateau import plateau

class Joueur(): # Initialise un joueur.
    def __init__(self, code: int, liBat: list, ombre: bool = False):
        a = 'base' + str(code)
        d = 'nSet' + str(code)
        e = 'set' + str(code)
        f = 'cTire' + str(code)
        b = ["Porte Avion", "Croiseur", "Sous-marin n°1", "Sous-marin n°2", "Torpilleur"]
        c = [5, 4, 3, 3, 2]
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.base = plateau(10, 10, mer, a)
        self.cTire = plateau(10, 10, mer, f)
        fond.itemconfigure(f, state='hidden')
        self.SetBateaux = liBat
        self.pret = False
        joueurs.append(self)
        # bateaux
        for i in range(len(b)):
            Bateau(b[i], c[i], i, code)
        fond.itemconfigure(d, font=Poli1)
        # /bateaux
        if ombre:
            fond.itemconfigure(a, state='hidden')
            fond.itemconfigure(d, state='hidden')
            fond.itemconfigure(e, state='hidden')
        shuffle(self.SetBateaux)
        placeLat(self.SetBateaux)