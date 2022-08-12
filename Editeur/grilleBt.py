from systeme.FondMarin import *
from ui.bouton import Bouton
from ui.ptiBouton import PtiBouton

class GrilleBt:
    def __init__(self) -> None:
        """Crée une grille à boutons.
        """
        self.grille = [[]]
        self.largeur = 0
        self.hauteur = 0
        self.espaceX = int(tlatba*0.06)
        self.espaceY = int(yf*0.05)
    
    def dessine(self, x: int, y: int, important: list) -> None:
        """Dessine la grille.

        Args:
            x (int): Position x du coin gauche supérieur.
            y (int): Position y du coin gauche supérieur.
            important (list): Liste de booléens pour l'option important de chacun des boutons.
        """
        draw_rectangle_rounded([x, y, self.largeur, self.hauteur], 0.2, 30, [255, 255, 255, 50])
        draw_rectangle_rounded_lines([x, y, self.largeur, self.hauteur], 0.2, 30, 3, WHITE)
        py = y + self.hauteur - int(yf*0.02)
        k = 0
        for i in range(len(self.grille)):
            px = x + self.largeur - int(tlatba*0.05)
            if len(self.grille[i]) == 1:
                actif = important[len(important)-1-k]
                k = k + 1
                telem = self.grille[i][0].getDims()
                if type(self.grille[i][0]) == PtiBouton:
                    self.grille[i][0].dessine((x+int(self.largeur/2), py-int(telem[1]/2)), actif)
                elif type(self.grille[i][0]) == Bouton:
                    self.grille[i][0].dessine((x+int(self.largeur/2), py-int(telem[1]/2)), True, actif)
            else:
                for j in range(len(self.grille[i])):
                    actif = important[len(important)-1-k]
                    k = k + 1
                    telem = self.grille[i][j].getDims()
                    if type(self.grille[i][j]) == PtiBouton:
                        self.grille[i][j].dessine((px-int(telem[0]/2), py-int(telem[1]/2)), actif)
                    elif type(self.grille[i][j]) == Bouton:
                        self.grille[i][j].dessine((px-int(telem[0]/2), py-int(telem[1]/2)), True, actif)
                    px -= telem[0] + self.espaceX
            py -= telem[1] + self.espaceY

    def ajouteElement(self, element: object, x: int, y: int) -> None:
        """Permet d'ajouter un nouvel élément à la grille.

        Args:
            element (object): Element à ajouter.
            x (int): Colonne de la grille sur la-quelle ajouter l'element.
            y (int): Ligne de la grille sur la-quelle ajouter l'element.
        """
        if type(element) in [Bouton, PtiBouton]:
            if y < len(self.grille):
                ligne = self.grille[y]
                if x <= 0:
                    self.grille[y] = [element] + ligne
                else:
                    self.grille[y].append(element)
            else:
                self.grille.append([element])
            self.setDims()

    def setDims(self) -> None:
        """Modifie les dimensions de la grille pour qu'elle s'adapte à son contenu.
        """
        l = 0
        h = 0
        ligne = 0
        g = len(self.grille[0])
        for i in range(len(self.grille)):
            if g < len(self.grille[i]):
                g = len(self.grille[i])
                ligne = i
        for i in range(g):
            taille = self.grille[ligne][i].getDims()
            l = l + taille[0]
        l = l + int(self.espaceX*(g-1)+tlatba*0.05*2)
        for i in range(len(self.grille)):
            taille = self.grille[i][0].getDims()
            h = h + taille[1]
        h = h + int(yf*0.02*2+self.espaceY*(len(self.grille)-1))
        self.largeur = l
        self.hauteur = h