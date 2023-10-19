from enum import Enum, auto

class TypeCase(Enum):
    MER = auto()
    ILE = auto()

class Case:
    def __init__(self, typeIle: TypeCase) -> None:
        self.contenu = []
        self.contenuMax = 2
        self.type = typeIle