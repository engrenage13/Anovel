from random import *
from FondMarin import *
from objets.BateauJoueur import Bateau
from objets.plateau import plateau

class Joueur(): # Initialise un joueur.
    def __init__(self, code: int):
        a = 'base' + str(code)
        f = 'cTire' + str(code)
        b = ["Porte Avion", "Croiseur", "Sous-marin n°1", "Sous-marin n°2", "Torpilleur"]
        c = [5, 4, 3, 3, 2]
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.base = plateau(10, 10, mer, a)
        self.cTire = plateau(10, 10, mer, f)
        self.SetBateaux = []
        self.pret = False
        joueurs.append(self)
        # bateaux
        for i in range(len(b)):
            bat = Bateau(b[i], c[i], i, code)
            self.SetBateaux.append(bat)
        # /bateaux
        shuffle(self.SetBateaux)

    def getBateaux(self) -> list:
        return self.SetBateaux

    def dessineBateaux(self) -> None:
        for i in range(len(self.SetBateaux)):
            self.SetBateaux[i].dessine(self.id)

    def montreBase(self) -> None:
        fond.itemconfigure('base' + str(self.id), state='normal')

    def miseEnPlace(self) -> None:
        self.montreBase()
        self.dessineBateaux()
        self.placeLat()

    def blocVert(self, bateau: object): # Désélectionne tout les bateaux à part celui qui vient d'être sélectionné.
        for i in range(len(self.getBateaux())):
            if bateau != self.SetBateaux[i]:
                if self.SetBateaux[i].defil:
                    self.SetBateaux[i].immobile()

    def vigile(self):
        # Remet les bateaux rejetés du plateau, correctement en place dans le panneau latéral.
        a = False
        c = fond.coords('pg')
        l = self.getBateaux()
        for i in range(len(l)):
            t = l[i].getTags()
            b = fond.coords(t[0])
            if int(b[0]) <= int(c[2]*0.05):
                a = True
        if a:
            self.placeLat()
        else:
            fond.after(1000, self.vigile)

    def placeLat(self): # Place les bateaux sur le panneau latéral de gauche.
        a = fond.coords('pg')
        l = self.getBateaux()
        for i in range(len(l)):
            t = l[i].getTags()
            b = fond.coords(t[0])
            d = fond.coords(t[1])
            c = int(a[3]*0.05)
            if int(b[1]) == c:
                fond.move(t[0], 0, yp*(i+1))
            if int(d[1]) == int(c*0.4):
                fond.move(t[1], 0, yp*(i+1))
            self.verifFonction()
        fond.delete('Pharos')

    def setVerif(self, fonction):
        self.verifFonction = fonction