import os
import random
from systeme.FondMarin import *
from jeux.archipel.fonctions.bases import TAILLECASE
from jeux.archipel.objets.Bateau import Bateau
from jeux.archipel.objets.bases.bougeable import Bougeable
from jeux.archipel.chargeIles import chargeSegment

class Case(Bougeable):
    """Une case est une portion du plateau.

    Args:
        Bougeable (Bougeable): La case est déplaçable.
    """
    def __init__(self, x: int = 0, y: int = 0, taille: int = TAILLECASE, couleurs: tuple[Color] = (WHITE, BLACK), bordure: float = 1.5) -> None:
        """Crée une case du plateau.

        Args:
            x (int, optional): Abscisse du coin supérieur gauche de la case. Defaults to 0.
            y (int, optional): Ordonnée du coin supérieur gauche de la case. Defaults to 0.
            taille (int, optional): La taille de la case. Defaults to TAILLECASE.
            couleurs (tuple[Color], optional): [Couleur de l'intérieur de la case, couleur de la bordure]. Defaults to (WHITE, BLACK).
            bordure (float, optional): Epaisseur de la bordure. Defaults to 1.5.
        """
        super().__init__(x, y)
        self.taille = taille
        self.couleurs = couleurs
        self.largeurBordure = bordure
        self.contenu = []
        # Iles
        self.typeIle = -1
        self.orienteIle = 0
        self.imaIle = None
        self.marqueur = False

    def dessine(self, grise: bool = False) -> None:
        """Dessine la case à l'écran.

        Args:
            grise (bool, optional): Permet d'appliquer un déformateur grisant la case. Defaults to False.
        """
        if not self.marqueur:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleurs[0])
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], self.largeurBordure, self.couleurs[1])
        if self.marqueur:
            if self.couleurs == ([0, 0, 0, 150], BLACK):
                draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [65, 150, 39, 150])
            else:
                draw_texture(self.imaIle, self.pos[0], self.pos[1], WHITE)
        if grise:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [50, 50, 50, 160])

    def dessineMarqueur(self, x: int, y: int, id: int|str, couleur: Color) -> None:
        """Dessine l'identifiant du bateau présent sur la case.

        Args:
            x (int): Abscisse du coin supérieur gauche du marqueur.
            y (int): Ordonnée du coin supérieur gauche du marqueur.
            id (int | str): L'indentifiant du bateau.
            couleur (Color): La couleur du marqueur.
        """
        t = int(self.taille*0.1)
        draw_rectangle_rounded([x, y, t, t], 0.3, 360, couleur)
        draw_text_ex(police1, str(id), (int(x+0.028*self.taille), int(y+0.005*self.taille)), 23, 0, WHITE)
        
    def dessineContenu(self) -> None:
        """Dessine le contenu de la case si elle en a.
        """
        if len(self.contenu) > 0:
            ecart = int(self.taille*0.035)
            tMarqueur = int(self.taille*0.1)
            if len(self.contenu) == 2:
                if self.contenu[0].direction%2 == 0:
                    largeur = int(self.taille-ecart*2)
                    hauteur = int(self.taille/2-ecart*2)
                    if self.contenu[0].actif or self.contenu[0].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                        self.dessineMarqueur(int(self.pos[0]+ecart+largeur-tMarqueur), int(self.pos[1]+ecart+hauteur-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                    else:
                        self.dessineMarqueur(int(self.pos[0]+self.taille-tMarqueur), int(self.pos[1]+self.taille/2-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                    self.contenu[0].dessine()
                    if self.contenu[1].actif or self.contenu[1].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+self.taille/2+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[1].couleur)
                        self.dessineMarqueur(int(self.pos[0]+ecart+largeur-tMarqueur), int(self.pos[1]+self.taille/2+ecart+hauteur-tMarqueur), self.contenu[1].id, self.contenu[1].couleur)
                    else:
                        self.dessineMarqueur(int(self.pos[0]+self.taille-tMarqueur), int(self.pos[1]+self.taille-tMarqueur), self.contenu[1].id, self.contenu[1].couleur)
                    self.contenu[1].dessine()
                else:
                    largeur = int(self.taille/2-ecart*2)
                    hauteur = int(self.taille-ecart*2)
                    if self.contenu[0].actif or self.contenu[0].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                        self.dessineMarqueur(int(self.pos[0]+ecart+largeur-tMarqueur), int(self.pos[1]+ecart+hauteur-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                    else:
                        self.dessineMarqueur(int(self.pos[0]+self.taille/2-tMarqueur), int(self.pos[1]+self.taille-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                    self.contenu[0].dessine()
                    if self.contenu[1].actif or self.contenu[1].getContact():
                        draw_rectangle_rounded_lines([int(self.pos[0]+self.taille/2+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[1].couleur)
                        self.dessineMarqueur(int(self.pos[0]+ecart+self.taille/2+largeur-tMarqueur), int(self.pos[1]+ecart+hauteur-tMarqueur), self.contenu[1].id, self.contenu[1].couleur)
                    else:
                        self.dessineMarqueur(int(self.pos[0]+self.taille-tMarqueur), int(self.pos[1]+self.taille-tMarqueur), self.contenu[1].id, self.contenu[1].couleur)
                    self.contenu[1].dessine()
            else:
                largeur = int(self.taille-ecart*2)
                hauteur = int(self.taille-ecart*2)
                if self.contenu[0].actif or self.contenu[0].getContact():
                    draw_rectangle_rounded_lines([int(self.pos[0]+ecart), int(self.pos[1]+ecart), largeur, hauteur], 0.15, 330, 5, self.contenu[0].couleur)
                    self.dessineMarqueur(int(self.pos[0]+ecart+largeur-tMarqueur), int(self.pos[1]+ecart+hauteur-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                else:
                    self.dessineMarqueur(int(self.pos[0]+self.taille-tMarqueur), int(self.pos[1]+self.taille-tMarqueur), self.contenu[0].id, self.contenu[0].couleur)
                self.contenu[0].dessine()

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

    def retire(self, element: Bateau) -> bool:
        """Retire un élément de la case.

        Args:
            element (Bateau): L'élément à retirer.

        Returns:
            bool: True si l'élément était sur la case.
        """
        rep = False
        if element in self.contenu:
            rep = True
            del self.contenu[self.contenu.index(element)]
            self.setPos(self.pos[0], self.pos[1])
        return rep
    
    def vide(self) -> None:
        """Permet de vider la case.
        """
        self.contenu = []

    def ajoute(self, contenu) -> bool:
        """Ajoute un élément sur la case si cela est possible.

        Args:
            contenu (_type_): L'élément à ajouter.

        Returns:
            bool: True si l'élément a pu être ajouté sur la case.
        """
        rep = True
        if not self.marqueur:
            if len(self.contenu) > 0:
                if len(self.contenu) >= 2:
                    rep = False
                elif self.contenu[0].direction%2 != contenu.direction%2:
                    self.tourneBateaux()
                    self.contenu.append(contenu)
                else:
                    self.contenu.append(contenu)
            else:
                self.contenu.append(contenu)
        else:
            rep = False
        if rep:
            contenu.place = True
            self.setPos(self.pos[0], self.pos[1])
        return rep

    def estPleine(self) -> bool:
        """Vérifie si la case est pleine.

        Returns:
            bool: True si la case est pleine.
        """
        if len(self.contenu) == 2:
            return True
        else:
            return False
        
    def estVide(self) -> bool:
        """Vérifie si la case est vide.

        Returns:
            bool: True si la case est vide.
        """
        if len(self.contenu) == 0:
            return True
        else:
            return False
        
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
        if self.typeIle > -1:
            self.typeIle = -1
            self.orienteIle = 0
            self.imaIle = None
            self.marqueur = False

    def contient(self, element: Bateau) -> bool:
        """Vérifie si un élément particulier est sur la case.

        Args:
            element (Bateau): L'élément recherché.

        Returns:
            bool: True s'il est sur la case.
        """
        return element in self.contenu
    
    def setIle(self, preciseDos: str = "a") -> None:
        """Modifie le segment d'île présent sur la case si elle a un marqueur.

        Args:
            preciseDos (str, optional): Précision pour le choix du dossier de segments. Defaults to "a".
        """
        if self.marqueur:
            if self.typeIle == 2:
                dossier = "2"+preciseDos
            else:
                dossier = str(self.typeIle)
            lifichiers = os.listdir(f"jeux/archipel/images/iles/{dossier}")
            segment = random.choice(lifichiers)
            self.imaIle = chargeSegment(f"jeux/archipel/images/iles/{dossier}/{segment}", dossier, f"{segment}{self.orienteIle}", self.orienteIle)
        
    def __add__(self, element):
        """Ajoute un élément à la case.

        Args:
            element (Element): L'élément à ajouter à la case.

        Returns:
            bool: True si l'élément a pu être ajouté à la case.
        """
        return self.ajoute(element)

    def __sub__(self, element):
        """Retire un élément de la case.

        Args:
            element (Element): L'élément à retirer.
        """
        self.retire(element)

    def __getitem__(self, key) -> Bateau:
        """Permet de récupérer un élément précis de la case.

        Args:
            key (int): La position de l'élément sur la case.

        Returns:
            Bateau: L'élément recherché.
        """
        return self.contenu[key]
    
    def __len__(self) -> int:
        """Renvoie le nombre d'éléments présents sur la case.

        Returns:
            int: Nombre d'éléments présents sur la case.
        """
        return len(self.contenu)
    
    def __pos__(self) -> None:
        """Place un marqueur sur la case.
        """
        self.marqueur = True

    def __neg__(self) -> None:
        """Retire le marqueur de la case.
        """
        self.marqueur = False