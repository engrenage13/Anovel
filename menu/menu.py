from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from animations.etincelles import Etincelles
from random import randint

class Menu:
    def __init__(self) -> None:
        # Boutons
        self.opt = [[Bouton(TB1o, BTV, "Jouer", '', [self.portailBoreal]), "BN"], 
                    [Bouton(TB1n, PTIBT1, "Parametres", 'images/ui/rouage.png', [self.portailBoreal]), "ANOVEL_OPTIONS"],
                    [Bouton(TB1o, BTDANGER, "Quitter", 'images/ui/quitte.png', [self.portailBoreal]), "QUITTE"]]
        self.Gstart = Grille(int(xf*0.15), [False])
        self.Gopt = Grille(int(xf*0.17), [False], False)
        self.Gstart.ajouteElement(self.opt[0][0], 0, 0)
        self.Gopt.ajouteElement(self.opt[1][0], 0, 0)
        self.Gopt.ajouteElement(self.opt[2][0], 1, 0)
        # Images
        bn = load_image('images/menu/bn.png')
        ratio = yf*0.3/bn.height
        image_resize(bn, int(bn.width*ratio), int(bn.height*ratio))
        self.ibn = load_texture_from_image(bn)
        unload_image(bn)
        # Animations
        self.etincelles = Etincelles([0, yf, xf, int(yf*0.005)], [YELLOW, BLUE, WHITE])
        self.alpha = 0
        self.monte = True
        self.timer = 0
        # Between the worlds
        self.play = False
        self.message = ""
        self.lu = True

    def dessine(self):
        self.animeFond()
        draw_rectangle_gradient_v(0, 0, xf, yf, BLACK, [0, 82, 172, 150])
        taille = int(yf*0.02)
        tv = measure_text_ex(police3i, version, taille, 0)
        draw_text_pro(police2i, f"{version} - {etatVersion.lower()}", (int(xf*0.005), int(yf-tv.y*1.1)), 
                    (0, 0), 0, taille, 0, GRAY)
        xbn = int(xf/2)
        draw_texture(self.ibn, int(xbn-self.ibn.width/2), int(yf*0.4-self.ibn.height/2), WHITE)
        ttit = int(yf*0.05)
        ttbn = measure_text_ex(police1, "BATAILLE NAVALE", ttit, 0)
        draw_rectangle_rounded((int(xbn-ttbn.x*0.6), int(yf*0.54-ttbn.y*0.6), int(ttbn.x*1.2), int(ttbn.y*1.2)), 0.2, 30, [30, 30, 30, 255])
        draw_text_pro(police1, "BATAILLE NAVALE", (int(xbn-ttbn.x*0.5), int(yf*0.54-ttbn.y*0.5)), (0, 0), 0, ttit, 0, WHITE)
        self.Gstart.dessine(int(xbn-self.Gstart.largeur/2), int(yf*0.65-self.Gstart.hauteur/2))
        self.Gopt.dessine(int(xf*0.98-self.Gopt.largeur), int(yf*0.07-self.Gopt.hauteur/2))

    def animeFond(self):
        self.etincelles.dessine()
        draw_rectangle(0, 0, xf, yf, [0, 117, 44, self.alpha])
        max = 100
        if (self.alpha == max or self.alpha == 0) and self.timer > 0:
            self.timer -= 1
        else:
            if self.monte:
                if self.alpha == max:
                    self.monte = False
                    self.timer = randint(2, max)
                else:
                    self.alpha += 1
            else:
                if self.alpha == 0:
                    self.monte = True
                    self.timer = randint(2, max)
                else:
                    self.alpha -= 1

    # Between the worlds
    def portailBoreal(self) -> None:
        i = 0
        v = False
        while i < len(self.opt) and not v:
            if self.opt[i][0].getContact():
                v = True
                self.nouveauMessage(self.opt[i][1])
            else:
                i += 1

    def nouveauMessage(self, message: str) -> None:
        self.message = message
        self.lu = False