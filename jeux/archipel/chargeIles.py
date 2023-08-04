from systeme.FondMarin import load_image, image_resize, load_texture_from_image, image_rotate_cw, unload_image, Texture
from jeux.archipel.fonctions.bases import TAILLECASE

segments = {"0": {}, "1": {}, "2a": {}, "2b": {}, "3": {}, "4": {}}

def chargeSegment(image: str, typeSeg: str, nom: str, rotations: int) -> Texture:
    """Charge les segments qui doivent apparaître sur le plateau.

    Args:
        image (str): Le chemin de l'image recherchée.
        typeSeg (str): Le type de segment.
        nom (str): Le nom qu'il faudra lui donner.
        rotations (int): Le nombre de rotations de 90° dans le sens horaire qu'il faut faire subir au segment.

    Returns:
        Texture: Le segment chargé.
    """
    if segments[typeSeg].get(nom, False):
        return segments[typeSeg].get(nom)
    else:
        ima = load_image(image)
        image_resize(ima, TAILLECASE, TAILLECASE)
        for i in range(rotations):
            image_rotate_cw(ima)
        texture = load_texture_from_image(ima)
        unload_image(ima)
        segments[typeSeg][nom] = texture
        return texture