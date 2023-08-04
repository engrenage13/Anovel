from systeme.FondMarin import yf, xf, police1
from jeux.archipel.ui.banniere import Banniere
from jeux.archipel.objets.Joueur import Joueur
from jeux.archipel.ui.fagnon import Fagnon
from jeux.archipel.ui.cptRebours import CptRebours
from jeux.archipel.objets.bases.fenetre import Fenetre
from ui.blocTexte import BlocTexte

class Intro(Fenetre):
    """La fenêtre d'introduction.

    Args:
        Fenetre (Fenetre): Hérite du système de fenêtre.
    """
    def __init__(self, joueurs: list[Joueur]) -> None:
        """Crée la fenêtre.

        Args:
            joueurs (list[Joueur]): Les joueurs participant au jeu.
        """
        super().__init__()
        self.bannieres = []
        y = int(yf*0.15)
        for i in range(len(joueurs)):
            if i%2:
                cote = False
            else:
                cote = True
            self.bannieres.append(Banniere(joueurs[i].nom, y, joueurs[i].couleur, cote))
            y += self.bannieres[i].hauteur + int(yf*0.13)
        self.vs = BlocTexte("VS", police1, int(yf*0.12))
        self.objectif = Fagnon("Coulez tous les bateaux adverses", int(xf*0.6))
        self.objectif.setPos(int(xf/2-self.objectif.getDims()[0]/2), int(yf*0.85-self.objectif.getDims()[1]/2))
        self.chrono = CptRebours(5)
        self.chrono.setPos(int(xf*0.93), int(yf*0.93))
        self.chrono.run()

    def dessine(self) -> None:
        """Dessine la fenêtre.
        """
        super().dessine()
        for i in range(len(self.bannieres)):
            self.bannieres[i].dessine()
        self.vs.dessine([[int(xf/2), int(yf*0.32)], 'c'])
        self.objectif.dessine()
        self.chrono.dessine()

    def estFini(self) -> bool:
        """Vérifie si l'animation d'introduction est terminée.

        Returns:
            bool: True si le chrono atteint 0.
        """
        if self.chrono.aFini():
            return True
        else:
            return False
        
    def rejouer(self) -> None:
        """Remet à 0 certains paramètres pour rejouer l'animation.
        """
        for i in range(len(self.bannieres)):
            self.bannieres[i].reset()
        self.chrono.reset()
        self.chrono.run()