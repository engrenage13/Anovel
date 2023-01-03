from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.boutonPression import BoutonPression

class Grille:
    def __init__(self, largeur: int, couleurs: list) -> None:
        """Crée une grille à boutons.
        """
        self.grille = [[]]
        self.largeur = largeur
        self.hauteur = 0
        self.espaceX = int(xf*0.003)
        self.espaceY = int(yf*0.005)
        if len(couleurs) == 0:
            couleurs = [[10, 10, 10, 190]]
        if len(couleurs) >= 2:
            self.couleurTour = couleurs[1]
        else:
            self.couleurTour = couleurs[0]
        self.couleurFond = couleurs[0]
    
    def dessine(self, x: int, y: int) -> None:
        """Dessine la grille.

        Args:
            x (int): Position x du coin gauche supérieur.
            y (int): Position y du coin gauche supérieur.
        """
        if self.couleurFond:
            draw_rectangle_rounded([x, y, self.largeur, self.hauteur], 0.1, 20, self.couleurFond)
        if self.couleurTour:
            draw_rectangle_rounded_lines([x, y, self.largeur, self.hauteur], 0.1, 20, 1, self.couleurTour)
        py = y
        if len(self.grille) > 1:
            py += self.espaceY
        for i in range(len(self.grille)):
            px = x+self.espaceX
            for j in range(len(self.grille[i])):
                bt = self.grille[i][j]
                bt.dessine(int(px+bt.getDims()[0]/2), int(py+bt.getDims()[1]/2))
                px += bt.getDims()[0] + self.espaceX
            py += bt.taille.hauteur + self.espaceY

    def ajouteElement(self, element: object, x: int, y: int) -> None:
        """Permet d'ajouter un nouvel élément à la grille.

        Args:
            element (object): Element à ajouter.
            x (int): Colonne de la grille sur la-quelle ajouter l'element.
            y (int): Ligne de la grille sur la-quelle ajouter l'element.
        """
        if type(element) in (Bouton, BoutonPression):
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
        """Modifie la hauteur de la grille et la largeur des boutons de la grille.
        """
        # Hauteur
        h = 0
        for i in range(len(self.grille)):
            h = h + self.grille[i][0].getDims()[1]
        h = h + int(self.espaceY*(len(self.grille)-1))
        if len(self.grille) > 1:
            h = h + int(self.espaceY*2)
        self.hauteur = h
        # Tailles bouton
        for i in range(len(self.grille)):
            l = self.largeur-self.espaceX*2
            cpt = 0
            if len(self.grille[i]) > 1:
                l -= self.espaceX*(len(self.grille[i])-1)
            for j in range(len(self.grille[i])):
                if not self.grille[i][j].taille.redim:
                    l -= self.grille[i][j].largeur
                else:
                    cpt += 1
            for k in range(len(self.grille[i])):
                if self.grille[i][k].taille.redim:
                    self.grille[i][k].setLargeur(int(l/cpt))