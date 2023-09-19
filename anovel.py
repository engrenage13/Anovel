from systeme.FondMarin import begin_drawing, end_drawing, clear_background, BLACK, config_sys
from systeme.set import startSet
from systeme.verif import fichierExiste, verifSauvegarde, scan
from systeme.fenetre import Fenetre
from menu.menu import Menu
from parametres.parametres import Parametres
from jeux.BN.partie import Partie
from jeux.archipel.archipel import Archipel

if not fichierExiste():
    verifSauvegarde()
scan()
startSet()

fen = Fenetre()
menu = Menu()
param = Parametres()
bataille = Partie()
archipel = Archipel()
fenetre = {"menu": menu, "param": param, "bn": bataille, "archipel": archipel}

menu.play = True
if config_sys['dev']:
    precedent = fenetre[config_sys['dev'].lower()]
    actif = fenetre[config_sys['dev'].lower()]
else:
    precedent = menu
    actif = menu

if type(actif) == Archipel:
    actif.initialise()

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
            elif actif.message == "ARCHIPEL":
                archipel.initialise()
                actif = archipel
            actif.play = True
    end_drawing()

fen.finDuJeu()
