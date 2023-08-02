class Action:
    def __init__(self, elements: list) -> None:
        self.elements = elements
        self.resultat = None

    def estFinie(self) -> bool:
        if self.resultat == None:
            return False
        else:
            return True