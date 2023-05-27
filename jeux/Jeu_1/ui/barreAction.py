from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from museeNoyee import minicoeur, minimarin

class BarreAction:
    def __init__(self, joueurs: list, passe) -> None:
        self.joueurs = joueurs
        self.actuel = 0
        # boutons
        self.passe = Bouton(TB2n, PTIBT1, "PASSE", 'images/ui/passer+.png', [passe])
        # dimensions
        self.hauteur = int(yf*0.07)

    def dessine(self) -> None:
        draw_rectangle(0, yf-self.hauteur, xf, yf, [80, 80, 80, 150])
        self.passe.dessine(int(xf-self.passe.getDims()[0]*0.7), int(yf-self.hauteur/2))
        self.dessineInfoBat()

    def dessineInfoBat(self) -> None:
        bateau = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        colFond = [24, 22, 22, 170]
        x = int(xf*0.005)
        y = int(yf-self.hauteur+yf*0.007)
        draw_rectangle(x, y, int(xf*0.136), int(yf*0.025), colFond)
        draw_texture(minicoeur, x, y, WHITE)
        x += int(xf*0.015)
        y += int(yf*0.0028)
        draw_rectangle(x, y, int(xf*0.12), int(yf*0.02), [230, 183, 183, 255])
        draw_rectangle(x, y, int((xf*0.12)*(bateau.vie/bateau.pvi)), int(yf*0.02), RED)
        x += int(xf*0.004)
        y -= int(yf*0.0008)
        draw_text_ex(police2, str(bateau.vie)+"/"+str(bateau.pvi), (x, y), int(yf*0.02), 0, WHITE)
        x = int(xf*0.005)
        y += int(yf*0.03)
        draw_rectangle(x, y, int(xf*0.04), int(yf*0.025), colFond)
        draw_texture(minimarin, x, y, WHITE)
        x += int(xf*0.019)
        y += int(yf*0.003)
        draw_text_ex(police2, str(bateau.marins), (x, y), int(yf*0.02), 0, WHITE)

    def rejouer(self) -> None:
        self.actuel = 0