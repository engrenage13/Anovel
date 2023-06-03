from systeme.FondMarin import draw_line_ex, WHITE, is_mouse_button_pressed
from jeux.Jeu_1.objets.plateau.zone import Zone
from jeux.Jeu_1.objets.plateau.case import Case
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.Bateau import Bateau

class Fleche:
    def __init__(self, case: Case, bateau: Bateau, zone: Zone, plateau: Plateau) -> None:
        self.zone = zone
        self.depart = case
        self.bateau = bateau
        self.plateau = plateau
        self.longueur = int(self.plateau.tailleCase*0.18)
        self.largeur = 5
        self.play = True

    def dessine(self) -> None:
        if self.zone.getContact() and self.play:
            case = self.trouveCase()
            draw_line_ex((int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.1)), (int(case.pos[0]+case.taille*0.1+self.longueur), int(case.pos[1]+case.taille*0.1)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.9-self.longueur), int(case.pos[1]+case.taille*0.1)), (int(case.pos[0]+case.taille*0.9), int(case.pos[1]+case.taille*0.1)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.9), int(case.pos[1]+case.taille*0.1)), (int(case.pos[0]+case.taille*0.9), int(case.pos[1]+self.longueur+case.taille*0.1)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.9), int(case.pos[1]+case.taille*0.9-self.longueur)), (int(case.pos[0]+case.taille*0.9), int(case.pos[1]+case.taille*0.9)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.9-self.longueur), int(case.pos[1]+case.taille*0.9)), (int(case.pos[0]+case.taille*0.9), int(case.pos[1]+case.taille*0.9)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.9)), (int(case.pos[0]+self.longueur+case.taille*0.1), int(case.pos[1]+case.taille*0.9)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.9-self.longueur)), (int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.9)), self.largeur, WHITE)
            draw_line_ex((int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.1)), (int(case.pos[0]+case.taille*0.1), int(case.pos[1]+case.taille*0.1+self.longueur)), self.largeur, WHITE)
            #self.positionne()
        
    def setCase(self, case: Case) -> None:
        self.case = case

    def setBateau(self, bateau: Bateau) -> None:
        self.bateau = bateau

    def positionne(self) -> None:
        if self.play:
            if is_mouse_button_pressed(0):
                self.case + self.bateau

    def checkBateauEstPlace(self) -> bool:
        if self.bateau in self.case.contenu:
            return True
        else:
            return False
        
    def trouveCase(self) -> Case:
        trouve = False
        i = 0
        while i < len(self.zone) and not trouve:
            c = self.zone[i]
            case = self.plateau[c[0]][c[1]]
            if case.getContact():
                trouve = True
            else:
                i += 1
        return case