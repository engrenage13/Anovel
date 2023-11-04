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
    Gstart.dessine(int(xf/2-Gstart.largeur/2), int(yf*0.9-Gstart.hauteur/2))
    end_drawing()

fen.finDuJeu()
