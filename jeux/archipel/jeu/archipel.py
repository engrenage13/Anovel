from jeux.archipel.jeu.jeu import Jeu
from jeux.archipel.jeu.plateau.plateau import Plateau
from jeux.archipel.jeu.bateau import Bateau
from jeux.archipel.config import bateaux as libat, joueurs as lijo
from jeux.archipel.jeu.joueur import Joueur
from jeux.archipel.jeu.phase import Phase, TypePhase

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
        self.phases = [Phase("mise_en_place", TypePhase.MISE_EN_PLACE), [(self.contenu["plateau"], "mep")]]

    def charge_set_bateaux(self) -> list[Bateau]:
        contenuSet = ["gafteur" for i in range(3)] + ["ferpasseur"]
        liste = []
        for i in range(len(contenuSet)):
            ibat = libat[contenuSet[i]]
            liste.append(Bateau(ibat["nom"], ibat["vie"], ibat["marins"], ibat["pm"], ibat["degats"]))
        return liste