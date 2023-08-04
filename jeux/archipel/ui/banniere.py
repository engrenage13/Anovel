from systeme.FondMarin import xf, yf, draw_rectangle, Color, police1
from ui.blocTexte import BlocTexte
from jeux.archipel.fonctions.deplacement import glisse

class Banniere:
    """Crée les bannières utilisées sur la fenêtre d'intro.
    """
    def __init__(self, texte: str, hauteur: int, couleur: Color, gauche: bool = True) -> None:
        """Crée la bannière.

        Args:
            texte (str): Le texte à afficher sur la bannière.
            hauteur (int): Ordonnée du sommet de la bannière.
            couleur (Color): Couleur du fond de la bannière.
            gauche (bool, optional): Alignement à gauche ou à droite de l'écran. Defaults to True.
        """
        self.sens = gauche
        self.longueur = int(xf*0.6)
        self.hauteur = int(yf*0.12)
        self.couleur = couleur
        self.y = hauteur
        self.titre = BlocTexte(texte, police1, int(yf*0.1), [int(xf*0.35), int(yf*0.08)])
        self.reset()

    def dessine(self) -> None:
        """Dessine la bannière.
        """
        draw_rectangle(self.pos[0], self.pos[1], self.longueur, self.hauteur, self.couleur)
        if self.sens:
            self.titre.dessine([[int(self.pos[0]+xf*0.21), int(self.pos[1]+self.hauteur/7)], 'no'], alignement='g')
        else:
            self.titre.dessine([[int(self.pos[0]+xf*0.39), int(self.pos[1]+self.hauteur/7)], 'ne'], alignement='d')
        if not self.auBoutDuChemin():
            self.pos = glisse(self.pos, self.dest, int(xf*0.001))

    def auBoutDuChemin(self) -> bool:
        """Vérifie si la bannière est arrivée au bout de son trajet.

        Returns:
            bool: True si la destination est atteinte.
        """
        rep = False
        if self.sens and self.pos[0] >= self.dest[0]:
            rep = True
        elif not self.sens and self.pos[0] <= self.dest[0]:
            rep = True
        return rep
    
    def reset(self) -> None:
        """Réinitialise certains points de la bannière pour pouvoir rejouer son animation.
        """
        if self.sens:
            self.pos = (-int(xf*0.2), self.y)
            self.dest = (0, self.y)
        else:
            self.pos = (int(xf*0.6), self.y)
            self.dest = (xf-self.longueur, self.y)