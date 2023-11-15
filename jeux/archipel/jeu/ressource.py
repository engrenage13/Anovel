class Ressource:
    def __init__(self, valeur: int, icone: str, max: int = None) -> None:
        """Crée une ressource.

        Args:
            valeur (int): Valeur initiale de la ressource.
            icone (str): Nom du fichier d'image utilisé pour illustrer la ressource.
            max (int, optional): La valeur maximale de la ressource. Defaults to None.
        """
        self.valeur = valeur
        self.path_icone = icone
        self.min = 0
        self.max = max

    def __add__(self, valeur: int) -> None:
        """Augmente la valeur de la ressource d'un nombre passé en paramètre (plafonné au max s'il est définit).

        Args:
            valeur (int): De combien on augmente.
        """
        if type(self.max) == int:
            if self.valeur + valeur > self.max:
                self.valeur += (self.max-self.valeur)
            else:
                self.valeur += valeur
        else:
            self.valeur += valeur

    def __sub__(self, valeur: int) -> bool:
        """Diminue la valeur de la ressource d'un nombre pramètrable (Limité à 0).

        Args:
            valeur (int): Nombre à soustraire à la valeur de la ressource.

        Returns:
            bool: True si la valeur atteint 0, False dans le cas contraire.
        """
        if self.valeur - valeur < self.min:
            self.valeur -= (self.valeur-self.min)
        else:
            self.valeur -= valeur
        if self.valeur == 0:
            est_a_zero = True
        else:
            est_a_zero = False
        return est_a_zero
        