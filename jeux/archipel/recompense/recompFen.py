from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.blocTexte import BlocTexte
from jeux.archipel.objets.Bateau import Bateau
from jeux.archipel.objets.Joueur import Joueur
from jeux.archipel.recompense.vignette import Vignette
from jeux.archipel.icones import minicoeur, minimarin, minifleche, minidegats
from jeux.archipel.recompense.creeJoueur import creeJoueur

class RecompFen:
    """La fenêtre de récompenses pour un abordage réussi.
    """
    def __init__(self, b1: list[Bateau, Joueur] = creeJoueur(0), b2: list[Bateau, Joueur] = creeJoueur(1)) -> None:
        """Crée la fenêtre.

        Args:
            j1 (list[Bateau, Joueur], optional): Le premier bateau qui participe et son propriétaire.
            j2 (list[Bateau, Joueur], optional): Le deuxième bateau qui participe et son propriétaire.
        """
        # Dimensions
        self.largeur = int(xf*0.7)
        self.hauteur = int(yf*0.77)
        self.hauteurTab = int(self.hauteur*0.35)
        self.largeurCadBat = int(self.largeur*0.5)
        self.fini = False
        # Animations
        self.playAnim = False
        self.ok = False
        self.opac = [0, 170]
        self.hauteurContenu = [int(yf*1.1), int(yf/2-self.hauteur/2)]
        # Bateaux
        self.vainqueur: list[Bateau, Joueur] = None
        self.perdant: list[Bateau, Joueur] = None
        self.setBateaux(b1, b2)
        # Vignettes
        self.degats = self.vainqueur[0].marins-self.perdant[0].marins-1
        self.vivm = Vignette("VOLER 1 MARIN", "jeux/archipel/images/Icones/marin.png")
        self.vivbm = Vignette("VOLER LE BATEAU ET SON EQUIPAGE", "jeux/archipel/images/Icones/cle.png")
        self.viex = Vignette(f"INFLIGER {self.degats} {'DEGAT' if self.degats == 1 else 'DEGATS'}", "jeux/archipel/images/Icones/explosif.png")
        self.vivb = Vignette("VOLER LE BATEAU", "jeux/archipel/images/Icones/cle.png")
        self.actions = (self.vivm, self.vivbm, self.viex, self.vivb)
        self.act = self.verifActionsPossibles()
        # Titres
        self.tt1_1 = self.vainqueur[1].nom.upper()
        self.tt1_2 = " GAGNE L'ABORDAGE"
        self.mt1_1 = measure_text_ex(police1, self.tt1_1, yf*0.04, 0)
        self.titre2 = BlocTexte("ET DOIT CHOISIR UNE RECOMPENSE", police1, int(yf*0.04))
        self.titre3 = BlocTexte("JE NE VEUX PAS DE RECOMPENSE", police1, int(yf*0.02))
        self.titre4 = BlocTexte("NAVIRE PERDANT", police1, int(yf*0.03))
        # Bouton
        self.croix = Bouton(TB2n, PTIBT2, "PASSER", 'images/ui/CroSom.png', [self.passe])
        # Textures
        lfleche = int(self.largeur*0.029)
        fle = load_image("images/ui/droite.png")
        image_resize(fle, lfleche, lfleche)
        self.fleche = load_texture_from_image(fle)
        unload_image(fle)

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        if self.ok and not self.fini and self.playAnim:
            self.playAnim = False
        draw_rectangle(0, 0, xf, yf, [41, 35, 45, self.opac[0]])
        ecart = int(yf*0.03)
        y = self.hauteurContenu[0]
        draw_rectangle(int(xf/2-self.largeur/2-2), y-2, self.largeur+4, self.hauteur+4, [192, 150, 9, 255])
        draw_rectangle(int(xf/2-self.largeur/2), y, self.largeur, self.hauteur, [45, 46, 60, 255])
        y += int(ecart/4)
        draw_text_ex(police1, self.tt1_1, (int(xf/2-self.largeur/2+ecart/2), int(y)), yf*0.04, 0, self.vainqueur[1].couleur)
        draw_text_ex(police1, self.tt1_2, (int(xf/2-self.largeur/2+ecart/2+self.mt1_1.x), int(y)), yf*0.04, 0, WHITE)
        y -= int(ecart/4)
        self.titre3.dessine([[int(xf/2+self.largeur/2-yf*0.005-self.croix.largeur-self.fleche.width*1.35-self.titre3.getDims()[0]), int(y+self.croix.largeur/2+yf*0.005-self.titre3.getDims()[1]/2)], 'no'], WHITE)
        draw_texture(self.fleche, int(xf/2+self.largeur/2-yf*0.005-self.croix.largeur-self.fleche.width*1.15), int(y+yf*0.005+self.croix.largeur/2-self.fleche.height/2), WHITE)
        self.croix.dessine(int(xf/2+self.largeur/2-yf*0.005-self.croix.largeur/2), int(y+self.croix.largeur/2+yf*0.005))
        y += int(self.mt1_1.y+ecart/4)
        self.titre2.dessine([[int(xf/2-self.largeur/2+ecart/2), int(y)], 'no'], WHITE)
        y += int(self.titre2.getDims()[1] + ecart)
        self.dessineVignettes(y)
        y += int(self.vivm.getDims()[1] + ecart)
        x = int(xf/2-self.largeurCadBat/2)
        self.dessineBateauPerdant(x, y)
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

    def dessineBateauPerdant(self, x: int, y: int) -> None:
        """Dessine le bloc avec le bateau qui a perdu.

        Args:
            x (int): abscisse du coin supérieur gauche.
            y (int): ordonnée du coin supérieur gauche.
        """
        perdant = self.perdant[0]
        couleurFondRec = [59, 91, 103, 255]
        draw_rectangle_rounded([x, y, self.largeurCadBat, self.hauteurTab], 0.04, 30, couleurFondRec)
        px = int(int(str(x))+self.largeurCadBat*0.02)
        py = int(int(str(y))+self.hauteurTab*0.01)
        ecarty = int(yf*0.01)
        self.titre4.dessine([[px, py], 'no'], WHITE, 'g')
        py += int(self.titre4.getDims()[1]+ecarty)
        img = perdant.image
        ecartx = int(self.largeurCadBat*0.09)
        draw_texture(img, int(x+self.largeurCadBat-ecartx-img.width), int(y+self.hauteurTab/2-img.height/2), WHITE)
        # stats
        stats = [[minicoeur, perdant.vie], [minimarin, perdant.marins], [minidegats, perdant.degats], [minifleche, perdant.pm]]
        lsta = int(self.largeurCadBat*0.06)
        hsta = int(minicoeur.height*1.2)
        for i in range(len(stats)):
            draw_texture(stats[i][0], int(px+lsta*0.01), int(py+minicoeur.height*0.1), WHITE)
            tt = measure_text_ex(police1, str(stats[i][1]), yf*0.026, 0)
            draw_text_ex(police1, str(stats[i][1]), (int(px+lsta*0.01+minicoeur.width*1.1), int(py+minicoeur.height*0.63-tt.y/2)), yf*0.026, 0, WHITE)
            if i != 0 and i%8 == 0:
                px += int(lsta+ecartx/4)
                py = int(y+self.hauteurTab*0.01+self.titre4.getDims()[1]+ecarty)
            else:
                py += hsta

    def verifActionsPossibles(self) -> list[Vignette]:
        """Met en place la liste des récompenses possibles pour le vainqueur.

        Returns:
            list[Vignette]: Les récompenses accessibles.
        """
        actions = []
        perdant = self.perdant[0]
        vainqueur = self.vainqueur[0]
        if perdant.marins > 0:
            actions.append(self.actions[0])
            if vainqueur.marins != perdant.marins:
                if (vainqueur.marins > perdant.marins and vainqueur.marins-perdant.marins >= 5):
                    actions.append(self.actions[1])
        else:
            actions.append(self.actions[3])
        if (vainqueur.marins > perdant.marins and vainqueur.marins-perdant.marins-1 > 0):
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

    def setBateaux(self, b1: list[Bateau, Joueur], b2: list[Bateau, Joueur]) -> None:
        """Modifie les bateaux utilisés pour le calcul des récompenses.

        Args:
            b1 (list[Bateau, Joueur]): Le premier bateau et son propriétaire.
            b2 (list[Bateau, Joueur]): Le deuxième bateau et son propriétaire.
        """
        passe = False
        if b1[0].marins > b2[0].marins:
            self.vainqueur = b1
            self.perdant = b2
        else:
            self.vainqueur = b2
            self.perdant = b1
            if b2[0].marins == b1[0].marins:
                passe = True
                self.passe()
        if not passe:
            self.playAnim = True
        print(self.vainqueur[0], self.perdant[0])

    def passe(self) -> None:
        """Passe le choix d'une récompense.
        """
        self.fini = True
        if self.opac[0] > 0:
            self.playAnim = True

    def clicSurVignette(self, vignette: int) -> None:
        """Met fin à l'affichage de la fenêtre si une vignette est cliquée.

        Args:
            vignette (int): La vignette testée.
        """
        action = self.actions.index(self.act[vignette])
        if self.actions[action] == self.vivm:
            self.vainqueur[0] + 1
            self.perdant[0] - 1
        elif self.actions[action] == self.vivb or self.actions[action] == self.vivbm:
            self.perdant[1] - self.perdant[0]
            self.vainqueur[1] + self.perdant[0]
        elif self.actions[action] == self.viex:
            self.perdant[0].setNbPV(self.perdant[0].vie - self.degats)
            if self.perdant[0].coule:
                self.vainqueur[1].nbelimination += 1
        self.fini = True
        self.actions[action].check = False
        self.playAnim = True