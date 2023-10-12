from systeme.FondMarin import police1, police2, police2i, BLUE, ORANGE
from jeux.archipel.objets.bases.fenetre import Fenetre, xf, yf, draw_rectangle
from jeux.archipel.objets.plateau.plateau import Plateau
from jeux.archipel.objets.plateau.zone import Zone
from jeux.archipel.action.Choix import Choix
from ui.blocTexte import BlocTexte
from jeux.archipel.objets.Joueur import Joueur

class PageCarte(Fenetre):
    """La page de la mini-carte du début de la partie.

    Args:
        Fenetre (Fenetre): Hérite de la structure de l'entité fenêtre.
    """
    def __init__(self, joueur1: Joueur) -> None:
        """Crée la fenêtre.

        Args:
            joueur1 (Joueur): Le joueur qui choisi sa zone de départ.
        """
        super().__init__()
        # Calcul de la taille des cases
        nbCases = 14
        tCase = int(yf*0.95/nbCases)
        # /
        self.plateau = Plateau(nbCases, tCase, False, True, (int(xf*0.6-yf*0.95/2), int(yf/2-yf*0.95/2)))
        self.titre = BlocTexte("ZONES DE DEPART", police1, int(yf*0.05))
        self.banniere = BlocTexte(joueur1.nom.upper(), police2i, int(yf*0.04))
        tex = "Choisis une zone de depart. Ton adversaire commencera dans la zone opposee."
        self.expli = BlocTexte(tex, police2, int(yf*0.03), [int(xf*0.18), ''])
        # Zones
        milieu = int(self.plateau.nbCases/2-1)
        end = self.plateau.nbCases-1
        z1 = Zone((0, 0), (2, 1), self.plateau) + Zone((0, 2), (1, 2), self.plateau)
        z2 = Zone((milieu-1, 0), (milieu+2, 1), self.plateau)
        z3 = Zone((end-2, 0), (end, 1), self.plateau) + Zone((end-1, 2), (end, 2), self.plateau)
        z4 = Zone((end-1, milieu-1), (end, milieu+2), self.plateau)
        z5 = Zone((end-1, end-2), (end, end), self.plateau) + Zone((end-2, end-1), (end-2, end), self.plateau)
        z6 = Zone((milieu-1, end-1), (milieu+2, end), self.plateau)
        z7 = Zone((0, end-1), (2, end), self.plateau) + Zone((0, end-2), (1, end-2), self.plateau)
        z8 = Zone((0, milieu-1), (1, milieu+2), self.plateau)
        #self.zones = [z1, z2, z3, z4, z5, z6, z7, z8]
        self.zones = [z2, z4, z6, z8]
        for i in range(len(self.zones)):
            self.zones[i].setCouleurs([255, 161, 0, 150], ORANGE, [229, 165, 56, 170], [255, 186, 66, 255])
        self.rejouer()

    def dessine(self) -> None:
        """Dessine la fenêtre.
        """
        super().dessine()
        draw_rectangle(0, 0, xf, yf, [144, 132, 78, 85])
        self.plateau.dessine()
        self.titre.dessine([[int(xf*0.005), int(yf*0.005)], 'no'], alignement='g')
        draw_rectangle(0, int(yf*0.11), int(xf*0.2), int(yf*0.06), BLUE)
        self.banniere.dessine([[int(xf*0.01), int(yf*0.115)], 'no'], alignement='g')
        self.expli.dessine([[int(xf*0.005), int(yf*0.21)], 'no'], alignement='g')
        for i in range(len(self.zones)):
            self.zones[i].dessine()
        self.action.verifClic()

    def rejouer(self) -> None:
        """Réinitialise le choix pour rejouer une nouvelle partie.
        """
        self.action = Choix(self.zones)
    
    def estFini(self) -> bool:
        """Vérifie si l'action de la fenêtre est terminée.

        Returns:
            bool: True si l'action est terminée.
        """
        return self.action.estFinie()