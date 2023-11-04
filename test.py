from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from ui.flex import Flex

fen = Fenetre()
base = Flex(pad=20)
f1 = Flex(("38%", base.longueur), (222, base.hauteur), 1)
f1.ajoute_enfant(h="40%", couleur=ORANGE)
f1.ajoute_enfant("40%", 43, couleur=RED)
base.enfants.append((f1, BLUE))
#base.ajoute_enfant("10%", "10%", couleur=GREEN)

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    base.dessine(couleur=[30, 30, 30, 255])
    end_drawing()

fen.finDuJeu()
