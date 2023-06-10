from jeux.Jeu_1.ui.cible import Bateau, Case
from systeme.FondMarin import draw_rectangle_lines_ex, WHITE, draw_circle
from jeux.Jeu_1.objets.plateau.zone import Zone
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.Jeu_1.ui.editTeleco import EditTeleco

class Fleche(EditTeleco):
    def __init__(self, depart: Case, bateau: Bateau, zone: Zone, plateau: Plateau) -> None:
        super().__init__(depart, bateau)
        self.zone = zone
        self.depart = depart
        self.bateau = bateau
        self.plateau = plateau
        self.chemin = [depart]
        self.pointsCardinaux = ["est", "sud", "ouest", "nord"]
        self.origiDir = self.pointsCardinaux[self.bateau.direction][:]
        self.setBoutons()

    def dessine(self) -> None:
        draw_rectangle_lines_ex([self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille], 
                                int(self.case.largeurBordure*2), WHITE)
        if self.play:
            if self.activeDep["nord"]:
                self.opt["nord"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1])
            if self.activeDep["est"]:
                self.opt["est"].dessine(self.case.pos[0]+self.case.taille, int(self.case.pos[1]+self.case.taille/2))
            if self.activeDep["sud"]:
                self.opt["sud"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1]+self.case.taille)
            if self.activeDep["ouest"]:
                self.opt["ouest"].dessine(self.case.pos[0], int(self.case.pos[1]+self.case.taille/2))

    def dessineChemin(self) -> None:
        for i in range(len(self.chemin)-1):
            case = self.chemin[i]
            draw_circle(int(case.pos[0]+case.taille/2), int(case.pos[1]+case.taille/2), case.taille*0.1, WHITE)

    def setBoutons(self) -> None:
        if len(self.chemin)-1 < self.bateau.pm:
            for i in range(len(self.pointsCardinaux)):
                self.activeDep[self.pointsCardinaux[i]] = True
            self.activeDep[self.pointsCardinaux[(self.bateau.direction+2)%len(self.pointsCardinaux)]] = False
            voisines = self.plateau.getVoisines(self.case)
            pn = ['e', 's', 'o', 'n']
            for i in range(len(pn)):
                if not voisines[pn[i]]:
                    self.activeDep[self.pointsCardinaux[i]] = False
                elif self.plateau[voisines[pn[i]][0]][voisines[pn[i]][1]].estPleine():
                    self.activeDep[self.pointsCardinaux[i]] = False
                elif voisines[pn[i]] not in self.zone:
                    self.activeDep[self.pointsCardinaux[i]] = False
        else:
            for i in range(len(self.pointsCardinaux)):
                self.activeDep[self.pointsCardinaux[i]] = False

    def setBateau(self, bateau: Bateau) -> None:
        super().setBateau(bateau)
        self.setBoutons()
        self.chemin = [self.depart]
        self.origiDir = self.pointsCardinaux[self.bateau.direction][:]

    def setCase(self, case: Case) -> None:
        super().setCase(case)
        self.depart = case
        self.setBoutons()
        self.chemin = [self.depart]
    
    def auNord(self) -> None:
        self.deplace("n")

    def aLEst(self) -> None:
        self.deplace("e")

    def auSud(self) -> None:
        self.deplace("s")

    def aLOuest(self) -> None:
        self.deplace("o")

    def deplace(self, direction: str) -> None:
        pc = ['e', 's', 'o', 'n']
        voisines = self.plateau.getVoisines(self.case)
        self.case - self.bateau
        self.case = self.plateau[voisines[direction][0]][voisines[direction][1]]
        if pc.index(direction) == (self.bateau.direction+1)%len(pc):
            self.bateau.droite()
        elif pc.index(direction) == (self.bateau.direction-1)%len(pc):
            self.bateau.gauche()
        self.case + self.bateau
        self.chemin.append(self.case)
        self.setBoutons()

    def reset(self) -> None:
        if self.chemin[-1] != self.depart:
            self.case - self.bateau
            while self.pointsCardinaux[self.bateau.direction] != self.origiDir:
                self.bateau.droite()
            self.case = self.depart
            self.depart + self.bateau
            self.chemin = [self.depart]
            self.setBoutons()