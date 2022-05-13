from systeme.FondMarin import *
from ui.bouton import Bouton
from objets.Joueur import Joueur
from objets.plateau import Plateau
from museeNoyee import mer

class Installateur:
    def __init__(self, joueur: Joueur, creator: object) -> None:
        """Crée la fenêtre d'installation de bateaux pour un joueur.

        Args:
            joueur (Joueur): Joueur concerné par l'installation.
            creator (Partie): Objet "Partie" qui a lancé l'installateur.
        """
        self.proprio = creator
        self.joueur = joueur
        self.liBat = self.joueur.getBateaux()
        self.taillecase = int(yf*0.084)
        self.plateau = Plateau(10, 10)
        self.btValid = Bouton([self.proprio.nouvelleEtape, self.verif], "Valider", [BLUE, DARKBLUE, WHITE])
        self.btValid.setTexteNotif("Action Impossible", "Tous les bateaux doivent être placés")

    def dessine(self) -> None:
        ory = int((yf-hbarre)/2-self.taillecase*5)+hbarre
        draw_texture(mer, 0, 0, WHITE)
        self.barreTitre()
        self.plateau.dessine((tlatba, ory), self.taillecase)
        self.dessineBateaux()
        self.btValid.dessine((int(xf-tlatba*0.5), ory+int(self.taillecase*9.5)))

    def dessineBateaux(self) -> None:
        """Dessine tous les bateaux du joueur.
        """
        for i in range(len(self.liBat)):
            if not self.liBat[i].pos and not self.liBat[i].defil:
                x = int(xf*0.01)
                y = int((yf*0.15)*(i+1))
            draw_text_pro(police1, self.liBat[i].nom, (int(xf*0.01), int((yf*0.15)*(i+1)-yf*0.03)), (0, 0),
                          0, 20, 0, WHITE)
            self.liBat[i].dessine(x, y)

    def barreTitre(self) -> None:
        """Crée la barre de titre en haut de la fenêtre.
        """
        draw_rectangle_gradient_h(0, 0, xf, hbarre, [112, 31, 126, 120], [150, 51, 140, 100])
        draw_text_pro(police1, f"Installation : {self.joueur.getNom()}", (int(hbarre/4), int(hbarre/4)), 
                      (0, 0), 0, 25, 0, WHITE)
        self.proprio.croix.dessine((xf-hbarre, int(hbarre*0.05)))

    def verif(self) -> bool:
        """Vérifie si tous les bateaux du joueur ont étaient placés correctement.

        Returns:
            bool: True si tous les bateaux sont placés de manière acceptable.
        """
        rep = True
        i = 0
        while i < len(self.liBat) and rep:
            if not self.liBat[i].pos:
                rep = False
        return rep