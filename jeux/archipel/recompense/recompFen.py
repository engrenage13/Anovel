from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.blocTexte import BlocTexte
from jeux.archipel.objets.Bateau import Bateau
from jeux.archipel.recompense.vignette import Vignette
from jeux.archipel.icones import coeur, marin, fleche, degats

class RecompFen:
    """La fenêtre de récompenses pour un abordage réussi.
    """
    def __init__(self, allie: Bateau = Bateau("", "jeux/archipel/images/Bateaux/gafteur.png", 5, 10, 0, 1, [0, 0, 0, 0]), ennemi: Bateau = Bateau("", "jeux/archipel/images/Bateaux/gafteur.png", 4, 1, 0, 0, [0, 0, 0, 0])) -> None:
        """Crée la fenêtre.

        Args:
            allie (Bateau, optional): Le bateau qui a gagné l'abordage. Defaults to Bateau("", "jeux/archipel/images/Bateaux/gbb.png", 5, 10, 0, 1, [0, 0, 0, 0]).
            ennemi (Bateau, optional): Le bateau qui a perdu l'abordage. Defaults to Bateau("", "jeux/archipel/images/Bateaux/gbb.png", 4, 1, 0, 0, [0, 0, 0, 0]).
        """
        # Dimensions
        self.largeur = int(xf*0.7)
        self.hauteur = int(yf*0.8)
        self.largeurPasse = int(self.largeur*0.2)
        self.hauteurPasse = int(self.hauteur*0.35)
        self.largeurCadBat = int(self.largeur*0.738)
        # Titres
        self.titre1 = BlocTexte("VOUS GAGNEZ L'ABORDAGE !", police1, int(yf*0.04))
        self.titre2 = BlocTexte("CHOISISSEZ UNE RECOMPENSE", police1, int(yf*0.04))
        self.titre3 = BlocTexte("JE NE VEUX PAS DE RECOMPENSES", police1, int(yf*0.03), [self.largeurPasse, ''])
        self.titre4 = BlocTexte("NAVIRE ADVERSE", police1, int(yf*0.03))
        # Boutons
        self.opt = [Bouton(TB2n, PTIBT2, "PASSER", 'images/ui/CroSom.png', [self.passe]),
                    Bouton(TB1o, BTX, "PASSER", '', [self.passe])]
        # Vignettes
        self.vivm = Vignette("VOLER 1 MARIN", "jeux/archipel/images/Icones/marin.png")
        self.vivbm = Vignette("VOLER LE BATEAU ET SON EQUIPAGE", "jeux/archipel/images/Icones/cle.png")
        self.viex = Vignette("INFLIGER DES DEGATS SUPPLEMENTAIRES", "jeux/archipel/images/Icones/explosif.png")
        self.vivb = Vignette("VOLER LE BATEAU", "jeux/archipel/images/Icones/cle.png")
        self.actions = (self.vivm, self.vivbm, self.viex, self.vivb)
        # Bateaux
        self.setBateaux(allie, ennemi)
        # Animations
        self.playAnim = True
        self.ok = False
        self.opac = [0, 170]
        self.hauteurContenu = [int(yf*1.1), int(yf/2-self.hauteur/2)]

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        if self.ok and self.valide == -1 and self.playAnim:
            self.playAnim = False
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        draw_rectangle(int(xf/2-self.largeur/2-2), y-2, self.largeur+4, self.hauteur+4, [192, 150, 9, 255])
        draw_rectangle(int(xf/2-self.largeur/2), y, self.largeur, self.hauteur, WHITE)
        self.titre1.dessine([[int(xf/2-self.largeur/2+ecart/2), int(y)], 'no'], BLACK)
        self.opt[0].dessine(int(xf/2+self.largeur/2-yf*0.005-self.opt[0].largeur/2), int(y+self.opt[0].largeur/2+yf*0.005))
        y += int(self.titre1.getDims()[1] + ecart/4)
        self.titre2.dessine([[int(xf/2-self.largeur/2+ecart/2), int(y)], 'no'], BLACK)
        y += int(self.titre2.getDims()[1] + ecart)
        self.dessineVignettes(y)
        y += int(self.vivm.getDims()[1] + ecart)
        x = int(xf/2-self.largeur*0.48)
        self.dessinePasse(x, y)
        x += self.largeurPasse + ecart
        self.dessineBateauAdverse(x, y)
        if self.playAnim:
            if not self.ok:
                self.anims(True)
            else:
                self.anims(False)

    def dessineVignettes(self, y: int) -> None:
        """Dessine les vignettes (récompenses disponibles).

        Args:
            y (int): La hauteur à laquelle les vignettes doivent être déssinés.
        """
        actions = self.act
        x = int(xf/2)
        espace = int(xf*0.02)
        if len(actions)%2 == 1:
            x -= int(self.vivm.getDims()[0]/2)
            if len(actions)-1 > 0:
                for i in range(int((len(actions)-1)/2)):
                    x -= int(espace+actions[i].getDims()[0])
        else:
            for i in range(int(len(actions)/2)):
                x -= int(actions[i].getDims()[0])
                if i == 0:
                    x -= int(espace/2)
                else:
                    x -= espace
        for j in range(len(actions)):
            actions[j].dessine(x, y)
            x += int(actions[j].getDims()[0] + espace)
            if actions[j].check:
                self.clicSurVignette(j)

    def dessinePasse(self, x: int, y: int) -> None:
        """Dessine le bloc avec le bouton pour passer.
        """
        couleurFondRec = [255, 180, 196, 235]
        draw_rectangle_rounded([x, y, self.largeurPasse, self.hauteurPasse], 0.15, 300, couleurFondRec)
        px = int(int(str(x))+self.largeurPasse*0.03)
        py = int(int(str(y))+self.hauteurPasse*0.01)
        self.titre3.dessine([[px, py], 'no'], BLACK, 'g')
        #py += int(yf*0.2)
        self.opt[1].dessine(int(x+self.largeurPasse/2), int(y+self.hauteurPasse*0.6))

    def dessineBateauAdverse(self, x: int, y: int) -> None:
        """Dessine le bloc avec le bateau adverse.

        Args:
            x (int): abscisse du coin supérieur gauche.
            y (int): ordonnée du coin supérieur gauche.
        """
        couleurFondRec = [180, 215, 255, 235]
        draw_rectangle_rounded([x, y, self.largeurCadBat, self.hauteurPasse], 0.15, 300, couleurFondRec)
        px = int(int(str(x))+self.largeurPasse*0.03)
        py = int(int(str(y))+self.hauteurPasse*0.01)
        ecarty = int(yf*0.01)
        self.titre4.dessine([[px, py], 'no'], BLACK, 'g')
        py += int(self.titre4.getDims()[1]+ecarty)
        img = self.bat[1].image
        ecartx = int(self.largeurCadBat*0.09)
        draw_texture(img, int(x+self.largeurCadBat-ecartx-img.width), int(y+self.hauteurPasse/2-img.height/2), WHITE)
        # stats
        stats = [[coeur, self.bat[1].vie], [marin, self.bat[1].marins], [fleche, self.bat[1].pm], [degats, self.bat[1].degats]]
        lsta = int(self.largeurCadBat*0.2)
        hsta = int(coeur.height*1.2)
        px += int(self.largeurCadBat*0.03)
        for i in range(len(stats)):
            draw_rectangle_gradient_h(px, py, lsta, hsta, [114, 125, 138, 200], [114, 125, 138, 0])
            draw_texture(stats[i][0], int(px+lsta*0.01), int(py+coeur.height*0.1), WHITE)
            tt = measure_text_ex(police1, str(stats[i][1]), yf*0.035, 0)
            draw_text_ex(police1, str(stats[i][1]), (int(px+lsta*0.01+coeur.width*1.1), int(py+coeur.height*0.63-tt.y/2)), yf*0.035, 0, BLACK)
            if i != 0 and i%2 == 0:
                px += int(lsta+ecartx/4)
                py = int(y+self.hauteurPasse*0.01+self.titre4.getDims()[1]+ecarty)
            else:
                py += hsta + ecarty

    def verifActionsPossibles(self) -> list[Vignette]:
        """Met en place la liste des récompenses possibles pour le vainqueur.

        Returns:
            list[Vignette]: Les récompenses accessibles.
        """
        actions = []
        if self.bat[1].marins > 0:
            actions.append(self.actions[0])
            if self.bat[0].marins != self.bat[1].marins:
                if (self.bat[0].marins > self.bat[1].marins and self.bat[0].marins-self.bat[1].marins >= 5) or (self.bat[0].marins < self.bat[1].marins and self.bat[1].marins-self.bat[0].marins >= 5):
                    actions.append(self.actions[1])
        else:
            actions.append(self.actions[3])
        if (self.bat[0].marins > self.bat[1].marins and self.bat[0].marins-self.bat[1].marins-1 > 0) or (self.bat[0].marins < self.bat[1].marins and self.bat[1].marins-self.bat[0].marins-1 > 0):
            actions.append(self.actions[2])
        return actions

    def anims(self, mode: bool) -> None:
        """Animation d'entrée et de sortie de la fenêtre.

        Args:
            mode (bool): False pour l'entrée, True pour la sortie.
        """
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
        """Modifie les bateaux utilisés pour le calcul des récompenses.

        Args:
            allie (Bateau): Le bateau vainqueur.
            ennemi (Bateau): Le bateau perdant.
        """
        self.bat = [allie, ennemi]
        self.valide = -1
        self.act = self.verifActionsPossibles()
        self.playAnim = True

    def passe(self) -> None:
        """Passe le choix d'une récompense.
        """
        self.valide = 0
        self.playAnim = True

    def clicSurVignette(self, vignette: int) -> None:
        """Met fin à l'affichage de la fenêtre si une vignette est cliquée.

        Args:
            vignette (int): La vignette testée.
        """
        indice = self.actions.index(self.act[vignette])
        if indice <= 2:
            self.valide = indice+1
        else:
            self.valide = 2
        self.actions[indice].check = False
        self.playAnim = True