import random
from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.fonctions.bases import TAILLECASE, EAUX
from jeux.Jeu_1.fonctions.deplacement import glisse

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
        self.positionCible = (x, y)
        self.glisse = False
        # /
        # Dessin
        self.elementsPrioritaires = []
        self.grise = False

    def dessine(self) -> None:
        self.dessineEnvirronement()
        self.dessineBordure()
        if len(self.elementsPrioritaires) > 0:
            for i in range(self.nbCases):
                for j in range(self.nbCases):
                    self.cases[i][j].dessine(self.grise)
            for i in range(len(self.elementsPrioritaires)):
                self.elementsPrioritaires[i].dessine()
            for i in range(self.nbCases):
                for j in range(self.nbCases):
                    self.cases[i][j].dessineContenu()
        else:
            for i in range(self.nbCases):
                for j in range(self.nbCases):
                    self.cases[i][j].dessine(self.grise)
                    self.cases[i][j].dessineContenu()
        if self.glisse and self.cases[0][0].pos != self.positionCible:
            self.rePlace()

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

    def place(self, x: int, y: int, glisse: bool = False) -> None:
        self.positionCible = (x, y)
        self.glisse = glisse
        if not glisse:
            px = x
            py = y
            tCase = TAILLECASE
            for i in range(self.nbCases):
                for j in range(self.nbCases):
                    self.cases[i][j].setPos(px, py)
                    px += tCase
                py += tCase
                px = x

    def rePlace(self) -> None:
        px = self.cases[0][0].pos[0]
        py = self.cases[0][0].pos[1]
        dep = glisse((px, py), self.positionCible, int(xf*0.01))
        tCase = TAILLECASE
        x = dep[0]
        y = dep[1]
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].setPos(x, y)
                x += tCase
            y += tCase
            x = dep[0]
        if self.cases[0][0].pos == self.positionCible:
            self.glisse = False

    def passeFrontiereHorizontale(self, x: int, absolue: bool = False) -> bool:
        rep = False
        tCase = self.tailleCase
        if absolue:
            xcomp1 = x
            xcomp2 = int(x+len(self.cases)*tCase)
        else:
            xcomp1 = self.cases[0][0].pos[0]+x
            xcomp2 = self.cases[0][self.nbCases-1].pos[0]+tCase+x
        if xcomp1 > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif xcomp2 < xf-self.largeurBordure-self.largeurEnvirronement:
            rep = True
        return rep
    
    def passeFrontiereVerticale(self, y: int, absolue: bool = False) -> bool:
        rep = False
        tCase = self.tailleCase
        if absolue:
            xcomp1 = y
            xcomp2 = int(y+len(self.cases)*tCase)
        else:
            xcomp1 = self.cases[0][0].pos[1]+y
            xcomp2 = self.cases[self.nbCases-1][0].pos[1]+tCase+y
        if xcomp1 > self.largeurBordure+self.largeurEnvirronement:
            rep = True
        elif xcomp2 < yf-self.largeurBordure-self.largeurEnvirronement:
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
    
    def getVoisines(self, case: Case) -> dict[tuple|bool]:
        voisines = {'n': False, 's': False, 'o': False, 'e': False}
        pos = self.trouveCoordsCase(case)
        if pos:
            if pos[0] > 0:
                voisines['o'] = (pos[1], pos[0]-1)
            if pos[1] > 0:
                voisines['n'] = (pos[1]-1, pos[0])
            if pos[0] < self.nbCases-1:
                voisines['e'] = (pos[1], pos[0]+1)
            if pos[1] < self.nbCases-1:
                voisines['s'] = (pos[1]+1, pos[0])
        return voisines
    
    def focusCase(self, case: tuple) -> None:
        if type(case) != bool:
            x = self.cases[0][0].pos[0]
            y = self.cases[0][0].pos[1]
            cx = int(self.cases[case[0]][case[1]].pos[0]+self.tailleCase/2)
            cy = int(self.cases[case[0]][case[1]].pos[1]+self.tailleCase/2)
            if cx <= int(xf/2):
                dx = int(xf/2-cx)
                mulx = 1
            else:
                dx = int(cx-xf/2)
                mulx = -1
            if cy <= int(yf/2):
                dy = int(yf/2-cy)
                muly = 1
            else:
                dy = int(cy-yf/2)
                muly = -1
            nx = x+(dx*mulx)
            ny = y+(dy*muly)
            if self.passeFrontiereHorizontale(nx, True):
                if mulx > 0:
                    nx = self.largeurBordure+self.largeurEnvirronement
                else:
                    nx = xf-(len(self.cases)*self.tailleCase)-self.largeurBordure-self.largeurEnvirronement
            if self.passeFrontiereVerticale(ny, True):
                if muly > 0:
                    ny = self.largeurBordure+self.largeurEnvirronement
                else:
                    ny = yf-(len(self.cases)*self.tailleCase)-self.largeurBordure-self.largeurEnvirronement
            self.place(nx, ny, True)
    
    def vide(self) -> None:
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].vide()
        self.elementsPrioritaires = []

    def rejouer(self) -> None:
        for i in range(self.nbCases):
            for j in range(len(self.nbCases)):
                self.cases[i][j].rejouer()
        self.elementsPrioritaires = []
    
    def __getitem__(self, key) -> list[Case]:
        return self.cases[key]
    
    def __len__(self) -> int:
        return self.nbCases
    
    def __add__(self, element) -> None:
        if element not in self.elementsPrioritaires:
            self.elementsPrioritaires.append(element)

    def __sub__(self, element) -> None:
        if element in self.elementsPrioritaires:
            pos = self.elementsPrioritaires.index(element)
            del self.elementsPrioritaires[pos]