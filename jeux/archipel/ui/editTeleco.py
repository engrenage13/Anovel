from jeux.archipel.ui.objets.Bateau import Bateau
from systeme.FondMarin import draw_rectangle_lines_ex, WHITE, TB2n, PTIBT3, BTANNULE, is_key_pressed
from jeux.archipel.ui.cible import Cible, Case, Bateau
from ui.bouton.bouton import Bouton

class EditTeleco(Cible):
    """La télécommande qui permet de modifier l'orientation et la position d'un bateau.

    Args:
        Cible (Cible): Hérite de la cible.
    """
    def __init__(self, case: Case, bateau: Bateau) -> None:
        """Crée la télécommande.

        Args:
            case (Case): La case sur laquelle s'affiche la télécommande.
            bateau (Bateau): Le bateau sur lequel elle agît.
        """
        super().__init__(case, bateau)
        self.fini = False
        self.retire = False
        self.opt = {"nord": Bouton(TB2n, PTIBT3, "NORD", 'images/ui/haut.png', [self.auNord]),
                    "est": Bouton(TB2n, PTIBT3, "EST", 'images/ui/droite.png', [self.aLEst]),
                    "sud": Bouton(TB2n, PTIBT3, "SUD", 'images/ui/bas.png', [self.auSud]),
                    "ouest": Bouton(TB2n, PTIBT3, "OUEST", 'images/ui/gauche.png', [self.aLOuest]),
                    "horaire": Bouton(TB2n, PTIBT3, "PIVOTER A DROITE", 'images/ui/tourneHoraire.png', [self.tourneHoraire]),
                    "anti-horaire": Bouton(TB2n, PTIBT3, "PIVOTER A GAUCHE", 'images/ui/tourneAntiHoraire.png', [self.tourneAntiHoraire]),
                    "retirer": Bouton(TB2n, BTANNULE, "RETIRER LE BATEAU", 'images/ui/CroSom.png', [self.supBat]),
                    "valider": Bouton(TB2n, PTIBT3, "VALIDER", 'images/ui/check.png', [self.valide])}
        self.activeDep = {"nord": True, "est": True, "sud": True, "ouest": True}
        self.veutBouger = False

    def dessine(self) -> None:
        """Déssine la télécommande.
        """
        draw_rectangle_lines_ex([self.case.pos[0], self.case.pos[1], self.case.taille, self.case.taille], 
                                int(self.case.largeurBordure*2), WHITE)
        if self.play:
            self.opt["valider"].dessine(self.case.pos[0]+self.case.taille, self.case.pos[1]+self.case.taille)
            if is_key_pressed(32):
                self.valide()
            self.opt["retirer"].dessine(self.case.pos[0]+self.case.taille, self.case.pos[1])
            if is_key_pressed(261):
                self.supBat()
            self.opt["horaire"].dessine(self.case.pos[0], self.case.pos[1]+self.case.taille)
            if is_key_pressed(88):
                self.tourneHoraire()
            self.opt["anti-horaire"].dessine(self.case.pos[0], self.case.pos[1])
            if is_key_pressed(90):
                self.tourneAntiHoraire()
            if self.activeDep["nord"]:
                self.opt["nord"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1])
                if is_key_pressed(87):
                    self.auNord()
            if self.activeDep["est"]:
                self.opt["est"].dessine(self.case.pos[0]+self.case.taille, int(self.case.pos[1]+self.case.taille/2))
                if is_key_pressed(68):
                    self.aLEst()
            if self.activeDep["sud"]:
                self.opt["sud"].dessine(int(self.case.pos[0]+self.case.taille/2), self.case.pos[1]+self.case.taille)
                if is_key_pressed(83):
                    self.auSud()
            if self.activeDep["ouest"]:
                self.opt["ouest"].dessine(self.case.pos[0], int(self.case.pos[1]+self.case.taille/2))
                if is_key_pressed(65):
                    self.aLOuest()

    def setCase(self, case: Case) -> None:
        """Modifie la case de structure.

        Args:
            case (Case): La nouvelle case mère de la télécommande.
        """
        super().setCase(case)
        self.fini = self.veutBouger = False

    def setBateau(self, bateau: Bateau) -> None:
        """Modifie le bateau sur lequel agît la télécommande.

        Args:
            bateau (Bateau): Le nouveau bateau.
        """
        super().setBateau(bateau)
        self.retire = self.veutBouger = False

    def valide(self) -> None:
        """Désactive la télécommande.
        """
        self.fini = True

    def supBat(self) -> None:
        """Supprime le bateau pour le replacer dans le tiroir.
        """
        self.retire = True
        self.fini = True

    def tourneHoraire(self) -> None:
        """Tourne le bateau dans le sens horaire de 90°.
        """
        if self.case.estPleine():
            self.case.tourneBateaux(False)
        else:
            self.bateau.droite()

    def tourneAntiHoraire(self) -> None:
        """Tourne le bateau dans le sens anti-horaire de 90°.
        """
        if self.case.estPleine():
            self.case.tourneBateaux()
        else:
            self.bateau.gauche()

    def auNord(self) -> None:
        """Déplace le bateau sur la case située au nord de la case mère.
        """
        self.veutBouger = "n"

    def aLEst(self) -> None:
        """Déplace le bateau sur la case située à l'est de la case mère.
        """
        self.veutBouger = "e"

    def auSud(self) -> None:
        """Déplace le bateau sur la case située au sud de la case mère.
        """
        self.veutBouger = "s"

    def aLOuest(self) -> None:
        """Déplace le bateau sur la case située à l'ouest de la case mère.
        """
        self.veutBouger = "o"