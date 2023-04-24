from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.plateau import Plateau

class Zone:
    def __init__(self, debut: tuple, fin: tuple, plateau: Plateau) -> None:
        self.cases = []
        self.plateau = plateau
        self.largeurBordure = int(xf*0.002)
        self.couleurFond = [255, 161, 0, 150]
        self.couleurBordure = ORANGE
        self.mappage(debut, fin)

    def dessine(self) -> None:
        for i in range(len(self.cases)):
            Case = self.cases[i]
            voisines = self.plateau.getVoisines(Case)
            x = Case.pos[0]
            y = Case.pos[1]
            cote = Case.taille
            draw_rectangle(x, y, cote, cote, self.couleurFond)
            if not voisines['n'] or voisines['n'] not in self.cases:
                draw_line_ex((x, y), (x+cote, y), self.largeurBordure, self.couleurBordure)
            if not voisines['e'] or voisines['e'] not in self.cases:
                draw_line_ex((x+cote, y), (x+cote, y+cote), self.largeurBordure, self.couleurBordure)
            if not voisines['s'] or voisines['s'] not in self.cases:
                draw_line_ex((x, y+cote), (x+cote, y+cote), self.largeurBordure, self.couleurBordure)
            if not voisines['o'] or voisines['o'] not in self.cases:
                draw_line_ex((x, y), (x, y+cote), self.largeurBordure, self.couleurBordure)

    def mappage(self, debut: tuple, fin: tuple) -> None:
        if debut == fin:
            self.cases.append(self.plateau[debut[1]][debut[0]])
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
                    self.cases.append(self.plateau[starty+i][startx+j])

    def __add__(self, zone) -> object:
        self.cases += zone.cases