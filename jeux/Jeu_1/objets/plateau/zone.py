from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.ptiteCase import PtiteCase

class Zone:
    def __init__(self, debut: tuple, fin: tuple, plateau: list[PtiteCase]) -> None:
        self.cases = []
        self.largeurBordure = int(xf*0.002)
        self.couleurFond = [255, 161, 0, 150]
        self.couleurBordure = ORANGE
        self.mappage(debut, fin, plateau)

    def dessine(self) -> None:
        for i in range(len(self.cases)):
            Case = self.cases[i]
            x = Case.pos[0]
            y = Case.pos[1]
            cote = Case.taille
            draw_rectangle(x, y, cote, cote, self.couleurFond)
            draw_line_ex((x, y), (x+cote, y), self.largeurBordure, self.couleurBordure)
            #draw_rectangle_lines_ex([x, y, cote, cote], self.largeurBordure, self.couleurBordure)

    def mappage(self, debut: tuple, fin: tuple, plateau: list[PtiteCase]) -> None:
        if debut == fin:
            self.cases.append(plateau[debut[0]][debut[1]])
        else:
            if debut[0] <= fin[0]:
                startx = debut[0]
                finx = fin[0]
            else:
                startx = fin[0]
                finx = debut[0]
            if debut[1] <= fin[1]:
                starty = debut[1]
                finy = fin[1]
            else:
                starty = fin[1]
                finy = debut[1]
            for i in range(finy-starty+1):
                for j in range(finx-startx+1):
                    print(starty+i, startx+j)
                    self.cases.append(plateau[starty+i][startx+j])