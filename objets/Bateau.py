from random import choice
from Image import Ima
from systeme.FondMarin import tailleCase

class Bateau:
    def __init__(self, nom: str, taille: int, id: int, image: Ima, proprietaire: object):
        """Crée un bateau.

        Args:
            nom (str): Le nom du bateau.
            taille (int): Le nombre de cases qu'occupe le bateau sur le plateau.
            id (int): Le numéro d'identification du bateau pour son propriétaire.
            image (Ima): Apparence du bateau.
            proprietaire (Joueur): Propriétaire du bateau.
        """
        self.taille = taille
        self.orient = 'h'
        self.nom = nom
        self.pos = None
        self.tag = 'bat' + str(id) + '.' + str(proprietaire.getId())
        self.tagPlus = 'tbat' + str(id) + '.' + str(proprietaire.getId())
        self.proprio = proprietaire
        self.etatSeg = ['o']*taille
        self.coule = False
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Images
        lideg = [90, -90]
        dimensions = image.getDimensions()
        horiz = image.reDim(prop=(tailleCase*0.88)*self.taille/dimensions[0])
        self.horiz = image.createPhotoImage(horiz)
        self.verti = image.tourne(choice(lideg), horiz)
        self.verti = image.createPhotoImage(self.verti)
        # /Images

    def estTouche(self, position: str) -> bool:
        """Dit si le bateau passé en paramètres est sur la case qui est regardée.

        Args:
            position (str): Case à vérifier.

        Returns:
            bool: True si le bateau est sur la case touché.
        """
        a = False
        i = 0
        while i < self.taille and not a:
            b = self.pos[i][0:len(self.pos[i])-2]
            if b == position:
                self.etatSeg[i] = 'x'
                a = True
            i = i + 1
        return a

    def estCoule(self) -> bool:
        """Dit si le bateau est coulé ou non.

        Returns:
            bool: True si le bateau est coulé.
        """
        a = False
        if self.coule:
            a = True
        else:
            if 'o' not in self.etatSeg:
                self.coule = True
                a = True
        return a