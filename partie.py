from systeme.FondMarin import *
from systeme.fenetre import Fenetre
from Installateur.Installateur import Installateur
from objets.Joueur import Joueur
from ui.clickIma import ClickIma
from museeNoyee import croixLumineuse, croixSombre
#from attaque import Attaque

class Partie:
    def __init__(self, fenetre: Fenetre) -> None:
        self.fenetre = fenetre
        self.croix = ClickIma([fenetre.switchEtat], [croixSombre, croixLumineuse])
        self.joueurs = []
        self.timeline = 0

    def nouvelleEtape(self) -> None:
        self.timeline = self.timeline + 1
        if self.timeline == 1:
            self.creeJoueurs()
            self.installateur = Installateur(self.joueurs[0], self)
        elif self.timeline == 2:
            self.installateur.setJoueur(self.joueurs[1])

    def dessine(self) -> None:
        if self.timeline == 1 or self.timeline == 2:
            self.installateur.dessine()

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

    def jeu(self) -> None:
        """Lance la partie.
        """
        j = self.getJoueurs()
        self.inst.sup()
        del(self.inst)
        #fond.itemconfigure('titre', text=(self.getJoueur(0).nom))
        #fond.move('titre', -xf*0.055, 0)
        for i in range(len(j)):
            j[i].cTire.dessine((tlatba, yf*0.105+yf*i))
        #Attaque(j[0], j[1])

    def checkEtat(self) -> None:
        """Vérifie si les 2 joueurs ont correctements positionnés tout leurs bateaux.
        """
        b = 0
        i = 0
        j = self.getJoueurs()
        while i < len(j) and b < 2:
            if not j[i].pret:
                b = b + 1
                if b == 1:
                    j[i].pret = True
            i = i + 1
        if b < 2:
            self.jeu()
        else:
            self.suite()