from FondMarin import *
from partie import Partie
from objets.animations import quadriDeco, plusDeTuile
from ui.bouton import Bouton

def jouer():
    jeu = Partie()
    jeu.miseEnPlace()
    fond.after(100, plusDeTuile)

fond.create_rectangle(0, 0, xf, yf, fill='black', tag='accueil')
fond.create_text(xf*0.5, yf*0.4, text=TITRE_F, font=Poli3, fill=bleu2, tags=('accueil', 'plafDec'))
fond.create_text(xf*0.66, yf*0.475, text=version, font=Lili2, fill=gris, tag='accueil')
quadriDeco()
start = Bouton(jouer, "Jouer", bleuBt, nom=['start', 'accueil'])
start.dessine((xf/2, yf*0.65))
quit = Bouton(auRevoir, "Quitter", nom=['auRevoir', 'accueil'])
quit.dessine((xf/2, yf*0.77))

Fen.title(TITRE_F)
Fen.attributes('-fullscreen', True)
Fen.mainloop()