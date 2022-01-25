from FondMarin import fond, xf, yf, Poli2, Poli3, Lili3, bleu2, vertFluo, gris, mer
from objets.animations import quadriDeco

def ecranFin(joueur: str = "Personne") -> None:
    fond.delete('pointeur')
    fond.create_rectangle(0, 0, xf, yf, fill='black', tag='ecranFin')
    fond.create_text(xf*0.5, yf*0.4, text=joueur, font=Poli3, fill=bleu2, tags=('ecranFin', 'plafDec'))
    fond.create_text(xf*0.5, yf*0.5, text="A Gagné !", font=Lili3, fill=vertFluo, tag='ecranFin')
    quadriDeco([gris, 'red']+mer, 'ecranFin')
    fond.create_rectangle(xf*0.4, yf*0.65, xf*0.6, yf*0.75, fill='red', width=4, outline='black', 
                        tags=('auRevoir', 'ecranFin'))
    fond.create_text(xf*0.5, yf*0.7, text="Quitter", font=Poli2, fill='white', tags=('auRevoir', 'ecranFin'))