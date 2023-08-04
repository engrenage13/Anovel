from systeme.FondMarin import draw_texture, police2, yf, Texture
from ui.blocTexte import BlocTexte

class Attribut:
    """Les icônes qui s'affichent sur la sélection du tiroir.
    """
    def __init__(self, valeur: int, icone: Texture) -> None:
        """Crée un attribut.

        Args:
            valeur (int): La valeur de la statistique.
            icone (Texture): L'icône qui illustre cette stat.
        """
        self.pos = (0, 0)
        self.setValeur(valeur)
        self.icone = icone

    def dessine(self, transparence: int = 255) -> None:
        """Dessine l'attribut.

        Args:
            transparence (int, optional): Transparence qui sera appliquée sur l'attribut. Defaults to 255.
        """
        x = int(self.pos[0])
        self.valeur.dessine([[x, self.pos[1]], 'no'], [255, 255, 255, transparence])
        x += int(self.valeur.getDims()[0])
        draw_texture(self.icone, x, self.pos[1], [255, 255, 255, transparence])

    def setValeur(self, valeur: str|int) -> None:
        """Modifie la valeur de la stat.

        Args:
            valeur (str | int): La nouvelle valeur de la stat.
        """
        self.valeur = BlocTexte(str(valeur), police2, int(yf*0.035))

    def getDims(self) -> tuple[int]:
        """Renvoie les dimensions de l'attribut.

        Returns:
            tuple[int]: (largeur, hauteur).
        """
        return (self.valeur.getDims()[0]+self.icone.width, self.icone.height)