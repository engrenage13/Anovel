import random
from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.fonctions.bases import TAILLECASE, EAUX

class Plateau:
    def __init__(self, nbCases: int, tailleCases: int = TAILLECASE, bordure: float = int(yf*0.05), envirronement: bool = True, plan: bool = False, accroche: tuple[int] = (0, 0)) -> None:
        self.nbCases = nbCases
        self.largeurBordure = bordure
        if envirronement:
            self.largeurEnvirronement = int(yf*0.2)
        else:
            self.largeurEnvirronement = 0
        self.tailleCase = tailleCases
        self.isPlan = plan
        self.env = envirronement
        self.cases = []
        x = accroche[0]+self.largeurBordure+self.largeurEnvirronement
        y = accroche[1]+self.largeurBordure+self.largeurEnvirronement
        for i in range(nbCases):
            cases = []
            for j in range(nbCases):
                if plan:
                    couleur = ([0, 0, 0, 150], BLACK)
                    largeur = 1
                else:
                    couleur = (random.choice(EAUX), [80, 80, 80, 150])
                    largeur = 1.5
                cases.append(Case(x, y, self.tailleCase, couleur, largeur))
                x += self.tailleCase
            self.cases.append(cases)
            x = accroche[0]+self.largeurBordure+self.largeurEnvirronement
            y += self.tailleCase
        # Défilement du plateau
        if plan:
            self.bloque = True
        else:
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
        tCase = self.tailleCase
        ajustFin = l*2
        OR = [169, 142, 23, 255]
        draw_rectangle_lines_ex([p[0]-l, p[1]-l, tCase*self.nbCases+ajustFin, tCase*self.nbCases+ajustFin], l, BLACK)
        draw_rectangle(p[0]-l, p[1]-l, l*2, l*2, OR)
        draw_rectangle(p[0]-l+tCase*self.nbCases, p[1]-l, l*2, l*2, OR)
        draw_rectangle(p[0]-l, p[1]-l+tCase*self.nbCases, l*2, l*2, OR)
        draw_rectangle(p[0]-l+tCase*self.nbCases, p[1]-l+tCase*self.nbCases, l*2, l*2, OR)

    def dessineEnvirronement(self) -> None:
        p = self.cases[0][0].pos
        l = self.largeurEnvirronement+self.largeurBordure
        tCase = self.tailleCase
        ajustFin = l*2
        if self.env:
            draw_rectangle(p[0]-l, p[1]-l, tCase*self.nbCases+ajustFin, tCase*self.nbCases+ajustFin, [11, 23, 62, 255])

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

    def place(self, x: int, y: int) -> None:
        px = x
        py = y
        tCase = self.tailleCase
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].setPos(px, py)
                px += tCase
            py += tCase
            px = x

    def passeFrontiereHorizontale(self, x: int) -> bool:
        rep = False
        tCase = self.tailleCase
        if self.cases[0][0].pos[0]+x > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif self.cases[0][self.nbCases-1].pos[0]+tCase+x < xf-self.largeurBordure-self.largeurEnvirronement:
            rep = True
        return rep
    
    def passeFrontiereVerticale(self, y: int) -> bool:
        rep = False
        tCase = self.tailleCase
        if self.cases[0][0].pos[1]+y > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif self.cases[self.nbCases-1][0].pos[1]+tCase+y < yf-self.largeurBordure-self.largeurEnvirronement:
            rep = True
        return rep
    
    def trouveCoordsCase(self, case: Case) -> tuple[int]|bool:
        trouve = False
        i = 0
        while i < self.nbCases and not trouve:
            j = 0
            while j < self.nbCases and not trouve:
                if self.cases[i][j] == case:
                    trouve = True
                else:
                    j += 1
            if not trouve:
                i += 1
        if trouve:
            return (j, i)
        else:
            return False
    
    def getVoisines(self, case: Case) -> dict[Case|bool]:
        voisines = {'n': False, 's': False, 'o': False, 'e': False}
        pos = self.trouveCoordsCase(case)
        if pos:
            if pos[0] > 0:
                voisines['o'] = self.cases[pos[1]][pos[0]-1]
            if pos[1] > 0:
                voisines['n'] = self.cases[pos[1]-1][pos[0]]
            if pos[0] < self.nbCases-1:
                voisines['e'] = self.cases[pos[1]][pos[0]+1]
            if pos[1] < self.nbCases-1:
                voisines['s'] = self.cases[pos[1]+1][pos[0]]
        return voisines
    
    def __getitem__(self, key) -> list[Case]:
        return self.cases[key]
    
    def __len__(self) -> int:
        return self.nbCases