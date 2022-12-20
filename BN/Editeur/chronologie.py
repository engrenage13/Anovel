from BN.objets.Bateau import Bateau
from BN.Editeur.tiroir import Tiroir

class Chronologie:
    def __init__(self, tiroir: Tiroir, bateaux: list) -> None:
        """Crée le système de chronologie de l'éditeur.

        Args:
            tiroir (Tiroir): Le tiroir utilisé par l'éditeur actif.
            bateaux (list): La liste des bateaux du joueur.
        """
        self.setBateaux(bateaux)
        self.tiroir = tiroir
        self.reset()

    def nouvelleSauvegarde(self) -> None:
        """Permet de créer une nouvelle sauvegarde de la position des bateaux du joueur.
        """
        sauvegarde = []
        for i in range(len(self.bateaux)):
            bateau = self.bateaux[i]
            if bateau.pos and not False in bateau.pos:
                sauvegarde.append([bateau.pos, bateau.direction])
            else:
                sauvegarde.append('t')
        if self.position > 0:
            self.etapes = self.etapes[0:self.position+1] + [sauvegarde]
        else:
            self.etapes.append(sauvegarde)
        self.position += 1

    def retablirSauvegarde(self) -> list:
        """Permet de rétablir une ancienne sauvegarde.

        Returns:
            list: Les bateaux qui ne sont pas dans le tiroir.
        """
        pos = []
        sauvegarde = self.etapes[self.position]
        for i in range(len(sauvegarde)):
            bateau = sauvegarde[i]
            if bateau == 't':
                if self.bateaux[i] not in self.tiroir.liste:
                    self.bateaux[i].pos = False
                    if self.bateaux[i].direction != 0:
                        self.bateaux[i].direction = 0
                    self.tiroir.ajValListe(self.bateaux[i])
            else:
                self.bateaux[i].pos = bateau[0]
                self.bateaux[i].direction = bateau[1]
                pos.append(self.bateaux[i])
                if self.bateaux[i] in self.tiroir.liste:
                    self.tiroir.supValListe(self.tiroir.liste.index(self.bateaux[i]))
        return pos

    def annuler(self) -> None:
        """Permet de reculer de 1 pas dans la chronologie, pour "annuler" la dernière sauvegarde.
        """
        if self.position > 0:
            self.position -= 1
        
    def retablir(self) -> None:
        """Permet d'avancer de 1 pas dans la chronologie, pour "rétablir" la dernière sauvegarde.
        """
        if self.position < len(self.etapes)-1:
            self.position += 1

    def setBateaux(self, bateaux: list) -> None:
        """Permet de modifier la liste des bateaux dont la position est sauvegardée par la chronologie.

        Args:
            bateaux (list): Les bateaux qui doivent être utilisés.
        """
        self.bateaux = []
        for i in range(len(bateaux)):
            if type(bateaux[i]) == Bateau:
                self.bateaux.append(bateaux[i])

    def reset(self) -> None:
        """Permet de réinitialiser la chronologie (Ne change pas les bateaux dont elle sauvegarde les positions).
        """
        self.etapes = []
        self.position = -1
        self.nouvelleSauvegarde()