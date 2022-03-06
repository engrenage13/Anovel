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
        self.stats = [0, [0, 0], [0, 0]]
        # bateaux
        for i in range(len(b)):
            bat = Bateau(b[i], c[i], i, self)
            self.SetBateaux.append(bat)
        # /bateaux
        shuffle(self.SetBateaux)

    def getBateaux(self) -> list:
        """Retourne la liste des bateaux du joueur.

        Returns:
            list: Liste des bateaux
        """
        return self.SetBateaux

    def getId(self) -> int:
        """Retourne l'identifiant du joueur

        Returns:
            int: identifiant du joueur.
        """
        return self.id

    def getNom(self) -> str:
        """Retourne le nom du joueur.

        Returns:
            str: nom du joueur
        """
        return self.nom

    def getStats(self) -> list:
        """Retourne la liste des statistiques du joueur.

        Returns:
            list: Liste des statistiques individuelles.
        """
        return self.stats

    def dessineBateaux(self) -> None:
        """Dessine tous les bateaux du joueur.
        """
        for i in range(len(self.SetBateaux)):
            self.SetBateaux[i].dessine(self.id)

    def montreBase(self) -> None:
        """Affiche le plateau d'installation du joueur.
        """
        fond.itemconfigure('base' + str(self.id), state='normal')

    def miseEnPlace(self) -> None:
        """Prépare le terrain pour que le joueur puisse positionner ses bateaux.
        """
        self.montreBase()
        self.dessineBateaux()
        self.placeLat()

    def blocVert(self, bateau: object):
        """Déselectionne tous les bateaux sauf celui passé en paramètre.

        Args:
            bateau (object): Bateau à ne pas déseclectionné.
        """
        for i in range(len(self.getBateaux())):
            if bateau != self.SetBateaux[i]:
                if self.SetBateaux[i].defil:
                    self.SetBateaux[i].immobile()

    def vigile(self):
        """Remet tout les bateaux mal positionnés, coorectement en place à côté du plateau.
        """
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

    def placeLat(self):
        """Place les bateaux sur le panneau latéral de gauche.
        """
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
        """Paramètre la foction de vérification avec celle passée en paramètre.

        Args:
            fonction (_type_): Le vérificateur
        """
        self.verifFonction = fonction

    def toucheCase(self, case: bool) -> None:
        """Incrémente le compteur de case touchées.
        """
        self.stats[0] = self.stats[0] + 1
        if case:
            self.stats[1][0] = self.stats[1][0] + 1
        else:
            self.stats[2][0] = self.stats[2][0] + 1
        self.stats[1][1] = round(self.stats[1][0]*100/self.stats[0], 1)
        self.stats[2][1] = round(self.stats[2][0]*100/self.stats[0], 1)