from jeux.archipel.jeu.jeu import Jeu
from jeux.archipel.jeu.plateau.plateau import Plateau
from jeux.archipel.jeu.bateau import Bateau
from jeux.archipel.config import bateaux as libat, joueurs as lijo
from jeux.archipel.jeu.joueur import Joueur

class Archipel(Jeu):
    def __init__(self, plateau: tuple[int, float]) -> None:
        super().__init__()
        self.contenu = {
            "plateau": Plateau(plateau[0], int(plateau[0]*plateau[0]*plateau[1])),
            "bateaux": {
                "set1": self.charge_set_bateaux(),
                "set2": self.charge_set_bateaux(),
            }
        }
        for i in range(len(lijo)):
            joueur = lijo[i]
            self.joueurs.append(Joueur(joueur["nom"], self.contenu["bateaux"][i]))
        # Phases
        mise_en_place = [self.contenu["plateau"].mise_en_place]
        partie = []
        fin_de_partie = []
        self.phases = [mise_en_place, partie, fin_de_partie]

    def charge_set_bateaux(self) -> list[Bateau]:
        contenuSet = ["gafteur" for i in range(3)] + ["ferpasseur"]
        liste = []
        for i in range(len(contenuSet)):
            ibat = libat[contenuSet[i]]
            liste.append(Bateau(ibat["nom"], ibat["vie"], ibat["marins"], ibat["pm"], ibat["degats"]))
        return liste
    
    def place_bateau(self, joueur: Joueur|int, bateau: Bateau|int, case: tuple[int]) -> None:
        ok_joueur = True if type(joueur) == Joueur else False
        if type(joueur) == int:
            joueur = self.joueurs[self.joueurs.index(joueur)]
            ok_joueur = True
        if ok_joueur:
            ok_bateau = True if type(bateau) == Bateau else False
            if type(bateau) == int:
                bateau = joueur[bateau]
                ok_bateau = True
            if ok_bateau:
                if type(case) == tuple[int] and len(case) >= 2:
                    case_plateau = self.contenu["plateau"][case[0]][case[1]]
                    bateau.position = case
                    case_plateau + bateau
                    bateau.est_en_place = True