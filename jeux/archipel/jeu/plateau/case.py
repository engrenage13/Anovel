from enum import Enum, auto

class TypeCase(Enum):
    MER = auto()
    ILE = auto()

class Case:
    def __init__(self, typeIle: TypeCase) -> None:
        """Crée une case du plateau.

        Args:
            typeIle (TypeCase): Type de case (MER ou ILE).
        """
        self.contenu = []
        self.contenuMax = 2
        self.type = typeIle

    def check_case_pleine(self) -> bool:
        """Vérifie si la case est pleine.

        Returns:
            bool: True si aucun bateau ne peut être posé sur cette case ou False dans le cas contraire.
        """
        return (self.type == TypeCase.ILE or len(self.contenu) == self.contenuMax)
    
    def get_autre_bateau(self, bateau: any) -> object|bool:
        """Renvoie le deuxième bateau que contient la case par rapport à celui passé en paramètres

        Args:
            bateau (Bateau): Le bateau que l'on ne cherche pas.

        Returns:
            bateau|bool: Le deuxième bateau ou False s'il n'y en a pas.
        """
        retour = False
        if bateau in self.contenu and len(self.contenu) > 1:
            i = 0
            while not retour and i < len(self.contenu):
                if self.contenu[i] != bateau:
                    retour = self.contenu[i]
                else:
                    i += 1
        return retour
    
    def vide(self) -> None:
        """Vide le contenu de la case.
        """
        while len(self.contenu) > 0:
            self - self.contenu[0]

    def __getitem__(self, key: int) -> object|bool:
        """Renvoie l'élément situé à l'indice key.

        Args:
            key (int): Indice de l'élément recherché.

        Returns:
            object|bool: Element contenu dans la case s'il l'indice existe ou False dans le cas contraire.
        """
        if key < len(self.contenu):
            return self.contenu[key]
        else:
            return False
        
    def __len__(self) -> int:
        """Retourne le nombre d'éléments présents sur la case.

        Returns:
            int: Nombre d'éléments présents sur la case.
        """
        return len(self.contenu)

    def __add__(self, element: any) -> bool:
        """Ajoute un élément sur cette case.

        Args:
            element (any): L'élément à ajouter.

        Returns:
            bool: True si l'élément a été ajouté, sinon False.
        """
        if len(self.contenu) < self.contenuMax:
            self.contenu.append(element)
            valide = True
        else:
            valide = False
        return valide
    
    def __sub__(self, element: any) -> bool:
        """Retire un élément de la case.

        Args:
            element (any): L'élément à retirer.

        Returns:
            bool: True s'il a été trouvé et retirer, False dans le cas contraire.
        """
        if element in self.contenu:
            del self.contenu[self.contenu.index(element)]
            valide = True
        else:
            valide = False
        return valide