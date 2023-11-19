from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille

class Ice:
    def __init__(self) -> None:
        self.lu = False
        self.message = ""
        # Images
        logo_template = load_image('images/logos/Anovel.png')
        ratio = int(xf*0.4)/logo_template.width
        image_resize(logo_template, int(logo_template.width*ratio), int(logo_template.height*ratio))
        self.logo = load_texture_from_image(logo_template)
        unload_image(logo_template)
        petit_navire = load_image('images/logos/navire.png')
        ratio = int(xf*0.17)/petit_navire.width
        image_resize(petit_navire, int(petit_navire.width*ratio), int(petit_navire.height*ratio))
        self.bateau = load_texture_from_image(petit_navire)
        unload_image(petit_navire)
        # Bouton
        self.Gstart = Grille(int(xf*0.28), [False])
        self.Gstart.ajouteElement(Bouton(TB1o, BTV, "Jouer", '', [self.portailBoreal]), 0, 0)

    def dessine(self) -> None:
        draw_texture(self.logo, int(xf/2-self.logo.width/2), int(yf*0.3-self.logo.height/2), WHITE)
        draw_triangle((int(xf*0.35), yf), (int(xf*2.25), yf), (int(xf*1.08), int(yf*0.8)), [12, 24, 99, 255])
        draw_triangle((-int(xf*0.25), yf), (int(xf*0.6), yf), (int(xf*0.3), int(yf*0.84)), [12, 24, 102, 255])
        draw_triangle((int(xf*0.35), yf), (int(xf*1.25), yf), (int(xf*0.63), int(yf*0.83)), [12, 24, 88, 255])
        draw_triangle((-int(xf*0.85), yf), (int(xf*0.5), yf), (int(xf*0.054), int(yf*0.845)), [12, 24, 147, 255])
        draw_triangle((-int(xf*0.05), yf), (int(xf*0.33), yf), (int(xf*0.14), int(yf*0.86)), [12, 24, 197, 255])
        draw_triangle((int(xf*0.6), yf), (int(xf*1.15), yf), (int(xf*0.85), int(yf*0.81)), [12, 24, 123, 255])
        draw_triangle((int(xf*0.25), yf), (int(xf*0.7), yf), (int(xf*0.47), int(yf*0.94)), [12, 24, 228, 255])
        draw_texture(self.bateau, int(xf/2-self.bateau.width/2), int(yf*0.79-self.bateau.height/2), WHITE)
        self.Gstart.dessine(int(xf/2-self.Gstart.largeur/2), int(yf*0.9-self.Gstart.hauteur/2))

    # Between the worlds
    def portailBoreal(self) -> None:
        """Vérifie quel bouton a été exécuté pour lancer son action.
        """
        self.lu = False
        self.message = "ANOVEL_MENU"

ice = Ice()
