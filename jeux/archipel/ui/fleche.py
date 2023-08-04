from random import randint, choice
from jeux.archipel.ui.cible import Bateau, Case
from systeme.FondMarin import *
from jeux.archipel.objets.plateau.zone import Zone
from jeux.archipel.objets.plateau.case import Case
from jeux.archipel.objets.plateau.plateau import Plateau
from jeux.archipel.objets.Bateau import Bateau
from jeux.archipel.ui.editTeleco import EditTeleco

class Fleche(EditTeleco):
    """Gestionnaire de déplacement du bateau.

    Args:
        EditTeleco (EditTeleco): Hérite de la télécommande à bateaux.
    """
    def __init__(self, depart: Case, bateau: Bateau, zone: Zone, plateau: Plateau) -> None:
        """Crée la télécommande.

        Args:
            depart (Case): La case de départ du bateau.
            bateau (Bateau): Le bateau qui se déplace.
            zone (Zone): La zone représentant toutes les cases sur les-quelles le bateau peut se déplacer.
            plateau (Plateau): Le plateau de jeu.
        """
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
        """Dessine le gestionnaire à l'écran.
        """
        draw_rectangle_lines_ex([self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille], 
                                int(self.case.largeurBordure*2), WHITE)
        if self.play:
            if self.activeDep["nord"]:
                self.opt["nord"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1])
                if is_key_pressed(87):
                    self.auNord()
            if self.activeDep["est"]:
                self.opt["est"].dessine(self.case.pos[0]+self.case.taille, int(self.case.pos[1]+self.case.taille/2))
                if is_key_pressed(68):
                    self.aLEst()
            if self.activeDep["sud"]:
                self.opt["sud"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1]+self.case.taille)
                if is_key_pressed(83):
                    self.auSud()
            if self.activeDep["ouest"]:
                self.opt["ouest"].dessine(self.case.pos[0], int(self.case.pos[1]+self.case.taille/2))
                if is_key_pressed(65):
                    self.aLOuest()
        self.dessineChemin()
        self.dessineProgression()

    def dessineChemin(self) -> None:
        """Dessine le chemin parcourue par le bateau à l'écran.
        """
        for i in range(len(self.cases)-1):
            case = self.cases[i]
            draw_circle(int(case.pos[0]+case.taille/2), int(case.pos[1]+case.taille/2), case.taille*0.1, WHITE)
            self.dessineRectangle(case, i)
        #if len(self.chemin) > 1:
            #self.dessineFleche()

    def dessineRectangle(self, case: Case, indice: int) -> None:
        """Dessine les rectangles des flèches.

        Args:
            case (Case): La case dans laquelle il faut dessiner.
            indice (int): L'orientation du rectangle.
        """
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
        """Dessine le pointe de la flèche.

        Args:
            direction (int): L'orientation de la pointe.
        """
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
        """L'indicateur de progression du parcours effectué par le bateau.
        """
        texte = f"{len(self.cases)-1}/{self.bateau.pm}"
        taille = self.case.taille*0.09
        tt = measure_text_ex(police2, texte, taille, 0)
        ecart = int(self.case.taille*0.04)
        bordure = int(self.case.taille*0.02)
        x = int(self.case.pos[0]+self.case.taille-bordure*2-tt.x-ecart)
        y = int(self.case.pos[1]+ecart)
        draw_rectangle_rounded([x, y, int(tt.x+bordure*2.5), int(tt.y+bordure)], 0.15, 30, [255, 255, 255, 190])
        x += bordure
        y += int(bordure/2)
        draw_text_ex(police2, texte, (x, y), taille, 0, BLACK)
    
    def setBoutons(self) -> None:
        """Modifie l'agancement des boutons de déplacement en fonction de la position du bateau.
        """
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
        """Modifie le bateau qui est doit se déplacer.

        Args:
            bateau (Bateau): Le nouveau bateau qui se déplace.
        """
        super().setBateau(bateau)
        self.setBoutons()
        self.cases = [self.depart]
        self.chemin = [[]]
        self.origiDir = self.pointsCardinaux[self.bateau.direction][:]

    def setCase(self, case: Case) -> None:
        """Modifie la case de départ du déplacement.

        Args:
            case (Case): La nouvelle case de départ.
        """
        super().setCase(case)
        self.depart = case
        self.setBoutons()
        self.cases = [self.depart]
        self.chemin = [[]]
    
    def auNord(self) -> None:
        """Déplacement vers la case située au nord de celle actuellement occupée par le bateau.
        """
        self.deplace("n")

    def aLEst(self) -> None:
        """Déplacement vers la case située à l'est de celle actuellement occupée par le bateau.
        """
        self.deplace("e")

    def auSud(self) -> None:
        """Déplacement vers la case située au sud de celle actuellement occupée par le bateau.
        """
        self.deplace("s")

    def aLOuest(self) -> None:
        """Déplacement vers la case située à l'ouest de celle actuellement occupée par le bateau.
        """
        self.deplace("o")

    def deplace(self, direction: str) -> None:
        """Déplace le bateau dans la direction souhaitée.

        Args:
            direction (str): Nord, sud, est ou ouest.
        """
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
        """Réinitialise certains paramètres du déplacement pour en mettre en place un nouveau.
        """
        if self.cases[-1] != self.depart:
            self.case - self.bateau
            while self.pointsCardinaux[self.bateau.direction] != self.origiDir:
                self.bateau.droite()
            self.case = self.depart
            self.depart + self.bateau
            self.cases = [self.depart]
            self.chemin = [[]]
            self.setBoutons()

    def passe(self) -> None:
        """Déplacement aléatoire dans la zone possible.
        """
        pas = randint(1, self.bateau.pm)
        for i in range(pas):
            pc = ['e', 's', 'o', 'n']
            pos = 0
            for j in range(len(self.pointsCardinaux)):
                if not self.activeDep[self.pointsCardinaux[j]]:
                    del pc[pos]
                else:
                    pos += 1
            if len(pc) > 0:
                self.deplace(choice(pc))
        self.setBoutons()