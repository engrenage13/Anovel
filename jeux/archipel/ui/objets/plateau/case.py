import os
import random
from systeme.FondMarin import *
from jeux.archipel.fonctions.bases import TAILLECASE
from jeux.archipel.ui.objets.Bateau import Bateau
from jeux.archipel.ui.objets.bases.bougeable import Bougeable
from jeux.archipel.ui.chargeIles import chargeSegment
from jeux.archipel.jeu.plateau.case import Case as C, TypeCase

class Case(Bougeable, C):
    """Une case est une portion du plateau.
    """
    def __init__(self, x: int = 0, y: int = 0, taille: int = TAILLECASE, couleur: Color = WHITE, type_case: TypeCase = TypeCase.MER) -> None:
        """Crée une case du plateau.

        Args:
            x (int, optional): Abscisse du coin supérieur gauche de la case. Defaults to 0.
            y (int, optional): Ordonnée du coin supérieur gauche de la case. Defaults to 0.
            taille (int, optional): La taille de la case. Defaults to TAILLECASE.
            couleur (Color, optional): Couleur de la case. Defaults to WHITE.
            type_case (TypeCase, optional): Type de la case. Defaults to MER.
        """
        Bougeable.__init__(self, x, y)
        C.__init__(self, type_case)
        self.taille = taille
        self.couleur = couleur
        self.image = None
        # Mer
        if self.type == TypeCase.MER:
            self.charge_mer()

    def dessine(self, grise: bool = False) -> None:
        """Dessine la case à l'écran.

        Args:
            grise (bool, optional): Permet d'appliquer un altérant qui va griser la case. Defaults to False.
        """
        if self.image != None:
            draw_texture(self.mer, self.pos[0], self.pos[1], WHITE)
        else:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleur)
        if grise:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [50, 50, 50, 160])
        
    def dessineContenu(self, actif: any|bool = False) -> None:
        """Dessine le contenu de la case si elle en a.
        """
        if len(self.contenu) > 0:
            if actif and actif in self.contenu:
                lum1 = self.contenu.index(actif) == 0
                lum2 = self.contenu.index(actif) == 1
            else:
                lum1, lum2 = False
            ecart = int(self.taille*0.035)
            if len(self.contenu) == 2:
                if self.contenu[0].direction%2 == 0:
                    largeur = int(self.taille-ecart*2)
                    hauteur = int(self.taille/2-ecart*2)
                    if lum1 or self.contenu[0].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                    self.contenu[0].dessine()
                    if lum2 or self.contenu[1].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+self.taille/2+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[1].couleur)
                    self.contenu[1].dessine()
                else:
                    largeur = int(self.taille/2-ecart*2)
                    hauteur = int(self.taille-ecart*2)
                    if lum1 or self.contenu[0].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                    self.contenu[0].dessine()
                    if lum2 or self.contenu[1].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+self.taille/2+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[1].couleur)
                    self.contenu[1].dessine()
            else:
                largeur = int(self.taille-ecart*2)
                hauteur = int(self.taille-ecart*2)
                if lum1 or self.contenu[0].getContact():
                    draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                self.contenu[0].dessine()

    def charge_mer(self) -> None:
        """Charge l'image de la mer.
        """
        mer = load_image("jeux/archipel/images/mer.png")
        image_resize(mer, self.taille, self.taille)
        self.image = load_texture_from_image(mer)
        unload_image(mer)

    def setPos(self, x: int, y: int) -> None:
        """Modifie la position de la case.

        Args:
            x (int): Nouvel abscisse du coin supérieur gauche de la case.
            y (int): Nouvel ordonnée du coin supérieur gauche de la case.
        """
        super().setPos(x, y)
        if len(self.contenu) > 0:
            if len(self.contenu) == 1:
                self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/2))
            else:
                if self.contenu[0].direction%2 == 0:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/4))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/4*3))
                else:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/4), int(self.pos[1]+self.taille/2))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/4*3), int(self.pos[1]+self.taille/2))
        
    def getContact(self) -> bool:
        """Vérifie si le curseur est sur la case.

        Returns:
            bool: True si le curseur est sur la case.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.pos[0] and x <= self.pos[0]+self.taille:
            if y >= self.pos[1] and y <= self.pos[1]+self.taille:
                rep = True
        return rep
    
    def tourneBateaux(self, sens: bool = True) -> None:
        """Permet de tourner tous les bateaux presants sur la case.

        Args:
            sens (bool, optional): True : Antihoraire, False: Horaire. Defaults to True.
        """
        for i in range(len(self.contenu)):
            if sens:
                self.contenu[i].gauche()
            else:
                self.contenu[i].droite()
        self.setPos(self.pos[0], self.pos[1])

    def rejouer(self) -> None:
        """Réinitialise les principaux paramètres de la case pour recommencer une partie.
        """
        if len(self.contenu) > 0:
            self.vide()
        if self.type == TypeCase.ILE:
            self.type = TypeCase.MER
            self.charge_mer()