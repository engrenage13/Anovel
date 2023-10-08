from systeme.FondMarin import *
from jeux.archipel.objets.Bateau import Bateau
from jeux.archipel.config import bateaux as libat
from ui.blocTexte import BlocTexte

class Joueur:
    """L'entité joueur est ce qui symbolise tout ce qui est lié à ce qu'un joueur peut faire lors de la partie.
    """
    def __init__(self, nom: str, bateaux: list[Bateau], couleur: Color):
        """Crée un joueur.

        Args:
            nom (str): Le nom du joueur.
            bateaux (list[Bateau]): Ses bateaux.
            couleur (Color): Sa couleur.
        """
        self.nom = nom
        self.titre = BlocTexte(nom, police1, int(yf*0.04), [int(xf*0.1), int(yf*0.06)])
        self.couleur = couleur
        self.btx = bateaux
        self.rejouer()

    def dessine(self) -> None:
        """Dessine l'entité joueur à l'écran.
        """
        # ui
        draw_rectangle_rounded([int(yf*0.01), int(yf*0.01), int(xf*0.1), int(yf*0.06)], 0.15, 30, [255, 255, 255, 170])
        self.titre.dessine([[int(yf*0.01+xf*0.05), int(yf*0.01+yf*0.025)], 'c'], self.couleur)

    def rejouer(self) -> None:
        """Réinitialise certains paramètres du joueur pour une nouvelle partie.
        """
        self.actif = False
        self.bateaux = []
        self.nbelimination = 0
        # bateaux
        for i in range(len(self.btx)):
            bateau = libat[self.btx[i]]
            bat = Bateau(bateau["nom"], bateau["image"], bateau["vie"], bateau["marins"], bateau["pm"], bateau["degats"], self.couleur)
            self.bateaux.append(bat)
        # Phase
        self.setPhase("placement")
        self.setIds()

    def bateauSuivant(self) -> None:
        """Passe au bateau suivant s'il y en a qui n'ont pas étaient joués, sinon elle met fin au tour du joueur.
        """
        if self.actuel < len(self.bateaux):
            -self.bateaux[self.actuel]
        if not self.tourFini():
            self.prochainBateau()
            +self.bateaux[self.actuel]
        else:
            self.actuel = 0
            -self

    def estEnPlace(self) -> bool:
        """Vérifie si tous les bateaux du joueur sont en place.

        Returns:
            bool: True si tous les bateaux sont placés.
        """
        place = True
        i = 0
        while i < len(self.bateaux) and place:
            if not self.bateaux[i].estEnPlace():
                place = False
            else:
                i += 1
        return place
    
    def prochainBateau(self) -> None:
        """Définit l'indice du prochain bateau.
        """
        i = self.actuel+1
        if i < len(self.bateaux):
            self.actuel = i
        else:
            self.actuel = 0

    def tourFini(self) -> bool:
        """Vérifie si le tour du joueur est terminé.

        Returns:
            bool: True si le joueur a terminé son tour.
        """
        i = 0
        fin = True
        while i < len(self.bateaux) and fin:
            if not self.bateaux[i].aFini():
                fin = False
            else:
                i += 1
        return fin
    
    def compteBateau(self) -> int:
        """Compte le nombre de bateau que possède le joueur.

        Returns:
            int: Total des bateaux du joueur.
        """
        compteur = 0
        for i in range(len(self.bateaux)):
            bat = self.bateaux[i]
            if bat.estEnVie():
                compteur += 1
        return compteur
    
    def setIds(self) -> None:
        """Modifie les identifiants des bateaux du joueur.
        """
        if self.phase == 'placement':
            places = []
            autres = []
            for i in range(len(self.bateaux)):
                if self.bateaux[i].place:
                    places.append(self.bateaux[i])
                else:
                    autres.append(self.bateaux[i])
            self.bateaux = places+autres
        for i in range(len(self.bateaux)):
            self.bateaux[i].id = i+1

    def setPhase(self, phase: str) -> None:
        """Modifie la phase du jeu pour le joueur (compliqué, voir config.json).

        Args:
            phase (str): La nouvelle phase.
        """
        self.phase = phase
        if self.phase == "placement":
            for i in range(len(self.bateaux)):
                self.bateaux[i].bloqueInfoBulle = True
        else:
            for i in range(len(self.bateaux)):
                self.bateaux[i].bloqueInfoBulle = False

    def __pos__(self) -> None:
        """Ce joueur devient actif.
        """
        self.actif = True
        if self.phase != "placement":
            i = 0
            while i < len(self.bateaux):
                if self.bateaux[i].coule:
                    del self.bateaux[i]
                else:
                    self.bateaux[i].finiTour = False
                    i += 1
            if len(self.bateaux) > 0:
                +self.bateaux[self.actuel]

    def __neg__(self) -> None:
        """Le tour de ce joueur est terminé ou suspendu.
        """
        self.actif = False
        for i in range(len(self.bateaux)):
            -self.bateaux[i]

    def __getitem__(self, key: int) -> Bateau|bool:
        """Renvoie l'un des bateaux du joueur.

        Args:
            key (int): L'indice du bateau recherché.

        Returns:
            Bateau|bool: Renvoie le bateau s'il a été trouvé ou False dans le cas contraire.
        """
        if key < len(self.bateaux):
            return self.bateaux[key]
        else:
            return False
    
    def __len__(self) -> int:
        """Retourne le nombre de bateau du joueur.

        Returns:
            int: Total des bateaux.
        """
        return len(self.bateaux)
    
    def __add__(self, bateau: Bateau) -> int:
        """Ajoute un bateau à la la flotte du joueur.

        Args:
            bateau (Bateau): Le bateau à ajouter.

        Returns:
            int: Le nouveau total de bateaux dans la flotte.
        """
        self.bateaux.append(bateau)
        bateau.finiTour = False
        bateau.couleur = self.couleur
        self.setIds()
        return len(self.bateaux)
    
    def __sub__(self, bateau: Bateau) -> int:
        """Supprime l'un des bateaux de la flotte du joueur.

        Args:
            bateau (Bateau): Le bateau qui s'en va.

        Returns:
            int: Le nouveau total de bateaux dans la flotte.
        """
        if bateau in self.bateaux:
            del self.bateaux[self.bateaux.index(bateau)]
        self.setIds()
        return len(self.bateaux)