from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from ui.flex import Flex

fen = Fenetre()
base = Flex()
f1 = Flex(("38%", xf), (222, yf))
f1.ajoute_enfant(h="40%", couleur=ORANGE)
f1.ajoute_enfant("40%", 43, RED)
base.enfants.append((f1, BLUE))

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    base.dessine()
    end_drawing()

fen.finDuJeu()
