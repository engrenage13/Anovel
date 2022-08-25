from systeme.FondMarin import *
from museeNoyee import croixLumineuse, croixSombre
from ui.clickIma import ClickIma
from parametres.menu import Menu

class Parametres:
    def __init__(self) -> None:
        """Crée la fenêtre des paramètres.
        """
        self.ouvert = False
        self.largeurLat = int(xf*0.25)
        self.menu = Menu("parametres/Categories.md", (0, int(yf*0.078), self.largeurLat, int(yf-yf*0.128)))
        self.croix = ClickIma([self.ferme], [croixSombre, croixLumineuse])

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        draw_rectangle(self.largeurLat, 0, xf, yf, [20, 20, 20, 255])
        self.dessineMenu()
        draw_rectangle(0, 0, self.largeurLat, int(yf*0.078), [107, 67, 237, 255])
        draw_text_pro(police1, "Parametres", (int(yf*0.02), int(yf*0.02)), (0, 0), 0, int(yf*0.05), 0, WHITE)
        self.dessineVersion()
        self.croix.dessine((xf-hbarre, int(hbarre*0.05)))

    def dessineMenu(self) -> None:
        """Permet de dessiner le menu latérale.
        """
        draw_rectangle(0, 0, self.largeurLat, yf, [60, 60, 60, 255])
        self.menu.dessine()

    def dessineVersion(self) -> None:
        """Dessine la partie indiquant la version du jeu.
        """
        draw_rectangle(0, yf-int(yf*0.05), self.largeurLat, int(yf*0.05), [10, 10, 10, 255])
        texte = f"{etatVersion.upper()} - {version}"
        taille = int(yf*0.03)
        tv = measure_text_ex(police2, texte, taille, 0)
        draw_text_pro(police2, texte, (int(xf*0.01), int(yf-tv.y*1.2)), (0, 0), 0, taille, 0, WHITE)

    def ouvre(self) -> None:
        """Permet d'ouvrir la fenêtre (fictivement).
        """
        self.ouvert = True
    
    def ferme(self) -> None:
        """Permet de fermer la fenêtre (fictivement).
        """
        self.ouvert = False