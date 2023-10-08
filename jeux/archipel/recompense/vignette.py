from systeme.FondMarin import *
from ui.blocTexte import BlocTexte

class Vignette:
    """L'affichage d'une récompense pour la fenêtre de récompenses.
    """
    def __init__(self, titre: str, icone: str) -> None:
        """Crée une vignette.

        Args:
            titre (str): Nom de la récompense.
            icone (str): Icône de la vignette.
        """
        self.largeur = int(xf*0.2)
        self.hauteur = int(yf*0.34)
        self.titre = BlocTexte(titre, police1, int(yf*0.03), [self.largeur, int(self.hauteur/2)])
        ico = load_image(icone)
        image_resize(ico, int(self.hauteur*0.5), int(self.hauteur*0.5))
        self.icone = load_texture_from_image(ico)
        unload_image(ico)
        self.check = False

    def dessine(self, x: int, y: int) -> None:
        """Dessine la vignette à l'écran.

        Args:
            x (int): Abscisse du coin supérieur gauche de la vignette.
            y (int): Ordonnée du coin supérieur gauche.
        """
        if check_collision_point_rec(get_mouse_position(), [x, y, self.largeur, self.hauteur]):
            couleur = [21, 21, 23, 255]
            if is_mouse_button_pressed(0):
                self.check = True
        else:
            couleur = [31, 31, 33, 255]
        draw_rectangle(x, y, self.largeur, self.hauteur, couleur)
        draw_texture(self.icone, int(x+self.largeur/2-self.icone.width/2), int(y+self.hauteur*0.09), WHITE)
        self.titre.dessine([[int(x+self.largeur/2), int(y+self.hauteur*0.75)], 'c'], WHITE)

    def getDims(self) -> tuple[int]:
        """Renvoie les dimensions de la vignette.

        Returns:
            tuple[int]: (largeur, hauteur).
        """
        return (self.largeur, self.hauteur)
    
    def reset(self) -> None:
        """Réinitialise la vignette.
        """
        self.check = False