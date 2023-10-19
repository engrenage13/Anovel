from enum import Enum, auto

class TypePhase(Enum):
    MISE_EN_PLACE = auto()
    PARTIE = auto()
    FIN = auto()

class Phase:
    def __init__(self, nom: str, typePhase: TypePhase, actions: list[tuple[object, str]]) -> None:
        self.nom = nom
        self.type = typePhase
        self.actions = actions
        self.finie = False

    def execute(self) -> None:
        pass