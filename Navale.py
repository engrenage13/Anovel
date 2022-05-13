from systeme.FondMarin import *
from partie import Partie
from animations.Paillette import Paillette
from ui.bouton import Bouton
from systeme.fenetre import Fenetre

fen = Fenetre()

partie = Partie(fen)

start = Bouton([partie.nouvelleEtape], "Jouer", [BLUE, DARKBLUE, WHITE])
quit = Bouton([fen.switchEtat], "Quitter", [DARKGRAY, DARKBLUE, WHITE])

def accueil():
    draw_rectangle_gradient_v(0, 0, xf, yf, (0, 0, 60, 200), (0, 0, 30, 100))
    for i in range(len(lolo)):
        lolo[i].dessine()
    draw_text_pro(police1, TITRE_F, (int(xf*0.5), int(yf*0.3)), (0, 0), 0, 20, 0, BLUE)
    draw_rectangle(int(xf*0.6), int(yf*0.4), int(xf*0.078), int(yf*0.04), BLUE)
    draw_text_pro(police2, etatVersion, (int(xf*0.605), int(yf*0.406)), (0, 0), 0, 21, 0, BLACK)
    draw_text_pro(police2, version, (int(xf*0.64), int(yf*0.406)), (0, 0), 0, 21, 0, WHITE)
    start.dessine((int(xf/2), int(yf*0.65)))
    quit.dessine((int(xf/2), int(yf*0.77)))

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