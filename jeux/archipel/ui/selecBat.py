from systeme.FondMarin import xf, yf, draw_rectangle_rounded, draw_texture, BTANNULE, TB2n, is_key_pressed
from jeux.archipel.ui.objets.Bateau import Bateau
from museeNoyee import poisson
from ui.bouton.bouton import Bouton

class SelecBat:
    """Le rectangle mettant en avant le bateau soustrait au tiroir.
    """
    def __init__(self) -> None:
        """Crée le rectangle.
        """
        self.contenu = None
        self.pos = (int(xf*0.06), int(yf*0.94))
        self.dims = (0, 0)
        self.btstop = Bouton(TB2n, BTANNULE, "ANNULER", 'images/ui/CroSom.png', [self.annulation])
        self.annule = False
        self.play = True
        # animation
        self.disparition()

    def dessine(self) -> None:
        """Dessine le rectangle et le bateau à l'intérieur.
        """
        draw_rectangle_rounded([self.pos[0], self.pos[1]-self.dims[1], self.dims[0], self.dims[1]], 0.1, 
                               30, [0, 12, 72, int(215*self.lum)])
        draw_texture(poisson, self.pos[0], int(self.pos[1]-(self.dims[1]-poisson.height)/2-poisson.height), [255, 255, 255, int(255*self.lum)])
        self.contenu.dessine()
        if self.lum >= 1 and self.play:
            self.btstop.dessine(int(self.pos[0]+self.dims[0]*0.98), int(self.pos[1]-self.dims[1]*0.97))
            if is_key_pressed(261):
                self.annulation()
        self.apparition()

    def setContenu(self, contenu: Bateau) -> None:
        """Modifie le contenu du rectangle.

        Args:
            contenu (Bateau): Le nouveau bateau qui doit apparaître dans le rectangle.
        """
        self.contenu = contenu
        self.dims = (int(contenu.image.width*1.3), int(contenu.image.height*1.1))
        self.contenu.setPos(int(contenu.image.width*0.6), int(self.pos[1]-self.dims[1]/2))
        self.annule = False

    def annulation(self) -> None:
        """Lance l'opération pour remettre le bateau dans le tiroir.
        """
        self.annule = True

    def apparition(self) -> None:
        """Animation d'apparition du rectangle.
        """
        l = int((self.pos[0]+self.contenu.image.width*0.55)-(self.contenu.image.width*0.6))
        val = 0.05
        if self.lum < 1:
            self.lum += val
            self.contenu.deplace(int(l*val), 0)

    def disparition(self) -> None:
        """Disparition du rectangle.
        """
        self.lum = 0.0