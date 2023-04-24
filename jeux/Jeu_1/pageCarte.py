from systeme.FondMarin import police1, police2, police2i, BLUE
from jeux.Jeu_1.objets.bases.fenetre import Fenetre, xf, yf, draw_rectangle
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.plateau.zone import Zone
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
        #self.z1 = Zone((0, 0), (2, 1), self.plateau.cases)

    def dessine(self) -> None:
        super().dessine()
        draw_rectangle(0, 0, xf, yf, [144, 132, 78, 85])
        self.plateau.dessine()
        self.titre.dessine([[int(xf*0.01), int(yf*0.005)], 'no'], alignement='g')
        draw_rectangle(0, int(yf*0.11), int(xf*0.2), int(yf*0.06), BLUE)
        self.banniere.dessine([[int(xf*0.01), int(yf*0.115)], 'no'], alignement='g')
        self.expli.dessine([[int(xf*0.005), int(yf*0.21)], 'no'], alignement='g')
        #self.z1.dessine()