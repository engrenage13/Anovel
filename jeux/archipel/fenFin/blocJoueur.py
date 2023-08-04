from systeme.FondMarin import *
from jeux.archipel.objets.Joueur import Joueur
from ui.blocTexte import BlocTexte

class BlocJoueur:
    """Bloc affichant le nom et les statistiques de fin de partie de l'un des joueurs.
    """
    def __init__(self, joueur: Joueur, classement: int) -> None:
        """Crée le bloc.

        Args:
            joueur (Joueur): Le joueur dont les informations seront affichées.
            classement (int): Son rang au classement final de la partie.
        """
        self.joueur = joueur
        self.classement = classement
        # contenu
        self.titre = BlocTexte(self.joueur.nom, police1, int(xf*0.02))
        self.num = BlocTexte(str(self.classement), police1i, int(xf*0.021))
        # dimensions
        self.largeurVignette = int(yf*0.06)
        self.tailleIcone = int(yf*0.07)
        self.espace = int(yf*0.015)
        self.largeur = int(xf*0.5)
        self.hauteur = self.tailleIcone+self.espace*2

    def dessine(self, x: int, y: int) -> None:
        """Dessine le bloc.

        Args:
            x (int): Abscisse du coin supérieur gauche du bloc.
            y (int): Ordonnée du coin supérieur gauche du bloc.
        """
        px = int(str(x))
        py = int(str(y))
        draw_rectangle(px, py, self.largeur, self.hauteur, BLACK)
        if self.classement == 1:
            couleurFond = GOLD
        elif self.classement == 2:
            couleurFond = [201, 202, 220, 255]
        elif self.classement == 3:
            couleurFond = [196, 130, 49, 255]
        else:
            couleurFond = [30, 30, 30, 255]
        draw_rectangle(px, py, self.largeurVignette, self.largeurVignette, couleurFond)
        px += int(self.largeurVignette/2)
        py += int(self.largeurVignette*0.1)
        self.num.dessine([[int(px-self.num.getDims()[0]/2), py], 'no'], WHITE)
        px += int(self.largeurVignette/2 + self.largeur*0.01)
        py += int(self.largeurVignette*0.02)
        self.titre.dessine([[px, py], 'no'], self.joueur.couleur, 'g')
        # bateaux
        px = int(str(x))+self.largeur-self.espace
        py = int(str(y))+self.espace
        draw_rectangle(px-self.tailleIcone, py, self.tailleIcone, self.tailleIcone, [90, 18, 18, 120])
        tm = measure_text_ex(police2i, f"x{self.joueur.nbelimination}", int(yf*0.028), 0)
        draw_text_ex(police2i, f"x{self.joueur.nbelimination}", (int(px-tm.x*0.9), int(py+self.tailleIcone-tm.y*0.8)), int(yf*0.028), 0, WHITE)
        px -= self.tailleIcone+self.espace
        draw_rectangle(px-self.tailleIcone, py, self.tailleIcone, self.tailleIcone, [21, 20, 20, 155])
        tv = measure_text_ex(police2i, f"x{self.joueur.compteBateau()}", int(yf*0.028), 0)
        draw_text_ex(police2i, f"x{self.joueur.compteBateau()}", (int(px-tv.x*0.9), int(py+self.tailleIcone-tv.y*0.8)), int(yf*0.028), 0, WHITE)

    def getDims(self) -> tuple[int]:
        """Renvoie les dimensions du bloc.

        Returns:
            tuple[int]: Largeur x hauteur.
        """
        return (self.largeur, self.hauteur)