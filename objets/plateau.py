from xml.dom import InvalidCharacterErr
from FondMarin import *

class Plateau:
    def __init__(self, x: int, y: int, idtag: str) -> None:
        """Crée un plateau de jeu.

        Args:
            x (int): Nombre de cases dans la longueur.
            y (int): Nombre de cases dans la hauteur.
            idtag (str): Tag du plateau (permet de l'identifier).
        """
        self.taille = yf*0.84/x
        self.identifiant = idtag
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.cases = []
        for i in range(y):
            ligne = []
            for j in range(x):
                quadrillage = self.alphabet[i] + str(j+1) + idtag[0] + idtag[len(idtag)-1]
                image = 'i' + quadrillage
                case = [quadrillage, image]
                ligne.append(case)
            self.cases.append(ligne)

    def dessine(self, coordonnes: tuple) -> None:
        """Dessine le plateau de jeu à l'écran.

        Args:
            coordonnes (tuple): "x et y" du coin en haut à gauche du plateau de jeu.
        """
        coo = coordonnes[:]
        y = coo[1]
        for i in range(len(self.cases)):
            x = coo[0]
            for j in range(len(self.cases[i])):
                fond.create_rectangle(x, y, x+self.taille, y+self.taille, fill='', 
                                      tags=(self.cases[i][j][0], self.identifiant, 'plateau'))
                fond.create_image(x+self.taille/2, y+self.taille/2, image='', 
                                  tags=(self.cases[i][j][1], self.identifiant, 'plateau'))
                x = x + self.taille
            y = y + self.taille

    def efface(self) -> None:
        """Efface le(s) plateau(x) affiché(s).
        """
        fond.delete(self.identifiant)

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
            raise InvalidCharacterErr("Ce caractère est incompatible.")
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
            raise InvalidCharacterErr("Ce caractère est incompatible.")
        elif nombre > self.getDimensions()[0] or nombre < 1:
            raise IndexError("Le plateau ne possède pas de colonne identifiée par ce nombre.")
        else:
            indice = nombre - 1
            colonne = []
            for i in range(self.getDimensions()[0]):
                colonne.append(self.cases[i][indice][0])
            return colonne

    def deplace(self, horizontal: float, vertical: float) -> None:
        """Déplace le plateau dans la direction souhaité.

        Args:
            horizontal (float): Nombre de pixel à parcourir vers la droite ou la gauche.
            vertical (float): Nombre de pixel à parcourir vers le haut ou le bas.
        """
        fond.move(self.identifiant, horizontal, vertical)