from systeme.FondMarin import *
from ui.blocTexte import BlocTexte

class Vignette:
    def __init__(self, titre: str, icone: str) -> None:
        self.largeur = int(xf*0.2)
        self.hauteur = int(yf*0.34)
        self.titre = BlocTexte(titre, police1, int(yf*0.03), [self.largeur, int(self.hauteur/2)])
        ico = load_image(icone)
        image_resize(ico, int(self.hauteur*0.5), int(self.hauteur*0.5))
        self.icone = load_texture_from_image(ico)
        unload_image(ico)
        self.check = False

    def dessine(self, x: int, y: int) -> None:
        if check_collision_point_rec(get_mouse_position(), [x, y, self.largeur, self.hauteur]):
            draw_rectangle(x, y, self.largeur, self.hauteur, [210, 210, 210, 255])
            if is_mouse_button_pressed(0):
                self.check = True
        else:
            draw_rectangle_lines_ex([x, y, self.largeur, self.hauteur], 2, BLACK)
        draw_texture(self.icone, int(x+self.largeur/2-self.icone.width/2), int(y+self.hauteur*0.09), WHITE)
        self.titre.dessine([[int(x+self.largeur/2), int(y+self.hauteur*0.75)], 'c'], BLACK)

    def getDims(self) -> tuple[int]:
        return (self.largeur, self.hauteur)
    
    def reset(self) -> None:
        self.check = False