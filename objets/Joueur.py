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
        # bateaux
        nomBats = ["Porte Avion", "Croiseur", "Sous-marin 1", "Sous-marin 2", "Torpilleur"]
        tailleBats = [5, 4, 3, 3, 2]
        urlBats = 'images/bateaux/'
        for i in range(len(nomBats)):
            bat = BateauJoueur(nomBats[i], tailleBats[i], urlBats+str(tailleBats[i])+'.png', self)
            self.SetBateaux.append(bat)
        # /bateaux
        self.rejouer()

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

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.pret = False
        self.stats = [0, [0, 0], [0, 0]]
        for i in range(len(self.SetBateaux)):
            self.SetBateaux[i].rejouer()
        shuffle(self.SetBateaux)