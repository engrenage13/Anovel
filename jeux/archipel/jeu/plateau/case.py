from enum import Enum, auto

class TypeCase(Enum):
    MER = auto()
    ILE = auto()

class Case:
    def __init__(self, typeIle: TypeCase) -> None:
        self.contenu = []
        self.contenuMax = 2
        self.type = typeIle

    def check_case_pleine(self) -> bool:
        return True if (self.type == TypeCase.ILE or len(self.contenu) == self.contenuMax) else False
    
    def get_autre_bateau(self, bateau: any) -> any|bool:
        retour = False
        if bateau in self.contenu and len(self.contenu) > 1:
            i = 0
            while not retour and i < len(self.contenu):
                if self.contenu[i] != bateau:
                    retour = self.contenu[i]
                else:
                    i += 1
        return retour

    def __add__(self, element: any) -> bool:
        if len(self.contenu) < self.contenuMax:
            self.contenu.append(element)
            valide = True
        else:
            valide = False
        return valide
    
    def __sub__(self, element: any) -> bool:
        if element in self.contenu:
            del self.contenu[self.contenu.index(element)]
            valide = True
        else:
            valide = False
        return valide