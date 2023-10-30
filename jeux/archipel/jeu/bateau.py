from enum import Enum, auto
from jeux.archipel.jeu.ressource import Ressource
from systeme.FondMarin import RED, BLUE, GREEN, YELLOW

class TypeBateau(Enum):
    GAFTEUR = auto()
    FERPASSEUR = auto()

class Bateau:
    def __init__(self, nom: str, vie: int, marins: int, pm: int, degats: int) -> None:
        self.nom = nom
        self.vie = Ressource(vie, RED, "")
        self.marins = Ressource(marins, BLUE, "")
        self.pm = Ressource(pm, GREEN, "")
        self.degats = Ressource(degats, YELLOW, "")
        # Autres variables
        self.position = None
        self.direction = 0
        self.est_en_jeu = False
        self.coule = False

    def get_vie(self) -> int:
        return self.vie.valeur
    
    def get_marins(self) -> int:
        return self.marins.valeur
    
    def get_pm(self) -> int:
        return self.pm.valeur
    
    def get_degats(self) -> int:
        return self.degats.valeur
    