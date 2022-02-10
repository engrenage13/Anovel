from random import *
from FondMarin import *
from placement import *
from objets.Joueur import Joueur
from objets.animations import quadriDeco, plusDeTuile

dpd = xf-tlatba

def jouer(event):
    fond.delete('accueil')
    fond.create_rectangle(0, yf*0.05, tlatba, yf, fill='black', tags=('pg'))
    fond.create_rectangle(dpd, yf*0.05, xf, yf, fill='black', tags=('pd'))
    fond.create_text(xf*0.015, yf*0.987, text=version, font=Lili1, fill=gris)
    fond.create_rectangle(dpd+tlatba*0.1, (yf*0.945)-(yf*0.84/10), dpd+tlatba*0.9, yf*0.945, fill="#333333", width=4, 
                          tags=('inst', 'valid', 'btV'))
    fond.create_text(dpd+tlatba*0.5, (yf*0.945)-(yf*0.84/20), text="VALIDER LE PLAN", font=Poli2, fill='white', 
                     tags=('inst', 'valid'))
    # Joueur 1
    Joueur1 = Joueur(1, liBat1)
    # Joueur 2
    Joueur2 = Joueur(2, liBat2, True)

    fond.create_rectangle(0, 0, xf, yf*0.05, fill=mauve)
    fond.create_text(xf*0.1, yf*0.027, text=(f"{Joueur1.nom} - Installation"), font=Poli1, fill='white', tag='titre')
    fond.create_text(xf*0.985, yf*0.022, text="x", font=Lili3, fill='red', tag='auRevoir')
    fond.after(100, plusDeTuile)
        
def auRevoir(event): # Ferme le jeu.
    Fen.quit()

fond.create_rectangle(0, 0, xf, yf, fill='black', tag='accueil')
fond.create_text(xf*0.5, yf*0.4, text=TITRE_F, font=Poli3, fill=bleu2, tags=('accueil', 'plafDec'))
fond.create_text(xf*0.66, yf*0.475, text=version, font=Lili2, fill=gris, tag='accueil')
quadriDeco()
fond.create_rectangle(xf*0.4, yf*0.6, xf*0.6, yf*0.7, fill=bleuBt, width=4, outline='black', 
                      tags=('start', 'accueil'))
fond.create_text(xf*0.5, yf*0.65, text="Jouer", font=Poli2, fill='white', tags=('start', 'accueil'))
fond.create_rectangle(xf*0.4, yf*0.72, xf*0.6, yf*0.82, fill=gris, width=4, outline='black', 
                      tags=('auRevoir', 'accueil'))
fond.create_text(xf*0.5, yf*0.77, text="Quitter", font=Poli2, fill='white', tags=('auRevoir', 'accueil'))

fond.tag_bind('auRevoir', '<Button-1>', auRevoir)
fond.tag_bind('start', '<Button-1>', jouer)

Fen.title(TITRE_F)
Fen.attributes('-fullscreen', True)
Fen.mainloop()