from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.case import Case, TAILLECASE

class Plateau:
    def __init__(self, nbCases: int) -> None:
        self.nbCases = nbCases
        self.largeurBordure = int(yf*0.05)
        self.largeurEnvirronement = int(yf*0.2)
        self.cases = []
        x = self.largeurBordure+self.largeurEnvirronement
        y = self.largeurBordure+self.largeurEnvirronement
        for i in range(nbCases):
            cases = []
            for j in range(nbCases):
                cases.append(Case(x, y))
                x += TAILLECASE
            self.cases.append(cases)
            x = self.largeurBordure+self.largeurEnvirronement
            y += TAILLECASE
        # Lien Menu
        self.bloque = False

    def dessine(self) -> None:
        self.dessineEnvirronement()
        self.dessineBordure()
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].dessine()

    def dessineBordure(self) -> None:
        p = self.cases[0][0].pos
        l = self.largeurBordure
        ajustFin = l*2
        OR = [169, 142, 23, 255]
        draw_rectangle_lines_ex([p[0]-l, p[1]-l, TAILLECASE*self.nbCases+ajustFin, 
                                 TAILLECASE*self.nbCases+ajustFin], l, BLACK)
        draw_rectangle(p[0]-l, p[1]-l, l*2, l*2, OR)
        draw_rectangle(p[0]-l+TAILLECASE*self.nbCases, p[1]-l, l*2, l*2, OR)
        draw_rectangle(p[0]-l, p[1]-l+TAILLECASE*self.nbCases, l*2, l*2, OR)
        draw_rectangle(p[0]-l+TAILLECASE*self.nbCases, p[1]-l+TAILLECASE*self.nbCases, l*2, l*2, OR)

    def dessineEnvirronement(self) -> None:
        p = self.cases[0][0].pos
        l = self.largeurEnvirronement+self.largeurBordure
        ajustFin = l*2
        draw_rectangle(p[0]-l, p[1]-l, TAILLECASE*self.nbCases+ajustFin, TAILLECASE*self.nbCases+ajustFin, [11, 23, 62, 255])

    def deplace(self, x: int, y: int) -> None:
        if not self.passeFrontiereHorizontale(x) and self.passeFrontiereVerticale(y):
            y = 0
        elif self.passeFrontiereHorizontale(x) and not self.passeFrontiereVerticale(y):
            x = 0
        elif self.passeFrontiereHorizontale(x) and self.passeFrontiereVerticale(y):
            x = y = 0
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].deplace(x, y)

    def passeFrontiereHorizontale(self, x: int) -> bool:
        rep = False
        if self.cases[0][0].pos[0]+x > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif self.cases[0][self.nbCases-1].pos[0]+TAILLECASE+x < xf-self.largeurBordure-self.largeurEnvirronement:
            rep = True
        return rep
    
    def passeFrontiereVerticale(self, y: int) -> bool:
        rep = False
        if self.cases[0][0].pos[1]+y > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif self.cases[self.nbCases-1][0].pos[1]+TAILLECASE+y < yf-self.largeurBordure-self.largeurEnvirronement:
            rep = True
        return rep