from enum import Enum, auto
from jeux.archipel.jeu.ressource import Ressource

class TypeBateau(Enum):
    GAFTEUR = auto()
    FERPASSEUR = auto()

class Bateau:
    def __init__(self, nom: str, vie: int, marins: int, pm: int, degats: int, portee: int) -> None:
        """Crée un bateau.

        Args:
            nom (str): Le nom du bateau.
            vie (int): La vie du bateau.
            marins (int): Le nombre de marins du bateau.
            pm (int): La distance maximale que peut parcourir le bateau en un déplacement.
            degats (int): Les dégâts qu'inflige le bateau lorsqu'il attaque.
            portee (int): La portée maximale des attaques du bateau.
        """
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
        # Sauvegarde
        self.sauvegarde = {"vie": vie, "marins": marins, "pm": pm, "degats": degats}

    def reinitialise(self) -> None:
        """Réinitialise la valeur des ressources
        """
        self.vie.valeur = self.sauvegarde["vie"]
        self.marins.valeur = self.sauvegarde["marins"]
        #self.pm.valeur = self.sauvegarde["pm"]
        #self.degats = self.sauvegarde["degats"]

    def get_vie(self) -> int:
        """Renvoie le nombre de PV actuel du bateau.

        Returns:
            int: PV du bateau.
        """
        return self.vie.valeur
    
    def get_marins(self) -> int:
        """Renvoie le nombre de marins présents sur le bateau.

        Returns:
            int: Nombre de marins du bateau.
        """
        return self.marins.valeur
    
    def get_pm(self) -> int:
        """Renvoie le nombre de PM du bateau.

        Returns:
            int: PM du bateau.
        """
        return self.pm.valeur
    
    def get_degats(self) -> int:
        """Renvoie les dégâts qu'inflige le bateau.

        Returns:
            int: Les dégâts du bateau.
        """
        return self.degats.valeur
    
    def __add__(self, valeur: int) -> None:
        """Ajoute des PV au bateau.

        Args:
            valeur (int): Nombre de PV à ajouter.
        """
        self.vie + valeur

    def __sub__(self, valeur: int) -> bool:
        """Retire des PV au bateau.

        Args:
            valeur (int): Nombre de PV à retirer.

        Returns:
            bool: True si le bateau a coulé, False dans le cas contraire.
        """
        mort = self.vie - valeur
        if mort:
            self.coule = True
        return mort
    