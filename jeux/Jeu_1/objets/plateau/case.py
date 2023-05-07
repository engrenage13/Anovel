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

    def dessine(self, grise: bool = False) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, self.couleurs[0])
        draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], self.largeurBordure, self.couleurs[1])
        if grise:
            draw_rectangle(self.pos[0], self.pos[1], self.taille, self.taille, [50, 50, 50, 160])
        
    def dessineContenu(self) -> None:    
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                self.contenu[i].dessine()

    def setPos(self, x: int, y: int) -> None:
        super().setPos(x, y)
        if len(self.contenu) > 0:
            if len(self.contenu) == 1:
                self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/2))
            else:
                if self.contenu[0].direction%2 == 0:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/10*3))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/2), int(self.pos[1]+self.taille/10*7))
                else:
                    self.contenu[0].setPos(int(self.pos[0]+self.taille/10*3), int(self.pos[1]+self.taille/2))
                    self.contenu[1].setPos(int(self.pos[0]+self.taille/10*7), int(self.pos[1]+self.taille/2))

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
            elif self.contenu[0].direction%2 == contenu.direction%2:
                self.contenu.append(contenu)
            else:
                rep = False
        else:
            self.contenu.append(contenu)
        if rep:
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
        
    def __add__(self, element):
        return self.ajoute(element)

    def __sub__(self, element):
        self.retire(element)

    def __getitem__(self, key) -> Bateau:
        return self.contenu[key]
    
    def __len__(self) -> int:
        return len(self.contenu)