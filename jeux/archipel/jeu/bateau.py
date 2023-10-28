from enum import Enum, auto

class TypeBateau(Enum):
    GAFTEUR = auto()
    FERPASSEUR = auto()

class Bateau:
    def __init__(self, nom: str, vie: int, marins: int, pm: int, degats: int) -> None:
        self.nom = nom
        self.vie = vie
        self.marins = marins
        self.pm = pm
        self.degats = degats
        # Autres variables
        self.position = None
        self.est_en_place = False