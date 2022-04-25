from random import *
from FondMarin import *
from objets.BateauJoueur import BateauJoueur
from objets.plateau import Plateau
from ui.notif import Notification
from Image import Ima

class Joueur():
    def __init__(self, code: int):
        """Crée un joueur (incarné par une personne).

        Args:
            code (int): L'identifiant numérique du joueur.
        """
        a = 'base' + str(code)
        f = 'cTire' + str(code)
        d = 'notifTouche' + str(code)
        e = 'notifCoule' + str(code)
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.base = Plateau(10, 10, a)
        self.cTire = Plateau(10, 10, f)
        self.SetBateaux = []
        self.pret = False
        self.stats = [0, [0, 0], [0, 0]]
        # bateaux
        nomBats = ["Porte Avion", "Croiseur", "Sous-marin n°1", "Sous-marin n°2", "Torpilleur"]
        tailleBats = [5, 4, 3, 3, 2]
        imaBats = [Ima('images/bateaux/5.png'), Ima('images/bateaux/4.png'), Ima('images/bateaux/3.png'), 
                   Ima('images/bateaux/3.png'), Ima('images/bateaux/2.png')]
        for i in range(len(nomBats)):
            bat = BateauJoueur(nomBats[i], tailleBats[i], i, imaBats[i], self)
            self.SetBateaux.append(bat)
        # /bateaux
        shuffle(self.SetBateaux)
        # notifs
        self.notifTouche = Notification("Touché !", d)
        self.notifCoule = Notification("Coulé !", e)
        # /notifs

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

    def montreBase(self) -> None:
        """Affiche le plateau d'installation du joueur.
        """
        self.base.dessine((tlatba, yf*0.105))

    def miseEnPlace(self) -> None:
        """Prépare le terrain pour que le joueur puisse positionner ses bateaux.
        """
        self.placeLat()

    def blocVert(self, bateau: BateauJoueur):
        """Déselectionne tous les bateaux sauf celui passé en paramètre.

        Args:
            bateau (BateauJoueur): Bateau à ne pas déseclectionné.
        """
        for i in range(len(self.getBateaux())):
            if bateau != self.SetBateaux[i]:
                if self.SetBateaux[i].defil:
                    self.SetBateaux[i].immobile()

    def placeLat(self):
        """Place correctement les bateaux à gauche.
        """
        plateau = [tlatba, yf]
        for i in range(len(self.getBateaux())):
            tags = self.getBateaux()[i].getTags()
            rect = fond.coords(tags[0])
            titre = fond.coords(tags[1])
            c = int(plateau[1]*0.05 + (tailleCase*0.8)/2)
            if int(rect[1]) == c:
                fond.move(tags[0], 0, yp*(i+1))
            if int(titre[1]) == int(c*0.3):
                fond.move(tags[1], 0, yp*(i+1))
        fond.delete('Pharos')

    def vigile(self):
        """Remet tous les bateaux mal positionnés, correctement en place à côté du plateau.
        """
        a = False
        l = self.getBateaux()
        for i in range(len(l)):
            t = l[i].getTags()
            b = fond.coords(t[0])
            if int(b[0]) <= int(tlatba*0.5):
                a = True
        if a:
            self.placeLat()
        else:
            fond.after(1000, self.vigile)

    def setVerif(self, fonction):
        """Paramètre la fonction de vérification avec celle passée en paramètre.

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

    def estToucheBateau(self, case: str) -> list:
        """Vérifie si l'un des bateaux du joueur est touché.

        Args:
            case (str): Case à comparer.

        Returns:
            list: Une liste composé d'un booléen, ainsi que l'indice du bateau touché dans la liste du joueur.
        """
        a = False
        i = 0
        while i < len(self.SetBateaux) and not a:
            a = self.SetBateaux[i].estTouche(case)
            i = i + 1
        return [a, i-1]

    def aPerdu(self) -> bool:
        """Vérifie si le joueur a encore des bateaux non-coulés.

        Returns:
            bool: True si tous les bateaux du joueur ont coulés.
        """
        a = True
        i = 0
        while i < len(self.SetBateaux) and a:
            if not self.SetBateaux[i].estCoule():
                a = False
            i = i + 1
        return a