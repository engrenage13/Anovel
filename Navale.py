from systeme.FondMarin import *
from partie import Partie
from animations.Paillette import Paillette
from ui.bouton import Bouton
from systeme.fenetre import Fenetre

fen = Fenetre()

partie = Partie(fen)

# Boutons
start = Bouton([partie.nouvelleEtape], "Jouer", [DARKBLUE, BLUE, WHITE])
quit = Bouton([fen.switchEtat], "Quitter", [DARKGRAY, GRAY, WHITE])

# Images
nanav = load_image('images/logos/Navale.png')
image_resize(nanav, int(nanav.width*0.19), int(nanav.height*0.19))
logo = load_texture_from_image(nanav)

def accueil():
    draw_rectangle_gradient_v(0, 0, xf, yf, (0, 0, 60, 200), (0, 0, 30, 100))
    for i in range(len(lolo)):
        lolo[i].dessine()
    draw_texture(logo, 0, 0, WHITE)
    draw_text_pro(police2, version, (int(xf*0.005), int(yf*0.975)), (0, 0), 0, 21, 0, WHITE)
    start.dessine((int(xf*0.35), int(yf*0.92)))
    quit.dessine((int(xf*0.65), int(yf*0.92)))

lolo = []
for i in range(10):
    lolo.append(Paillette((0, 0, xf, yf), [BLUE, DARKBLUE, SKYBLUE]))

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    if partie.timeline == 0:
        accueil()
    else:
        partie.dessine()
    end_drawing()

fen.finDuJeu()