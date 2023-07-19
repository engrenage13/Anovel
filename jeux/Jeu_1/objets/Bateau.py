from systeme.FondMarin import *
from jeux.Jeu_1.objets.bases.pivote import Pivote
from jeux.Jeu_1.ui.infoBulle import InfoBulle
from museeNoyee import coeur, marin, degats as explosion

class Bateau(Pivote):
    def __init__(self, nom: str, image: str, pv: int, marins: int, pm: int, degats: int, couleur: Color, ide: int):
        """Crée un bateau.

        Args:
            nom (str): Nom du bateau.
            image (str): Chemin d'accès à l'image du bateau.
            pv (int): Points de vie du bateau.
            marins (int): Nombre de marins présents sur le bateau.
            pm (int): Portée de déplacement du bateau.
            couleur (Color): Couleur du bateau.
        """
        super().__init__(image)
        self.nom = nom
        self.couleur = couleur
        self.id = ide
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
            self.infoBulle.dessine(self.pos[0], int(self.pos[1]-self.dims[1]/2))

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du bateau pour rejouer une nouvelle partie.
        """
        self.reset()
        self.place = False
        self.coule = False
        self.actif = False
        self.finiTour = False
        self.vie = int(str(self.pvi))
        self.marins = int(str(self.marinsi))
        self.pm = int(str(self.pmi))
        self.degats = int(str(self.degi))

    def estEnPlace(self) -> bool:
        return self.place
    
    def aFini(self) -> bool:
        rep = self.coule
        if not rep:
            rep = self.finiTour
        return rep
    
    def estEnVie(self) -> bool:
        if self.coule:
            return False
        else:
            return True
        
    def setNbPV(self, vie: int) -> None:
        self.vie = vie
        self.infoBulle.setValeurElement("coeur", self.vie)
        if self.vie <= 0:
            self.coule = True

    def __pos__(self) -> None:
        super().__pos__()
    
    def __neg__(self) -> None:
        super().__neg__()
        self.finiTour = True

    def __add__(self, valeur: int) -> int:
        self.marins += valeur
        self.infoBulle.setValeurElement("marin", self.marins)
        return self.marins
    
    def __sub__(self, valeur: int) -> int:
        self.marins -= valeur
        self.infoBulle.setValeurElement("marin", self.marins)
        return self.marins
    
    def __bool__(self) -> bool:
        return self.estEnVie()