class Ressource:
    def __init__(self, valeur: int, icone: str, max: int = None) -> None:
        self.valeur = valeur
        self.path_icone = icone
        self.min = 0
        self.max = max

    def __add__(self, valeur: int) -> None:
        if type(self.max) == int:
            if self.valeur + valeur > self.max:
                self.valeur += (self.max-self.valeur)
            else:
                self.valeur += valeur
        else:
            self.valeur += valeur

    def __sub__(self, valeur: int) -> bool:
        if self.valeur - valeur < self.min:
            self.valeur -= (self.valeur-self.min)
            est_a_zero = True
        else:
            self.valeur -= valeur
            est_a_zero = False
        return est_a_zero
        