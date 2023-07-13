from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.blocTexte import BlocTexte
from jeux.Jeu_1.objets.Bateau import Bateau

class RecompFen:
    def __init__(self, allie: Bateau = Bateau("", "jeux/Jeu_1/images/Bateaux/gbb.png", 0, 1, 0, [0, 0, 0, 0], 0), ennemi: Bateau = Bateau("", "jeux/Jeu_1/images/Bateaux/gbb.png", 0, 1, 0, [0, 0, 0, 0], 0)) -> None:
        self.setBateaux(allie, ennemi)
        #m = load_image("jeux/Jeu_1/images/Icones/marin.png")
        # Dimensions
        self.largeur = int(xf*0.7)
        self.hauteur = int(yf*0.8)
        # Titres
        self.titre1 = BlocTexte("VOUS GAGNEZ L'ABORDAGE !", police1, int(yf*0.04))
        self.titre2 = BlocTexte("CHOISISSEZ UNE RECOMPENSE", police1, int(yf*0.04))
        # Boutons
        self.opt = [Bouton(TB2n, PTIBT2, "PASSER", 'images/ui/CroSom.png', [self.passe]),
                    Bouton(TB1o, BTX, "PASSER", '', [self.passe])]
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 170]
        self.hauteurContenu = [int(yf*1.1), int(yf/2-self.hauteur/2)]

    def dessine(self) -> None:
        couleurFondRec = [243, 123, 123, 255]
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        draw_rectangle(int(xf/2-self.largeur/2-2), y-2, self.largeur+4, self.hauteur+4, [192, 150, 9, 255])
        draw_rectangle(int(xf/2-self.largeur/2), y, self.largeur, self.hauteur, WHITE)
        self.titre1.dessine([[int(xf/2-self.largeur/2+ecart/2), int(y)], 'no'], BLACK)
        self.opt[0].dessine(int(xf/2+self.largeur/2-yf*0.005-self.opt[0].largeur/2), int(y+self.opt[0].largeur/2+yf*0.005))
        y += int(self.titre1.getDims()[1] + ecart/4)
        self.titre2.dessine([[int(xf/2-self.largeur/2+ecart/2), int(y)], 'no'], BLACK)
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

    def anims(self, mode: bool) -> None:
        if mode:
            if self.opac[0] < self.opac[1]:
                self.opac[0] += 2
            if self.hauteurContenu[0] > self.hauteurContenu[1]:
                self.hauteurContenu[0] -= int(yf*0.03)
            if self.opac[0] == self.opac[1] and self.hauteurContenu[0] <= self.hauteurContenu[1]:
                self.playAnim = False
                self.ok = True
        else:
            if self.opac[0] > 0:
                self.opac[0] -= 2
            if self.hauteurContenu[0] < int(yf*1.1):
                self.hauteurContenu[0] += int(yf*0.03)
            if self.opac[0] == 0 and self.hauteurContenu[0] >= int(yf*1.1):
                self.playAnim = False
                self.ok = False

    def setBateaux(self, allie: Bateau, ennemi: Bateau) -> None:
        self.bat = [allie, ennemi]
        self.valeursInitiales = [str(allie.marins), str(ennemi.marins)]
        self.valide = 1

    def passe(self) -> None:
        self.valide = 0
        self.playAnim = True