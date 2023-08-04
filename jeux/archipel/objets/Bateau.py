from systeme.FondMarin import *
from jeux.archipel.objets.bases.pivote import Pivote
from jeux.archipel.ui.infoBulle import InfoBulle
from jeux.archipel.icones import coeur, marin, degats as explosion

class Bateau(Pivote):
    """Un bateau est l'un des éléments du jeu.

    Args:
        Pivote (Pivote): Le bateau est un élément pivotable.
    """
    def __init__(self, nom: str, image: str, pv: int, marins: int, pm: int, degats: int, couleur: Color):
        """Crée un bateau.

        Args:
            nom (str): Nom du bateau.
            image (str): Chemin d'accès à l'image du bateau.
            pv (int): Points de vie du bateau.
            marins (int): Nombre de marins présents sur le bateau.
            pm (int): Portée de déplacement du bateau.
            degats (int): Les dégâts que le bateau peut infliger.
            couleur (Color): Couleur du bateau.
        """
        super().__init__(image)
        self.nom = nom
        self.couleur = couleur
        # Valeurs initiales
        self.pvi = pv
        self.marinsi = marins
        self.pmi = pm
        self.degi = degats
        self.rejouer()
        # InfoBulle
        self.infoBulle = InfoBulle([["coeur", self.vie, coeur], ["marin", self.marins, marin], ["flamme", self.degats, explosion]])

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
        self.id = 0
        self.place = False
        self.coule = False
        self.actif = False
        self.finiTour = False
        self.bloqueInfoBulle = False
        self.vie = int(str(self.pvi))
        self.marins = int(str(self.marinsi))
        self.pm = int(str(self.pmi))
        self.degats = int(str(self.degi))

    def estEnPlace(self) -> bool:
        """Vérifie si le bateau est en place.

        Returns:
            bool: True s'il est placé.
        """
        return self.place
    
    def aFini(self) -> bool:
        """Vérifie si le tour du bateau est terminé.

        Returns:
            bool: True si l'action est terminée.
        """
        rep = self.coule
        if not rep:
            rep = self.finiTour
        return rep
    
    def estEnVie(self) -> bool:
        """Vérifie si le bateau nest pas coulé.

        Returns:
            bool: True si le bateau flotte.
        """
        if self.coule:
            return False
        else:
            return True
        
    def setNbPV(self, vie: int) -> None:
        """Modifie les PV actuel du bateau.

        Args:
            vie (int): Le nouveau nombre de PV du bateau.
        """
        self.vie = vie
        self.infoBulle.setValeurElement("coeur", self.vie)
        if self.vie <= 0:
            self.coule = True

    def __pos__(self) -> None:
        """Rend le bateau actif.
        """
        super().__pos__()
    
    def __neg__(self) -> None:
        """Rend le bateau inactif.
        """
        super().__neg__()
        self.finiTour = True

    def __add__(self, valeur: int) -> int:
        """Ajoute des marins sur le bateau.

        Args:
            valeur (int): Le nombre de marins à ajouter.

        Returns:
            int: Le nouveau total de marins présents sur le bateau.
        """
        self.marins += valeur
        self.infoBulle.setValeurElement("marin", self.marins)
        return self.marins
    
    def __sub__(self, valeur: int) -> int:
        """Retire des marins du bateau.

        Args:
            valeur (int): Nombre de marins à supprimer.

        Returns:
            int: Le nouveau total de marins présents sur le bateau.
        """
        self.marins -= valeur
        self.infoBulle.setValeurElement("marin", self.marins)
        return self.marins
    
    def __bool__(self) -> bool:
        """Retourne un booléen changeant de valeur en fonction du fait que le bateau soit coulé ou non.

        Returns:
            bool: True si le bateau flotte.
        """
        return self.estEnVie()