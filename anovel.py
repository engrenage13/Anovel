from systeme.FondMarin import begin_drawing, end_drawing, clear_background, BLACK
from systeme.set import startSet
from systeme.verif import fichierExiste, verifSauvegarde, scan
from systeme.fenetre import Fenetre
from menu.menu import Menu
from parametres.parametres import Parametres
from jeux.BN.partie import Partie

if not fichierExiste():
    verifSauvegarde()
scan()
startSet()

fen = Fenetre()
menu = Menu()
param = Parametres()
bataille = Partie()

menu.play = True
precedent = menu
actif = menu

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    actif.dessine()
    if not actif.lu:
        actif.lu = True
        if actif.message == "QUITTE":
            fen.switchEtat()
        # modules noirs et oranges
        elif actif.message == "PRECEDENT":
            actif.play = False
            a = actif
            actif = precedent
            precedent = a
        else:
            message = actif.message
            actif.play = False
            precedent = actif
            if actif.message == "ANOVEL_OPTIONS":
                actif = param
            elif actif.message == "ANOVEL_MENU":
                actif = menu
                if precedent == bataille:
                    bataille.timeline = 0
                    bataille.rejouer()
            elif actif.message == "BN":
                actif = bataille
            actif.play = True
    end_drawing()

fen.finDuJeu()
