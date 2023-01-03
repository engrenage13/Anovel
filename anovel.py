from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from systeme.set import startSet
from systeme.verif import fichierExiste, verifSauvegarde, scan
from BN.partie import Partie
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from parametres.parametres import Parametres

fen = Fenetre()
if not fichierExiste():
    verifSauvegarde()
scan()
startSet()
partie = Partie(fen)
param = Parametres()

# Boutons
Gstart = Grille(int(xf*0.15), [False])
Gset = Grille(int(xf*0.15), [False])
Gquit = Grille(int(xf*0.15), [False])
Gstart.ajouteElement(Bouton(TB1o, BTV, "Jouer", '', [partie.nouvelleEtape]), 0, 0)
Gset.ajouteElement(Bouton(TB1o, BTNOIR, "Parametres", '', [param.ouvre]), 0, 0)
Gquit.ajouteElement(Bouton(TB1o, BTDANGER, "Quitter", '', [fen.switchEtat]), 0, 0)

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
        draw_text_pro(police2i, f"{version} - {etatVersion.lower()}", (int(xf*0.005), int(yf-tv.y*1.1)), 
                      (0, 0), 0, taille, 0, GRAY)
        Gstart.dessine(int(xf*0.25-Gstart.largeur/2), int(yf*0.92-Gstart.hauteur/2))
        Gset.dessine(int(xf*0.5-Gset.largeur/2), int(yf*0.92-Gset.hauteur/2))
        Gquit.dessine(int(xf*0.75-Gquit.largeur/2), int(yf*0.92-Gquit.hauteur/2))
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