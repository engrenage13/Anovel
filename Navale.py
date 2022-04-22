from FondMarin import *
from partie import Partie
from animations.Carrelage import Etincelle
from ui.bouton import Bouton

def jouer():
    jeu = Partie()
    jeu.miseEnPlace()
    etincelle.fin()

fond.create_rectangle(0, 0, xf, yf, fill='black', tag='accueil')
fond.create_text(xf*0.5, yf*0.4, text=TITRE_F, font=Poli3, fill=bleu2, tags=('accueil', 'plafDec'))
fond.create_rectangle(xf*0.6, yf*0.46, xf*0.678, yf*0.495, fill=bleu2, tag='accueil')
fond.create_text(xf*0.62, yf*0.4775, text="alpha", font=Lili2, fill=noir, tag='accueil')
fond.create_text(xf*0.658, yf*0.4775, text=version, font=Lili2, fill=blanc, tag='accueil')
etincelle = Etincelle()
etincelle.eblouissement()
start = Bouton(jouer, "Jouer", bleuBt, nom=['start', 'accueil'])
start.dessine((xf/2, yf*0.65))
quit = Bouton(auRevoir, "Quitter", nom=['auRevoir', 'accueil'])
quit.dessine((xf/2, yf*0.77))

Fen.title(TITRE_F)
Fen.attributes('-fullscreen', True)
Fen.mainloop()