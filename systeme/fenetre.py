from systeme.FondMarin import *

class Fenetre:
    def __init__(self) -> None:
        """Crée un objet capable de gérer certains paramètre essentiels à la fenêtre du jeu.
        """
        self.etat = True

    def switchEtat(self) -> None:
        """Permet de modifier l'etat de la fenêtre. 
           (True : la fenêtre fonctionne, False : elle s'apprête à se fermer).
        """
        if self.etat:
            self.etat = False
        else:
            self.etat = True

    def jeuDoitFermer(self) -> bool:
        """Vérifie si un bouton ou une commande demandant la fermeture du jeu a était passé...

        Returns:
            bool: True : si une telle commande a était passé. False dans le cas contraire.
        """
        if self.etat:
            rep = window_should_close()
        else:
            rep = True
        return rep

    def finDuJeu(self):
        """Gère les commandes nécessaire à une fermeture propre et en douceur di jeu.
        """
        unload_font(police1)
        unload_font(police2)
        close_window()