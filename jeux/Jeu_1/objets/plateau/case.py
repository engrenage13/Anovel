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

    def dessineMarqueur(self) -> None:
        v = 0.07
        t = int(self.taille*v)
        if self.contenu[0].direction%2 == 1:
            x = 1-v*len(self.contenu)
            y = 0.93
        else:
            x = 0.93
            y = 1-v*len(self.contenu)
        for i in range(len(self.contenu)):
            draw_rectangle(int(self.pos[0]+x*self.taille), int(self.pos[1]+y*self.taille), t, t, WHITE)
            draw_rectangle_lines(int(self.pos[0]+x*self.taille), int(self.pos[1]+y*self.taille), t, t, BLACK)
            draw_text_ex(police1, str(self.contenu[i].id), (int(self.pos[0]+(x+0.016)*self.taille), int(self.pos[1]+(y+0.005)*self.taille)), t, 0, self.contenu[i].couleur)
            if self.contenu[0].direction%2 == 1:
                x += v
            else:
                y += v
        
    def dessineContenu(self) -> None:    
        if len(self.contenu) > 0:
            for i in range(len(self.contenu)):
                self.contenu[i].dessine()
                if self.contenu[i].actif:
                    draw_rectangle_lines_ex([self.pos[0], self.pos[1], self.taille, self.taille], 3, WHITE)
            self.dessineMarqueur()

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