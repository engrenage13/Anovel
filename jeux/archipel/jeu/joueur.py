from jeux.archipel.jeu.bateau import Bateau

class Joueur:
    def __init__(self, nom: str, bateaux: list[Bateau]) -> None:
        self.nom = nom
        self.bateaux = bateaux

    def copie_joueur(self, bateaux: list[Bateau] = None) -> object:
        if bateaux == None or len(bateaux) == 0:
            bats = self.bateaux
        else:
            bats = bateaux
        return Joueur(self.nom, bats)
