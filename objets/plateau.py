from systeme.FondMarin import *
from museeNoyee import croix, rond

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

    def dessine(self, coordonnes: tuple, taille: int, cibles: list=[]) -> None:
        """Dessine le plateau de jeu à l'écran.

        Args:
            coordonnes (tuple): "x et y" du coin en haut à gauche du plateau de jeu.
            taille (int): Taille voulu pour les cases.
            cibles (list): Liste des cases à mettre en surbrillance et la couleur à appliquer.
        """
        coo = coordonnes[:]
        y = coo[1]
        draw_rectangle_lines(coo[0]-1, y-1, int(taille*len(self.cases))+2, int(taille*len(self.cases))+2, BLACK)
        for i in range(len(self.cases)):
            x = coo[0]
            for j in range(len(self.cases[i])):
                couleur = BLACK
                epais = 1
                if len(cibles) > 1 and self.cases[i][j][0] in cibles[0]:
                    couleur = cibles[1]
                    draw_rectangle(x, y, taille, taille, [couleur[0], couleur[1], couleur[2], 50])
                    epais = 3
                draw_rectangle_lines_ex((x, y, taille, taille), epais, couleur)
                if self.cases[i][j][1] != '':
                    image = croix
                    if self.cases[i][j][1].lower() == 'o':
                        image = rond
                    draw_texture(image, x, y, WHITE)
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

    def reinitialise(self) -> None:
        """Vide le contenu des cases pour lancer une nouvelle partie.
        """
        for i in range(len(self.cases)):
            for j in range(len(self.cases[i])):
                if self.cases[i][j][1] != '':
                    self.cases[i][j][1] = ''