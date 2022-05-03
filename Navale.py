from FondMarin import *
#from partie import Partie
from animations.paillette import Paillette
#from ui.bouton import Bouton

#def jouer():
    #jeu = Partie()
    #jeu.miseEnPlace()
    #etincelle.fin()

#etincelle = Etincelle()
#start = Bouton(jouer, "Jouer", BLUE, nom=['start', 'accueil'])
#quit = Bouton(auRevoir, "Quitter", nom=['auRevoir', 'accueil'])

def accueil():
    draw_rectangle_gradient_v(0, 0, xf, yf, (0, 0, 60, 200), (0, 0, 30, 100))
    for i in range(len(lolo)):
        lolo[i].dessine()
    draw_text_pro(police1, TITRE_F, (int(xf*0.5), int(yf*0.3)), (0, 0), 0, 20, 0, BLUE)
    draw_rectangle(int(xf*0.6), int(yf*0.4), int(xf*0.078), int(yf*0.04), BLUE)
    draw_text_pro(police2, "alpha", (int(xf*0.605), int(yf*0.406)), (0, 0), 0, 21, 0, BLACK)
    draw_text_pro(police2, version, (int(xf*0.64), int(yf*0.406)), (0, 0), 0, 21, 0, WHITE)
    #start.dessine((xf/2, yf*0.65))
    #quit.dessine((xf/2, yf*0.77))

lolo = []
for i in range(10):
    lolo.append(Paillette((xf, yf), [BLUE, DARKBLUE, SKYBLUE]))

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    accueil()
    end_drawing()