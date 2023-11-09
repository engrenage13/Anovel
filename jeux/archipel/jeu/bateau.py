from enum import Enum, auto
from jeux.archipel.jeu.ressource import Ressource

class TypeBateau(Enum):
    GAFTEUR = auto()
    FERPASSEUR = auto()

class Bateau:
    def __init__(self, nom: str, vie: int, marins: int, pm: int, degats: int, portee: int) -> None:
        self.nom = nom
        self.vie = Ressource(vie, "")
        self.marins = Ressource(marins, "")
        self.pm = Ressource(pm, "")
        self.degats = Ressource(degats, "")
        self.portee = portee
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
    
    def __add__(self, valeur: int) -> None:
        self.vie + valeur

    def __sub__(self, valeur: int) -> bool:
        mort = self.vie - valeur
        if mort:
            self.coule = True
        return mort
    