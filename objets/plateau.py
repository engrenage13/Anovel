from systeme.FondMarin import *

class Plateau:
    def __init__(self, x: int, y: int) -> None:
        """Crée un plateau de jeu.

        Args:
            x (int): Nombre de cases dans la longueur.
            y (int): Nombre de cases dans la hauteur.
        """
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.cases = []
        for i in range(y):
            ligne = []
            for j in range(x):
                quadrillage = self.alphabet[i] + str(j+1)
                case = [quadrillage, '']
                ligne.append(case)
            self.cases.append(ligne)

    def dessine(self, coordonnes: tuple, taille: int) -> None:
        """Dessine le plateau de jeu à l'écran.

        Args:
            coordonnes (tuple): "x et y" du coin en haut à gauche du plateau de jeu.
        """
        coo = coordonnes[:]
        y = coo[1]
        draw_rectangle_lines(coo[0]-1, y-1, int(taille*len(self.cases))+2, int(taille*len(self.cases))+2, BLACK)
        for i in range(len(self.cases)):
            x = coo[0]
            for j in range(len(self.cases[i])):
                draw_rectangle_lines(x, y, taille, taille, BLACK)
                x = x + taille
            y = y + taille

    def getDimensions(self) -> tuple:
        """Renvoie les dimensions du plateau.

        Returns:
            tuple: horizontal x vertical.
        """
        return (len(self.cases), len(self.cases[0]))

    def getLigne(self, lettre: str) -> list:
        """Renvoie la ligne identifié par la lettre voulue.

        Args:
            lettre (str): Idetifiant de la ligne recherchée.

        Raises:
            InvalidCharacterErr: Le caractère ne fait pas partie de l'alphabet.
            IndexError: La lettre n'est attribué à aucune ligne.

        Returns:
            list: Liste des tags des cases de la ligne.
        """
        if lettre.upper() not in self.alphabet:
            raise IndexError("Ce caractère ne fait pas partie de l'alphabet lié au plateau.")
        elif lettre.upper() not in self.alphabet[0:self.getDimensions()[0]]:
            raise IndexError("Le plateau ne possède pas de ligne identifiée par cette lettre.")
        else:
            indice = self.alphabet.index(lettre.upper())
            ligne = []
            for i in range(self.getDimensions()[1]):
                ligne.append(self.cases[indice][i][0])
            return ligne

    def getColonne(self, nombre: int) -> list:
        """Renvoie la colonne identifié par le nombre passé en paramètre.

        Args:
            nombre (int): L'indentifiant de la colonne recherchée.

        Raises:
            InvalidCharacterErr: Le caractère n'est pas un nombre.
            IndexError: Ce nombre n'est attribué à aucune colonne.

        Returns:
            list: Liste des tags des cases de la colonne.
        """
        if type(nombre) != int:
            raise IndexError("Il semble que cette chaîne comporte des valeurs qui ne sont pas des entiers.")
        elif nombre > self.getDimensions()[0] or nombre < 1:
            raise IndexError("Le plateau ne possède pas de colonne identifiée par ce nombre.")
        else:
            indice = nombre - 1
            colonne = []
            for i in range(self.getDimensions()[0]):
                colonne.append(self.cases[i][indice][0])
            return colonne