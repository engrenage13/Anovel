from systeme.FondMarin import *
from partie import Partie
from ui.bouton import Bouton
from systeme.fenetre import Fenetre

fen = Fenetre()

partie = Partie(fen)

# Boutons
start = Bouton([partie.nouvelleEtape], [0, 50, 240, 255], "Jouer")
quit = Bouton([fen.switchEtat], DARKGRAY, "Quitter")

# Images
nanav = load_image('images/logos/Navale.png')
image_resize(nanav, int(nanav.width*0.19), int(nanav.height*0.19))
logo = load_texture_from_image(nanav)
unload_image(nanav)
tableau = load_image('images/backgrounds/epave.png')
ratio = yf/tableau.height
image_resize(tableau, int(tableau.width*ratio), int(tableau.height*ratio))
fond = load_texture_from_image(tableau)
unload_image(tableau)

def accueil():
    draw_texture(fond, 0, 0, WHITE)
    draw_texture(logo, 0, 0, WHITE)
    draw_text_pro(police2, version, (int(xf*0.005), int(yf*0.975)), (0, 0), 0, 19, 0, GRAY)
    start.dessine((int(xf*0.35), int(yf*0.92)), True)
    quit.dessine((int(xf*0.65), int(yf*0.92)))

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    if partie.timeline == 0:
        accueil()
    else:
        partie.dessine()
    end_drawing()

fen.finDuJeu()