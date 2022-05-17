from random import *
from systeme.FondMarin import *
from objets.BateauJoueur import BateauJoueur

class Joueur():
    def __init__(self, code: int):
        """Crée un joueur (incarné par une personne).

        Args:
            code (int): L'identifiant numérique du joueur.
        """
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.SetBateaux = []
        self.pret = False
        self.stats = [0, [0, 0], [0, 0]]
        # bateaux
        nomBats = ["Porte Avion", "Croiseur", "Sous-marin 1", "Sous-marin 2", "Torpilleur"]
        tailleBats = [5, 4, 3, 3, 2]
        urlBats = 'images/bateaux/'
        for i in range(len(nomBats)):
            bat = BateauJoueur(nomBats[i], tailleBats[i], urlBats+str(tailleBats[i])+'.png', self)
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