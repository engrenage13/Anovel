from random import randint
from FondMarin import fond

class Paillette:
    def __init__(self, id: int) -> None:
        self.id = 'paillette'+str(id)
        self.etat = False
        self.taille = 0

    def getEtat(self) -> bool:
        """Renvoie l'état de la paillette.

        Returns:
            bool: True pour dire qu'elle existe à l'écran et False, le contraire.
        """
        return self.etat

    def dessine(self, x: int, y: int, couleur: str) -> None:
        """Dessine la paillette à l'écran.

        Args:
            x (int): Position en abcisse de la paillette, à l'écran.
            y (int): Position en ordonnée de la paillette, à l'écran.
            couleur (str): Couleur à aapliqué à la paillette.
        """
        self.max = randint(10, 25)
        fond.create_rectangle(x, y, x, y, fill=couleur, tags=('paillette', self.id))
        fond.tag_lower(self.id, 'plafDec')
        self.etat = True
        fond.after(500, self.grossi)

    def grossi(self) -> None:
        """Fait grossir la paillette un certain nombre de fois (aléatoire).
        """
        if self.taille < self.max:
            c = fond.coords(self.id)
            fond.coords(self.id, c[0]-1, c[1]-1, c[2]+1, c[3]+1)
            self.taille = self.taille + 1
            fond.after(10, self.grossi)
        else:
            self.taille = 0
            fond.after(1000, self.retreci)

    def retreci(self) -> None:
        """Fait rétrécir la paillette jusqu'à ce qu'elle soit minuscule, puis la détruit.
        """
        if self.taille < self.max:
            c = fond.coords(self.id)
            fond.coords(self.id, c[0]+1, c[1]+1, c[2]-1, c[3]-1)
            self.taille = self.taille + 1
            fond.after(10, self.retreci)
        else:
            self.etat = False
            self.taille = 0
            fond.delete(self.id)