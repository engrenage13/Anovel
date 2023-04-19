from systeme.FondMarin import xf, yf, draw_rectangle, Color, police1
from ui.blocTexte import BlocTexte
from jeux.Jeu_1.fonctions.deplacement import glisse

class Banniere:
    def __init__(self, texte: str, hauteur: int, couleur: Color, gauche: bool = True) -> None:
        self.sens = gauche
        self.longueur = int(xf*0.6)
        self.hauteur = int(yf*0.12)
        self.couleur = couleur
        self.titre = BlocTexte(texte, police1, int(yf*0.1), [int(xf*0.35), int(yf*0.08)])
        if self.sens:
            self.pos = (-int(xf*0.2), hauteur)
            self.dest = (0, hauteur)
        else:
            self.pos = (int(xf*0.6), hauteur)
            self.dest = (xf-self.longueur, hauteur)

    def dessine(self) -> None:
        draw_rectangle(self.pos[0], self.pos[1], self.longueur, self.hauteur, self.couleur)
        if self.sens:
            self.titre.dessine([[int(self.pos[0]+xf*0.21), int(self.pos[1]+self.hauteur/7)], 'no'], alignement='g')
        else:
            self.titre.dessine([[int(self.pos[0]+xf*0.39), int(self.pos[1]+self.hauteur/7)], 'ne'], alignement='d')
        if not self.auBoutDuChemin():
            self.pos = glisse(self.pos, self.dest, int(xf*0.001))

    def auBoutDuChemin(self) -> bool:
        rep = False
        if self.sens and self.pos[0] >= self.dest[0]:
            rep = True
        elif not self.sens and self.pos[0] <= self.dest[0]:
            rep = True
        return rep