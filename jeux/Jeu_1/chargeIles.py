from systeme.FondMarin import load_image, image_resize, load_texture_from_image, image_rotate_cw, unload_image, Texture
from jeux.Jeu_1.fonctions.bases import TAILLECASE

segments = {"0": {}, "1": {}, "2a": {}, "2b": {}, "3": {}, "4": {}}

def chargeSegment(image: str, typeSeg: str, nom: str, rotations: int) -> Texture:
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