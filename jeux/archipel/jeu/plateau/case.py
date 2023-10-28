from enum import Enum, auto

class TypeCase(Enum):
    MER = auto()
    ILE = auto()

class Case:
    def __init__(self, typeIle: TypeCase) -> None:
        self.contenu = []
        self.contenuMax = 2
        self.type = typeIle

    def __add__(self, element: any) -> bool:
        if len(self.contenu) < self.contenuMax:
            self.contenu.append(element)
            valide = True
        else:
            valide = False
        return valide