from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from systeme.set import startSet
from systeme.verif import fichierExiste, verifSauvegarde, scan
from BN.partie import Partie
from ui.bouton import Bouton
from parametres.parametres import Parametres

fen = Fenetre()
if not fichierExiste():
    verifSauvegarde()
scan()
startSet()
partie = Partie(fen)
param = Parametres()

# Boutons
start = Bouton([partie.nouvelleEtape], [0, 50, 240, 255], "Jouer")
sett = Bouton([param.ouvre], [80, 137, 80, 255], "Parametres")
quit = Bouton([fen.switchEtat], DARKGRAY, "Quitter")

# Images
nonov = load_image('images/logos/Navale.png')
ratio = xf/nonov.width*0.35
image_resize(nonov, int(nonov.width*ratio), int(nonov.height*ratio))
logo = load_texture_from_image(nonov)
unload_image(nonov)
tableau = load_image('images/backgrounds/epave.png')
ratio = yf/tableau.height
image_resize(tableau, int(tableau.width*ratio), int(tableau.height*ratio))
fond = load_texture_from_image(tableau)
unload_image(tableau)

def accueil():
    if not param.ouvert:
        draw_texture(fond, 0, 0, WHITE)
        draw_texture(logo, 0, 0, WHITE)
        taille = int(yf*0.02)
        tv = measure_text_ex(police3i, version, taille, 0)
        draw_text_pro(police3i, f"{version} - {etatVersion.lower()}", (int(xf*0.005), int(yf-tv.y*1.1)), 
                      (0, 0), 0, taille, 0, GRAY)
        start.dessine((int(xf*0.25), int(yf*0.92)), True)
        sett.dessine((int(xf*0.5), int(yf*0.92)))
        quit.dessine((int(xf*0.75), int(yf*0.92)))
    else:
        param.dessine()

while not fen.jeuDoitFermer():
    begin_drawing()
    clear_background(BLACK)
    if partie.timeline == 0:
        accueil()
    else:
        partie.dessine()
    end_drawing()

fen.finDuJeu()