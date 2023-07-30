from systeme.FondMarin import *
from jeux.Jeu_1.fonctions.bases import TAILLECASE
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.objets.bases.bougeable import Bougeable

class Case(Bougeable):
    def __init__(self, x: int = 0, y: int = 0, taille: int = TAILLECASE, couleurs: tuple[Color] = (WHITE, BLACK), bordure: float = 1.5) -> None:
        super().__init__(x, y)
        self.taille = taille
        self.couleurs = couleurs
        self.largeurBordure = bordure
        self.contenu = []
        # Iles
        self.typeIle = -1
        self.marqueur = False

    def dessine(self, grise: bool = False) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleurs[0])
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], self.largeurBordure, self.couleurs[1])
        if grise:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [50, 50, 50, 160])

    def dessineMarqueur(self, x: int, y: int, id: int|str, couleur: Color) -> None:
        t = int(self.taille*0.1)
        draw_rectangle_rounded([x, y, t, t], 0.3, 360, couleur)
        draw_text_ex(police1, str(id), (int(x+0.028*self.taille), int(y+0.005*self.taille)), 23, 0, WHITE)
        
    def dessineContenu(self) -> None:
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
        rep = False
        if element in self.contenu:
            rep = True
            del self.contenu[self.contenu.index(element)]
            self.setPos(self.pos[0], self.pos[1])
        return rep
    
    def vide(self) -> None:
        self.contenu = []

    def ajoute(self, contenu) -> bool:
        rep = True
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
        if rep:
            contenu.place = True
            self.setPos(self.pos[0], self.pos[1])
        return rep

    def estPleine(self) -> bool:
        if len(self.contenu) == 2:
            return True
        else:
            return False
        
    def estVide(self) -> bool:
        if len(self.contenu) == 0:
            return True
        else:
            return False
        
    def getContact(self) -> bool:
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.pos[0] and x <= self.pos[0]+self.taille:
            if y >= self.pos[1] and y <= self.pos[1]+self.taille:
                rep = True
        return rep
    
    def tourneBateaux(self, sens: bool = True) -> None:
        for i in range(len(self.contenu)):
            if sens:
                self.contenu[i].gauche()
            else:
                self.contenu[i].droite()
        self.setPos(self.pos[0], self.pos[1])

    def rejouer(self) -> None:
        if len(self.contenu) > 0:
            self.vide()
        if self.typeIle > -1:
            self.typeIle = -1
            self.marqueur = False

    def contient(self, element: Bateau) -> bool:
        return element in self.contenu
        
    def __add__(self, element):
        return self.ajoute(element)

    def __sub__(self, element):
        self.retire(element)

    def __getitem__(self, key) -> Bateau:
        return self.contenu[key]
    
    def __len__(self) -> int:
        return len(self.contenu)
    
    def __pos__(self) -> None:
        self.marqueur = True

    def __neg__(self) -> None:
        self.marqueur = False