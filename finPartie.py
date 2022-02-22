from FondMarin import fond, xf, yf, Poli3, Lili3, bleu2, vertFluo, gris, mer, rouge, auRevoir
from objets.animations import quadriDeco
from ui.bouton import Bouton

def ecranFin(joueur: str = "Personne") -> None:
    fond.delete('pointeur')
    fond.create_rectangle(0, 0, xf, yf, fill='black', tag='ecranFin')
    fond.create_text(xf*0.5, yf*0.4, text=joueur, font=Poli3, fill=bleu2, tags=('ecranFin', 'plafDec'))
    fond.create_text(xf*0.5, yf*0.5, text="A Gagné !", font=Lili3, fill=vertFluo, tag='ecranFin')
    quadriDeco([gris, 'red']+mer, 'ecranFin')
    quit = Bouton(auRevoir, "Quitter", rouge, nom=['auRevoir', 'ecranFin'])
    quit.dessine((xf/2, yf*0.7))