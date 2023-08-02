from systeme.FondMarin import load_image, image_rotate_cw, image_resize, load_texture_from_image
from jeux.archipel.objets.bases.element import Element
from jeux.archipel.fonctions.bases import TAILLECASE

class Pivote(Element):
    """Permet de créer un élément ayant la capacité de pivoter

    Args:
        Element (Class): La structure de base de tout élément
    """
    def __init__(self, image: str, x: int = 0, y: int = 0) -> None:
        self.direction = 0
        self.images = []
        # Travail des images
        img = load_image(image)
        prop = TAILLECASE*0.9
        for i in range(4):
            if i > 0:
                image_rotate_cw(img)
            if img.width >= img.height:
                diviseur = img.width
            else:
                diviseur = img.height
            image_resize(img, int(img.width*prop/diviseur), int(img.height*prop/diviseur))
            self.images.append(load_texture_from_image(img))
        # /
        super().__init__(self.images[self.direction], x, y)

    def reset(self, x: int = 0, y: int = 0) -> None:
        """Permet de réinitialiser l'orientation de l'élément et de changer sa position.

        Args:
            x (int, optional): Nouvel abscisse pour l'élément. Defaults to 0.
            y (int, optional): Nouvel ordonnée pour l'élément. Defaults to 0.
        """
        self.direction = 0
        self.setPos(x, y)
        self.setImage(self.images[self.direction])

    def gauche(self) -> None:
        """Permet de pivoter de 90° vers la gauche
        """
        self.direction -= 1
        if self.direction < 0:
            self.direction = 3
        self.setImage(self.images[self.direction])

    def droite(self) -> None:
        """Permet de pivoter de 90° vers la droite
        """
        self.direction = (self.direction+1)%4
        self.setImage(self.images[self.direction]) 