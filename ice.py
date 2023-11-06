from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille

fen = Fenetre()

# Variables
lu = False
message = ""

# Images
logo_template = load_image('images/logos/Anovel.png')
ratio = int(xf*0.4)/logo_template.width
image_resize(logo_template, int(logo_template.width*ratio), int(logo_template.height*ratio))
logo = load_texture_from_image(logo_template)
unload_image(logo_template)
petit_navire = load_image('images/logos/navire.png')
ratio = int(xf*0.17)/petit_navire.width
image_resize(petit_navire, int(petit_navire.width*ratio), int(petit_navire.height*ratio))
bateau = load_texture_from_image(petit_navire)
unload_image(petit_navire)

# Between the worlds
def portailBoreal() -> None:
    """Vérifie quel bouton a été exécuté pour lancer son action.
    """
    lu = False
    message = "ANOVEL_MENU"

# Bouton
Gstart = Grille(int(xf*0.28), [False])
Gstart.ajouteElement(Bouton(TB1o, BTV, "Jouer", '', [portailBoreal]), 0, 0)

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(WHITE)
    draw_texture(logo, int(xf/2-logo.width/2), int(yf*0.3-logo.height/2), WHITE)
    draw_triangle((int(xf*0.35), yf), (int(xf*2.25), yf), (int(xf*1.08), int(yf*0.8)), [12, 24, 99, 255])
    draw_triangle((-int(xf*0.25), yf), (int(xf*0.6), yf), (int(xf*0.3), int(yf*0.84)), [12, 24, 102, 255])
    draw_triangle((int(xf*0.35), yf), (int(xf*1.25), yf), (int(xf*0.63), int(yf*0.83)), [12, 24, 88, 255])
    draw_triangle((-int(xf*0.85), yf), (int(xf*0.5), yf), (int(xf*0.054), int(yf*0.845)), [12, 24, 147, 255])
    draw_triangle((-int(xf*0.05), yf), (int(xf*0.33), yf), (int(xf*0.14), int(yf*0.86)), [12, 24, 197, 255])
    draw_triangle((int(xf*0.6), yf), (int(xf*1.15), yf), (int(xf*0.85), int(yf*0.81)), [12, 24, 123, 255])
    draw_texture(bateau, int(xf/2-bateau.width/2), int(yf*0.79-bateau.height/2), WHITE)
    Gstart.dessine(int(xf/2-Gstart.largeur/2), int(yf*0.9-Gstart.hauteur/2))
    end_drawing()

fen.finDuJeu()
