from jeux.Jeu_1.ui.cible import Bateau, Case
from systeme.FondMarin import *
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
        self.cases = [depart]
        self.chemin = [[]]
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
        self.dessineChemin()
        self.dessineProgression()

    def dessineChemin(self) -> None:
        for i in range(len(self.cases)-1):
            case = self.cases[i]
            draw_circle(int(case.pos[0]+case.taille/2), int(case.pos[1]+case.taille/2), case.taille*0.1, WHITE)
            self.dessineRectangle(case, i)
        #if len(self.chemin) > 1:
            #self.dessineFleche()

    def dessineRectangle(self, case: Case, indice: int) -> None:
        x = case.pos[0]
        y = case.pos[1]
        t = case.taille
        for i in range(len(self.chemin[indice])):
            trait = self.chemin[indice][i]
            if indice == len(self.chemin)-2 and i == len(self.chemin[indice])-1:
                self.dessineFleche(trait)
            else:
                if trait == 0:
                    draw_rectangle(int(x+t*0.62), int(y+t*0.43), int(t*0.38), int(t*0.14), WHITE)
                elif trait == 1:
                    draw_rectangle(int(x+t*0.43), int(y+t*0.62), int(t*0.14), int(t*0.38), WHITE)
                elif trait == 2:
                    draw_rectangle(x, int(y+t*0.43), int(t*0.38), int(t*0.14), WHITE)
                else:
                    draw_rectangle(int(x+t*0.43), y, int(t*0.14), int(t*0.38), WHITE)

    def dessineFleche(self, direction: int) -> None:
        case = self.cases[-2]
        x = case.pos[0]
        y = case.pos[1]
        t = case.taille
        if direction == 0:
            draw_rectangle(int(x+t*0.62), int(y+t*0.43), int(t*0.25), int(t*0.14), WHITE)
            draw_triangle((int(x+t*0.83), int(y+t*0.67)), (int(x+t*0.99), int(y+t*0.5)), (int(x+t*0.83), int(y+t*0.33)), WHITE)
        elif direction == 1:
            draw_rectangle(int(x+t*0.43), int(y+t*0.62), int(t*0.14), int(t*0.25), WHITE)
            draw_triangle((int(x+t*0.5), int(y+t*0.99)), (int(x+t*0.67), int(y+t*0.83)), (int(x+t*0.33), int(y+t*0.83)), WHITE)
        elif direction == 2:
            draw_rectangle(int(x+t*0.13), int(y+t*0.43), int(t*0.25), int(t*0.14), WHITE)
            draw_triangle((int(x+t*0.17), int(y+t*0.67)), (int(x+t*0.17), int(y+t*0.33)), (int(x+t*0.01), int(y+t*0.5)), WHITE)
        else:
            draw_rectangle(int(x+t*0.43), int(y+t*0.13), int(t*0.14), int(t*0.25), WHITE)
            draw_triangle((int(x+t*0.67), int(y+t*0.17)), (int(x+t*0.5), int(y+t*0.01)), (int(x+t*0.33), int(y+t*0.17)), WHITE)

    def dessineProgression(self) -> None:
        texte = f"{len(self.cases)-1}/{self.bateau.pm}"
        taille = self.case.taille*0.09
        tt = measure_text_ex(police2, texte, taille, 0)
        ecart = int(self.case.taille*0.04)
        bordure = int(self.case.taille*0.02)
        x = int(self.case.pos[0]+self.case.taille-bordure*2-tt.x-ecart)
        y = int(self.case.pos[1]+ecart)
        draw_rectangle_rounded([x, y, int(tt.x+bordure*2), int(tt.y+bordure)], 0.15, 30, [255, 255, 255, 190])
        x += bordure
        y += int(bordure/2)
        draw_text_ex(police2, texte, (x, y), taille, 0, BLACK)
    
    def setBoutons(self) -> None:
        if len(self.cases)-1 < self.bateau.pm:
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
        self.cases = [self.depart]
        self.chemin = [[]]
        self.origiDir = self.pointsCardinaux[self.bateau.direction][:]

    def setCase(self, case: Case) -> None:
        super().setCase(case)
        self.depart = case
        self.setBoutons()
        self.cases = [self.depart]
        self.chemin = [[]]
    
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
        self.cases.append(self.case)
        self.chemin[-1].append(pc.index(direction))
        self.chemin.append([(pc.index(direction)+2)%len(pc)])
        self.setBoutons()

    def reset(self) -> None:
        if self.cases[-1] != self.depart:
            self.case - self.bateau
            while self.pointsCardinaux[self.bateau.direction] != self.origiDir:
                self.bateau.droite()
            self.case = self.depart
            self.depart + self.bateau
            self.cases = [self.depart]
            self.chemin = [[]]
            self.setBoutons()