from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from BN.Editeur.editeur import Editeur
from BN.objets.Joueur import Joueur
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from BN.attaque import Attaque
from BN.finPartie import FinPartie
from parametres.parametres import Parametres

class Partie:
    def __init__(self, fenetre: Fenetre) -> None:
        """Crée l'entité qui gère la totalité de la partie.

        Args:
            fenetre (Fenetre): La fenêtre affiché à l'écran.
        """
        self.fenetre = fenetre
        self.param = Parametres()
        self.grOpt = Grille(int(TB2n.hauteur*2+3*espaceBt), [False])
        self.grOpt.ajouteElement(Bouton(TB2n, PTIBT1, "PARAMETRES", 'images/ui/RouSom.png', [self.param.ouvre]), 0, 0)
        self.grOpt.ajouteElement(Bouton(TB2n, PTIBT1, "QUITTER", 'images/ui/CroSom.png', [fenetre.switchEtat]), 1, 0)
        self.joueurs = []
        self.timeline = 0
        self.creeJoueurs()
        self.editeur = Editeur(self.joueurs[0], self)
        self.baston = Attaque(self.joueurs[0], self.joueurs[1], self)

    def nouvelleEtape(self) -> None:
        """Incrémente le marqueur sur la chronologie de la partie.
        """
        self.timeline = self.timeline + 1
        if self.timeline == 2:
            self.editeur.setJoueur(self.joueurs[1])
        elif self.timeline == 4:
            win = [False]*len(self.joueurs)
            for i in range(len(self.joueurs)):
                if self.joueurs[i] == self.baston.gagnant:
                    win[i] = True
            self.ecranFin = FinPartie(list(zip(self.joueurs, win)), self.baston.tour, self)

    def dessine(self) -> None:
        """Dessine les éléments de la partie à l'écran.
        """
        if not self.param.ouvert:
            if self.timeline == 1 or self.timeline == 2:
                self.editeur.dessine()
            elif self.timeline == 3:
                self.baston.dessine()
            elif self.timeline == 4:
                self.baston.dessine()
                self.ecranFin.dessine()
                if self.ecranFin.saturation == 255:
                    self.nouvelleEtape()
            elif self.timeline == 5:
                self.ecranFin.dessine()
            self.grOpt.dessine(xf-self.grOpt.largeur, espaceBt)
        else:
            self.param.dessine()

    def getJoueurs(self) -> list:
        """Renvoie la liste des joueurs présents dans la partie.

        Raises:
            IndexError: Si aucun joueur n'a était créé.

        Returns:
            list: liste des joueurs.
        """
        if len(self.joueurs) == 0:
            raise IndexError("getJoueurs : Aucun joueur n'a était créé.")
        return self.joueurs

    def getJoueur(self, indice: int) -> object:
        """Renvoie un joueur en particulier

        Args:
            indice (int): L'indice du joueur que l'on cherche via la liste des joueurs `self.joueurs`.

        Raises:
            IndexError: _description_
            IndexError: _description_

        Returns:
            object: Un joueur (objet)
        """
        if indice < 0 or indice > 1:
            raise IndexError("getJoueur : L'indice fournis n'est pas recevable, il doit être 0 ou 1.")
        elif len(self.joueurs) == 0:
            raise IndexError("getJoueur : Aucun joueur n'a était créé.")
        return self.joueurs[indice]

    def creeJoueurs(self) -> None:
        """Crée les joueurs pour la partie.
        """
        self.joueurs = []
        for i in range(2):
            j = Joueur(i+1)
            self.joueurs.append(j)

    def rejouer(self) -> None:
        """Réinitialise certains paramètres de la partie pour rejouer.
        """
        for i in range(len(self.joueurs)):
            self.joueurs[i].rejouer()
        self.editeur.setJoueur(self.joueurs[0])
        self.baston.rejouer()
        if self.timeline > 0:
            self.timeline = 1
        del self.ecranFin