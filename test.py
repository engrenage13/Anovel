from systeme.FondMarin import begin_drawing, end_drawing, clear_background, BLACK, BLUE
from systeme.fenetre import Fenetre
from ui.flex import Flex

fen = Fenetre()
base = Flex()
f1 = Flex("38%", 222)

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    base.dessine()
    f1.dessine(BLUE)
    end_drawing()

fen.finDuJeu()
