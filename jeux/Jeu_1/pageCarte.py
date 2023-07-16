from systeme.FondMarin import police1, police2, police2i, BLUE, ORANGE
from jeux.Jeu_1.objets.bases.fenetre import Fenetre, xf, yf, draw_rectangle
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.plateau.zone import Zone
from jeux.Jeu_1.action.Choix import Choix
from ui.blocTexte import BlocTexte

class PageCarte(Fenetre):
    def __init__(self) -> None:
        super().__init__()
        # Calcul de la taille des cases
        nbCases = 14
        tCase = int(yf*0.95/nbCases)
        # /
        self.plateau = Plateau(14, tCase, 3, False, True, (int(xf*0.6-yf*0.95/2), int(yf/2-yf*0.95/2)))
        self.titre = BlocTexte("CARTE", police1, int(yf*0.05))
        self.banniere = BlocTexte("JOUEUR 1", police2i, int(yf*0.04))
        tex = "Choisis une zone de depart. Ton adversaire commencera dans la zone opposee."
        self.expli = BlocTexte(tex, police2, int(yf*0.03), [int(xf*0.18), ''])
        # Zones
        z1 = Zone((0, 0), (2, 1), self.plateau) + Zone((0, 2), (1, 2), self.plateau)
        z2 = Zone((5, 0), (8, 1), self.plateau)
        z3 = Zone((11, 0), (13, 1), self.plateau) + Zone((12, 2), (13, 2), self.plateau)
        z4 = Zone((12, 5), (13, 8), self.plateau)
        z5 = Zone((12, 11), (13, 13), self.plateau) + Zone((11, 12), (11, 13), self.plateau)
        z6 = Zone((5, 12), (8, 13), self.plateau)
        z7 = Zone((0, 11), (1, 13), self.plateau) + Zone((2, 12), (2, 13), self.plateau)
        z8 = Zone((0, 5), (1, 8), self.plateau)
        #self.zones = [z1, z2, z3, z4, z5, z6, z7, z8]
        self.zones = [z2, z4, z6, z8]
        for i in range(len(self.zones)):
            self.zones[i].setCouleurs([255, 161, 0, 150], ORANGE, [229, 165, 56, 170], [255, 186, 66, 255])
        self.rejouer()

    def dessine(self) -> None:
        super().dessine()
        draw_rectangle(0, 0, xf, yf, [144, 132, 78, 85])
        self.plateau.dessine()
        self.titre.dessine([[int(xf*0.01), int(yf*0.005)], 'no'], alignement='g')
        draw_rectangle(0, int(yf*0.11), int(xf*0.2), int(yf*0.06), BLUE)
        self.banniere.dessine([[int(xf*0.01), int(yf*0.115)], 'no'], alignement='g')
        self.expli.dessine([[int(xf*0.005), int(yf*0.21)], 'no'], alignement='g')
        for i in range(len(self.zones)):
            self.zones[i].dessine()
        self.action.verifClic()

    def rejouer(self) -> None:
        self.action = Choix(self.zones)
    
    def estFini(self) -> bool:
        return self.action.estFinie()