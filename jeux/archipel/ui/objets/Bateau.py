from systeme.FondMarin import *
from jeux.archipel.ui.objets.bases.pivote import Pivote
from jeux.archipel.ui.infoBulle import InfoBulle
from jeux.archipel.ui.icones import coeur, marin, degats as explosion
from jeux.archipel.jeu.bateau import Bateau as Bato

class Bateau(Bato, Pivote):
    def __init__(self, nom: str, vie: int, marins: int, pm: int, degats: int, portee: int, image: str, couleur: Color):
        """Crée un bateau.

        Args:
            nom (str): Nom du bateau.
            vie (int): Points de vie du bateau.
            marins (int): Nombre de marins présents sur le bateau.
            pm (int): Portée de déplacement du bateau.
            degats (int): Les dégâts que le bateau peut infliger.
            portee (int): Nombre de cases maximal que peuvent parcourir les tirs du bateau.
            image (str): Chemin d'accès à l'image du bateau.
            couleur (Color): Couleur du bateau.
        """
        Bato.__init__(self, nom, vie, marins, pm, degats, portee)
        Pivote.__init__(self, image)
        self.couleur = couleur
        self.rejouer()
        # InfoBulle
        self.infoBulle = InfoBulle([["coeur", self.get_vie(), coeur], ["marin", self.get_marins(), marin], ["flamme", self.get_degats(), explosion]])

    def dessine(self) -> None:
        """Dessine le bateau.
        """
        super().dessine()
        if self.getContact():
            if not self.bloqueInfoBulle:
                self.infoBulle.dessine(self.pos[0], int(self.pos[1]-self.dims[1]/2))

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du bateau pour rejouer une nouvelle partie.
        """
        self.reset()
        self.reinitialise()
        self.id = 0
        self.bloqueInfoBulle = False
    
    def aFini(self) -> bool: # A delete
        """Vérifie si le tour du bateau est terminé.

        Returns:
            bool: True si l'action est terminée.
        """
        return True
    
    def est_en_vie(self) -> bool:
        """Vérifie si le bateau nest pas coulé.

        Returns:
            bool: True si le bateau flotte.
        """
        if self.coule:
            return False
        else:
            return True
        
    def setNbPV(self, vie: int) -> None: # à delete
        """Modifie les PV actuel du bateau.

        Args:
            vie (int): Le nouveau nombre de PV du bateau.
        """
        pass

    def __pos__(self) -> None: # à supprimer
        """Rend le bateau actif.
        """
        super().__pos__()
    
    def __neg__(self) -> None: # à supprimer
        """Rend le bateau inactif.
        """
        super().__neg__()

    def __add__(self, valeur: int) -> None:
        """Ajoute des PV au bateau.

        Args:
            valeur (int): Nombre de PV à ajouter.
        """
        super().__add__(valeur)
        self.infoBulle.setValeurElement("coeur", self.get_vie())
    
    def __sub__(self, valeur: int) -> bool:
        """Retire des PV au bateau.

        Args:
            valeur (int): Nombre de PV à retirer.

        Returns:
            bool: True si le bateau a coulé, False dans le cas contraire.
        """
        mort = super().__sub__(valeur)
        self.infoBulle.setValeurElement("coeur", self.get_vie())
        return mort
    
    def __bool__(self) -> bool:
        """Booléen signifiant que le bateau a coulé ou non.

        Returns:
            bool: True si le bateau flotte.
        """
        return self.est_en_vie()