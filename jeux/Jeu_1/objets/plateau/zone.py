from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.plateau import Plateau

class Zone:
    def __init__(self, debut: tuple, fin: tuple, plateau: Plateau) -> None:
        self.cases = []
        self.plateau = plateau
        self.largeurBordure = int(xf*0.002)
        self.couleurs = ([255, 255, 255, 150], WHITE)
        self.couleurActives = ([255, 255, 255, 150], WHITE)
        self.mappage(debut, fin)

    def dessine(self) -> None:
        for i in range(len(self.cases)):
            Case = self.cases[i]
            voisines = self.plateau.getVoisines(Case)
            x = Case.pos[0]
            y = Case.pos[1]
            cote = Case.taille
            if self.getContact():
                cf = self.couleurActives[0]
                cb = self.couleurActives[1]
            else:
                cf = self.couleurs[0]
                cb = self.couleurs[1]
            draw_rectangle(x, y, cote, cote, cf)
            if not voisines['n'] or voisines['n'] not in self.cases:
                draw_line_ex((x, y), (x+cote, y), self.largeurBordure, cb)
            if not voisines['e'] or voisines['e'] not in self.cases:
                draw_line_ex((x+cote, y), (x+cote, y+cote), self.largeurBordure, cb)
            if not voisines['s'] or voisines['s'] not in self.cases:
                draw_line_ex((x, y+cote), (x+cote, y+cote), self.largeurBordure, cb)
            if not voisines['o'] or voisines['o'] not in self.cases:
                draw_line_ex((x, y), (x, y+cote), self.largeurBordure, cb)

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

    def getContact(self) -> bool:
        rep = False
        i = 0
        while i < len(self.cases) and not rep:
            if self.cases[i].getContact():
                rep = True
            else:
                i += 1
        return rep
    
    def setCouleurs(self, fond: Color, bordure: Color, fondActif: Color, bordureActif: Color) -> None:
        self.couleurs = (fond, bordure)
        self.couleurActives = (fondActif, bordureActif)

    def __add__(self, zone) -> object:
        self.cases += zone.cases
        return self