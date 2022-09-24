from objets.Bateau import Bateau
from objets.plateau import Plateau
from systeme.FondMarin import *
from random import randint, choice

class Positionneur:
    def __init__(self, nbBateaux: int) -> None:
        self.reset(nbBateaux)

    def getCaseJumelles(self, position: list, indice: int, armada: list) -> list:
        """Vérifie si le bateau ne touche aucun autre bateau.

        Args:
            position (list): Les cases occupées par le bateau.
            indice (int): L'indice du bateau sélectionné.
            armada (list): Liste des bateaux traités par l'éditeur.

        Returns:
            list: 1. True si le bateau est sur une case déjà occupé par un autre. 2. Indice de la case concernée.
        """
        rep = False
        i = 0
        while i < len(position) and not rep:
            j = 0
            while j < len(armada) and not rep:
                if j != indice and armada[j].pos:
                    if position[i] in armada[j].pos:
                        rep = True
                j = j + 1
            i = i + 1
        return [rep, i]

    def getContact(self, bateau: int) -> bool:
        """Vérifie si le curseur est sur le bateau.

        Args:
            bateau (int): L'indice du bateau à tester.

        Returns:
            bool: True si le curseur est sur le bateau, False dans le cas contraire.
        """
        bat = self.coords[bateau]
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= bat[0] and x <= bat[0]+bat[2]:
            if y >= bat[1] and y <= bat[1]+bat[3]:
                rep = True
        return rep

    def switchMode(self, indice: int, bateau: Bateau) -> bool:
        """Sélectionne et déselectionne le bateau.

        Args:
            indice (int): Indice du bateau sur lequel agir.
            bateau (Bateau): Bateau sur lequel agir.

        Returns:
            bool: True si le bateau entre en phase de placement, False s'il est relâché.
        """
        if self.verifType(bateau):
            if self.defil[indice]:
                self.immobile(indice, bateau)
                rep = False
            else:
                self.declenMouv(indice)
                rep = True
        else:
            rep = None
        return rep

    def immobile(self, indice: int, bateau: Bateau):
        """Désélectionne le bateau.

        Args:
            indice (int): L'indice du bateau sur lequel agir.
            bateau (Bateau): Le bateau sur lequel agir.
        """
        if self.verifType(bateau):
            self.defil[indice] = False
            if not bateau.pos or False in bateau.pos:
                bateau.pos = False
                if bateau.direction != 0:
                    bateau.direction = 0

    def declenMouv(self, indice: int):
        """Sélectionne le bateau.

        Args:
            indice (int): L'indice du bateau sur lequel agir.
        """
        self.defil[indice] = True

    def setPosition(self, coord: list, zone: int, bateau: Bateau) -> None:
        """Modifie la position du bateau sur le plateau.

        Args:
            coord (list): Liste des cases ciblé.
            zone (int): Zone de l'écran où se trouve le bateau.
            bateau (Bateau): Bateau dont la position doit être modifiée.
        """
        if self.verifType(bateau):
            pos = []
            if zone == 1:
                for i in range(bateau.taille-len(coord)):
                    pos.append(False)
                for i in range(len(coord)):
                    pos.append(coord[len(coord)-1-i])
            elif zone == 2:
                pos = coord
            else:
                pos = coord
                for i in range(bateau.taille-len(coord)):
                    pos.append(False)
            bateau.pos = pos

    def tourne(self, indice: int, bateau: Bateau):
        """Fait tourner le bateau.

        Args:
            indice (int): L'indice du bateau qui doit pivoter.
            bateau (Bateau): Le bateau qui doit pivoter.
        """
        if self.verifType(bateau):
            if self.defil[indice]:
                if bateau.direction < 3:
                    bateau.direction += 1
                else:
                    bateau.direction = 0

    def verifType(self, bateau: Bateau) -> bool:
        """Verifie si l'objet passé en paramètre est bien un Bateau.

        Args:
            bateau (Bateau): L'objet à vérifier.

        Returns:
            bool: True si c'est un Bateau.
        """
        if type(bateau) == Bateau:
            rep = True
        else:
            rep = False
        return rep

    def reset(self, nbBateaux: int) -> None:
        """Réinitialise les valeurs par défaut du positionneur avec le nombre de bateaux souhaité.

        Args:
            nbBateaux (int): Nombre de bateaux à positionner.
        """
        self.coords = [[0, 0, 1, 1]]*nbBateaux
        self.defil = [False]*nbBateaux

    def checkClone(self, valeur: object, liste: list) -> bool:
        """Vérifie si la valeur est déjà dans la liste.

        Args:
            valeur (object): Valeur à vérifier.
            liste (list): Liste où il faut vérifier.

        Returns:
            bool: True si la valeur n'est pas dans une liste, False sinon.
        """
        rep = True
        if valeur in liste:
            rep = False
        return rep

    def setCoord(self, bateau: int, coord: list) -> None:
        """Permet de modifier les coordonnées du bateau à l'écran.

        Args:
            bateau (int): L'indice du bateau concerné.
            coord (list): Les nouvelles coordonnées du bateau.
        """
        if bateau >= 0 and bateau < len(self.coords):
            self.coords[bateau] = coord

    def placementAleatoire(self, bateaux: list, plateau: Plateau) -> None:
        """Permet de placer tous les bateaux de manière aléatoire sur le plateau.

        Args:
            bateaux (list): Liste des bateaux à placer.
            plateau (Plateau): Le plateau sur lequel placer les bateaux.
        """
        dims = plateau.getDimensions()
        verif = self.verifPlacement(bateaux)
        blacklist = verif[0]
        liBat = verif[1]
        for i in range(len(liBat)):
            bateau = liBat[i]
            valid = False
            while not valid:
                pos = []
                dir = randint(0, 3)
                if dir == 0 or dir == 2:
                    sens = 'h'
                else:
                    sens = 'v'
                if sens == 'h':
                    x = randint(1, dims[0]-bateau.taille)
                    y = choice(plateau.alphabet[0:dims[1]-1])
                    for j in range(bateau.taille):
                        case = y+str(x)
                        pos.append(case)
                        x = x + 1
                else:
                    x = randint(1, dims[0])
                    y = choice(plateau.alphabet[0:dims[1]-bateau.taille])
                    for j in range(bateau.taille):
                        case = y+str(x)
                        pos.append(case)
                        y = plateau.alphabet[plateau.alphabet.index(y)+1]
                k = 0
                erreur = False
                while k < len(pos) and not erreur:
                    if pos[k] in blacklist:
                        erreur = True
                    else:
                        k = k + 1
                if not erreur:
                    valid = True
                    blacklist += pos
            self.setPosition(pos, 2, bateau)
            bateau.direction = dir

    def verifPlacement(self, bateaux: list) -> list:
        """Vérifie si les bateaux passés en paramètres sont placés ou non.

        Args:
            bateaux (list): Les bateaux à vérifier.

        Returns:
            list: 1. Listes des cases occupées. 2. Les bateaux qu'il reste à placer.
        """
        blacklist = []
        liBat = []
        nbVerif = 0
        troupeau = 0
        for i in range(len(bateaux)):
            bateau = bateaux[i]
            if self.verifType(bateau):
                troupeau = troupeau + 1
                if bateau.pos or (type(bateau.pos) == list and not (False in bateau.pos)):
                    nbVerif += 1
                    blacklist = blacklist + bateau.pos
                else:
                    liBat.append(bateau)
        if nbVerif == troupeau:
            blacklist = []
            liBat = bateaux
        return [blacklist, liBat]