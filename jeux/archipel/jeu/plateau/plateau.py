from jeux.archipel.jeu.plateau.case import Case, TypeCase
from random import choice

class Plateau:
    def __init__(self, taille: int, nbIles: int) -> None:
        """Initialise le plateau de jeu.

        Args:
            taille (int): Le nombre de cases sur un côté du plateau (plateau carré).
            nbIles (int): Nombre maximal de cases pouvant être des îles.
        """
        self.taille = taille
        self.nbIles = nbIles
        self.cases = []

    def mise_en_place(self) -> None:
        """Met le plateau en place.
        """
        typIles = [type.value for type in TypeCase]
        countIle = 0
        for i in range(self.taille):
            ligne = []
            for j in range(self.taille):
                if countIle < self.nbIles:
                    typIle = choice(typIles)
                    countIle += 1
                else:
                    typIle = TypeCase.MER
                ligne.append(Case(typIle))
            self.cases.append(ligne)

    def check_case_existe(self, case: tuple[int]) -> bool:
        """Vérifie si une case existe en regardant ses coordonnées.

        Args:
            case (tuple[int]): Coordonnées de la case à vérifier.

        Returns:
            bool: True si la case a été trouvée.
        """
        existe = False
        if type(case) == tuple[int] and len(case) >= 2:
            if case[0] < self.taille and case[1] < len(self.cases[case[0]]):
                existe = True
        return existe

    def __getitem__(self, key: int) -> list[Case]|bool:
        """Renvoie la colonne de cases coorespondante à key.

        Args:
            key (int): L'indice de la colonne recherchée.

        Returns:
            list[Case]|bool: Liste de cases ou False si aucune colonne n'est associé à key.
        """
        if key < len(self.cases):
            return self.cases[key]
        else:
            return False
        
    def __len__(self) -> int:
        """Renvoie la taille de la liste des colonnes du plateau soit sa longueur.

        Returns:
            int: La longueur du plateau.
        """
        return len(self.cases)