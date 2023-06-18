from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from ui.blocTexte import BlocTexte
from jeux.Jeu_1.objets.Bateau import Bateau

class OrgaFen:
    def __init__(self, bateau1: Bateau, bateau2: Bateau) -> None:
        self.setbateaux(bateau1, bateau2)
        m = load_image("jeux/Jeu_1/images/Icones/marin.png")
        image_resize(m, int(xf*0.065), int(xf*0.065))
        self.marin = load_texture_from_image(m)
        unload_image(m)
        # Dimensions
        self.largeur = int(xf*0.5)
        self.hauteur = int(yf*0.8)
        # Autres
        self.titre = BlocTexte("ORGANISATION", police1, int(yf*0.04), [self.largeur, ''])
        # Boutons
        #self.opt = [[Bouton(TB1o, BTV, "CONTINUER", '', [self.portailAustral]), "JEU"],
         #           [Bouton(TB1o, BTNOIR, "PARAMETRES", '', [self.portailAustral]), "ANOVEL_OPTIONS"],
         #           [Bouton(TB1o, BTNOIR, "MENU PRINCIPAL", '', [self.portailAustral]), "ANOVEL_MENU"],
         #           [Bouton(TB1o, BTDANGER, "QUITTER", '', [self.portailAustral]), "QUITTE"]]
        self.gm1 = Grille(int(xf*0.25), [False])
        #self.gm1.ajouteElement(self.opt[0][0], 0, 0)
        #self.gm1.ajouteElement(self.opt[1][0], 0, 1)
        self.gm2 = Grille(int(xf*0.25), [False])
        #self.gm2.ajouteElement(self.opt[2][0], 0, 0)
        self.gm3 = Grille(int(xf*0.25), [False])
        #self.gm3.ajouteElement(self.opt[3][0], 0, 0)
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 170]
        self.hauteurContenu = [int(yf*1.1), int(yf/2-self.hauteur/2)]

    def dessine(self) -> None:
        if not self.ok and not self.playAnim:
            self.playAnim = True
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        draw_rectangle(int(xf/2-self.largeur/2-2), y-2, self.largeur+4, self.hauteur+4, [192, 150, 9, 255])
        draw_rectangle(int(xf/2-self.largeur/2), y, self.largeur, self.hauteur, WHITE)
        self.titre.dessine([[int(xf/2), int(y+self.titre.getDims()[1]/2)], 'c'], BLACK)
        y += int(self.titre.getDims()[1] + ecart)
        self.dessineBateau(y, 0)
        y = self.dessineBateau(y, 1, False)
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

    def dessineBateau(self, y: int, idBat: int, gauche: bool = True) -> int:
        total = self.bat[0].marins + self.bat[1].marins
        espace = int(yf*0.03)
        hbarre = int(yf*0.26)
        lbarre = int(xf*0.02)
        bat = self.bat[idBat]
        y += int(espace/2)
        texte = f"{bat.marinsi} marins en\ndebut de partie"
        tt = measure_text_ex(police2, texte, int(yf*0.025), 0)
        h = int(bat.marins*hbarre/total)
        tm = measure_text_ex(police2, str(bat.marins), int(yf*0.03), 0)
        couleurFondRec = [182, 231, 247, 255]
        couleurJauge = [12, 106, 156, 255]
        couleurContenu = [80, 224, 250, 255]
        couleurTexteRec = BLACK
        couleurTexteJauge = WHITE
        if gauche:
            x = int(xf/2-self.largeur*0.46)
            draw_texture(bat.images[0], x, int(y+hbarre*0.7-bat.images[0].height/2), WHITE)
            draw_rectangle_rounded([x, int(y+hbarre*0.7+bat.images[0].height*0.9), int(tt.x*1.1), int(tt.y*1.1)], 0.15, 30, couleurFondRec)
            draw_text_ex(police2, texte, (int(x+tt.x*0.05), int(y+hbarre*0.7+bat.images[0].height*0.9+tt.y*0.05)), int(yf*0.025), 0, couleurTexteRec)
            x += bat.images[0].width + espace
            draw_texture(self.marin, int(x+lbarre/2-self.marin.width/2), y, WHITE)
            y += self.marin.height
            draw_rectangle(x, y, lbarre, hbarre, couleurJauge)
            draw_rectangle(x, int(y+hbarre-h), lbarre, h, couleurContenu)
            draw_circle(int(x+lbarre*1.9), int(y+hbarre*0.32), int(lbarre/2), couleurJauge)
            draw_text_ex(police2, str(bat.marins), (int(x+lbarre*1.9-tm.x/2), int(y+hbarre*0.32-tm.y/2)), int(yf*0.03), 0, couleurTexteJauge)
        else:
            x = int(xf/2+self.largeur*0.46)
            draw_texture(bat.images[0], int(x-bat.images[0].width), int(y+hbarre*0.7-bat.images[0].height/2), WHITE)
            draw_rectangle_rounded([int(x-bat.images[0].width), int(y+hbarre*0.7+bat.images[0].height*0.9), int(tt.x*1.1), int(tt.y*1.1)], 0.15, 30, couleurFondRec)
            draw_text_ex(police2, texte, (int(x-bat.images[0].width+tt.x*0.05), int(y+hbarre*0.7+bat.images[0].height*0.9+tt.y*0.05)), int(yf*0.025), 0, couleurTexteRec)
            x -= bat.images[0].width + espace
            draw_texture(self.marin, int(x-lbarre/2-self.marin.width/2), y, WHITE)
            y += self.marin.height
            draw_rectangle(x-lbarre, y, lbarre, hbarre, couleurJauge)
            draw_rectangle(x-lbarre, int(y+hbarre-h), lbarre, h, couleurContenu)
            draw_circle(int(x-lbarre*1.9), int(y+hbarre*0.32), int(lbarre/2), couleurJauge)
            draw_text_ex(police2, str(bat.marins), (int(x-lbarre*1.9-tm.x*0.55), int(y+hbarre*0.32-tm.y/2)), int(yf*0.03), 0, couleurTexteJauge)
        return int(y + hbarre + espace)

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

    def setbateaux(self, bateau1: Bateau, bateau2: Bateau) -> None:
        self.bat = [bateau1, bateau2]