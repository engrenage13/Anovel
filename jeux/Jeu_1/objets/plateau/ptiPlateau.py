from systeme.FondMarin import draw_rectangle_lines_ex, BLACK, xf, yf
from jeux.Jeu_1.objets.plateau.ptiteCase import PtiteCase

class PtiPlateau:
    def __init__(self, nbCases: int) -> None:
        self.nbCases = nbCases
        self.largeurBordure = 3
        self.tCase = int(yf*0.95/nbCases)
        self.cases = []
        x = int((xf*0.6)-self.tCase*self.nbCases/2)
        y = int((yf/2)-self.tCase*self.nbCases/2)
        for i in range(nbCases):
            cases = []
            for j in range(nbCases):
                cases.append(PtiteCase(x, y, self.tCase))
                x += self.tCase
            self.cases.append(cases)
            x = int((xf*0.6)-self.tCase*self.nbCases/2)
            y += self.tCase
        self.bloque = False

    def dessine(self) -> None:
        p = self.cases[0][0].pos
        l = self.largeurBordure
        ajustFin = l*2
        draw_rectangle_lines_ex([p[0]-l, p[1]-l, self.tCase*self.nbCases+ajustFin, self.tCase*self.nbCases+ajustFin], self.largeurBordure, BLACK)
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].dessine()

    def __getitem__(self, key) -> list[PtiteCase]:
        return self.cases[key]
    
    def __len__(self) -> int:
        return self.nbCases