from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from Installateur.Installateur import Installateur
from objets.Joueur import Joueur
from ui.clickIma import ClickIma
from museeNoyee import croixLumineuse, croixSombre
from attaque import Attaque
from finPartie import FinPartie

class Partie:
    def __init__(self, fenetre: Fenetre) -> None:
        self.fenetre = fenetre
        self.croix = ClickIma([fenetre.switchEtat], [croixSombre, croixLumineuse])
        self.joueurs = []
        self.timeline = 0
        self.creeJoueurs()
        self.installateur = Installateur(self.joueurs[0], self)
        self.baston = Attaque(self.joueurs[0], self.joueurs[1], self)

    def nouvelleEtape(self) -> None:
        self.timeline = self.timeline + 1
        if self.timeline == 2:
            self.installateur.setJoueur(self.joueurs[1])
        elif self.timeline == 4:
            win = [False]*len(self.joueurs)
            for i in range(len(self.joueurs)):
                if self.joueurs[i] == self.baston.gagnant:
                    win[i] = True
            self.ecranFin = FinPartie(list(zip(self.joueurs, win)), self.baston.tour, self)

    def dessine(self) -> None:
        if self.timeline == 1 or self.timeline == 2:
            self.installateur.dessine()
        elif self.timeline == 3:
            self.baston.dessine()
        elif self.timeline == 4:
            self.baston.dessine()
            self.ecranFin.dessine()
            self.croix.dessine((xf-hbarre, int(hbarre*0.05)))
            if self.ecranFin.saturation == 255:
                self.nouvelleEtape()
        elif self.timeline == 5:
            self.ecranFin.dessine()
            self.croix.dessine((xf-hbarre, int(hbarre*0.05)))

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
        for i in range(len(self.joueurs)):
            self.joueurs[i].rejouer()
        self.installateur.setJoueur(self.joueurs[0])
        self.baston.rejouer()
        if self.timeline > 0:
            self.timeline = 1
        del self.ecranFin