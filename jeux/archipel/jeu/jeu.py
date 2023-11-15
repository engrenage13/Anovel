from enum import Enum, auto

class Phases(Enum):
    MISE_EN_PLACE = auto()
    PARTIE = auto()
    FIN = auto()

class Etats(Enum):
    CHARGEMENT = auto()
    EN_ATTENTE = auto()
    ERREUR = auto()

class Jeu:
    def __init__(self) -> None:
        """Crée les variables de base du jeu.
        """
        self.contenu = {}
        self.joueurs = []