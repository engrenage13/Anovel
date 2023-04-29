from systeme.FondMarin import *
from jeux.Jeu_1.objets.bases.pivote import Pivote
from jeux.Jeu_1.fonctions.deplacement import glisse

class Bateau(Pivote):
    def __init__(self, image: str, pv: int, marins: int, pm: int):
        """Crée un bateau.

        Args:
            image (str): Chemin d'accès à l'image du bateau.
            pv (int): Points de vie du bateau.
            marins (int): Nombre de marins présents sur le bateau.
            pm (int): Portée de déplacement du bateau.
        """
        super().__init__(image)
        # Valeurs initiales
        self.pvi = pv
        self.marinsi = marins
        self.pmi = pm
        self.rejouer()

    def dessine(self) -> None:
        """Dessine le bateau.
        """
        super().dessine()

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du bateau pour rejouer une nouvelle partie.
        """
        self.pos = []
        self.place = False
        self.coule = False
        self.actif = False
        self.vie = self.pvi
        self.marins = self.marinsi
        self.pm = self.pmi