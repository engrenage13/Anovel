from systeme.FondMarin import Texture, draw_texture, WHITE, get_mouse_x, get_mouse_y
from jeux.Jeu_1.objets.bases.bougeable import Bougeable

class Element(Bougeable):
    """L'objet de base pour générer n'importe quel élément du jeu.
    """
    def __init__(self, image: Texture, x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self.setImage(image)

    def dessine(self) -> None:
        """Permet d'afficher l'élément
        """
        x = self.pos[0]
        y = self.pos[1]
        l = self.dims[0]
        h = self.dims[1]
        draw_texture(self.image, int(x-l/2), int(y-h/2), WHITE)

    def getContact(self) -> bool:
        """Vérifie si le pointeur de la souris est sur l'élément

        Returns:
            bool: True si la souris est sur l'élément
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[0]+self.coords[2]:
            if y >= self.coords[1] and y <= self.coords[1]+self.coords[3]:
                rep = True
        return rep
    
    def setPos(self, x: int, y: int) -> None:
        """Change la position de l'élément

        Args:
            x (int): Le nouvel abscisse de l'élément
            y (int): Le nouvel ordonnée de l'élément
        """
        super().setPos(x, y)
        self.setCoords()
        
    def setImage(self, image: Texture) -> None:
        """Change l'image de l'élément

        Args:
            image (Texture): La nouvelle image pour l'élément
        """
        self.image = image
        self.dims = (self.image.width, self.image.height)
        self.setCoords()

    def setCoords(self) -> None:
        """Modifie les coordonnées de l'élément
        """
        x = self.pos[0]
        y = self.pos[1]
        self.coords = [int(x-self.dims[0]/2), int(y-self.dims[1]/2), self.image.width, self.image.height]