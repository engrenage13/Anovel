from jeux.archipel.jeu.bateau import Bateau

class Joueur:
    def __init__(self, nom: str, bateaux: list[Bateau]) -> None:
        """Crée un joueur.

        Args:
            nom (str): Le nom du joueur.
            bateaux (list[Bateau]): Les bateaux du joueur.
        """
        self.nom = nom
        self.bateaux = bateaux
        self.a_perdu = False
        self.nb_elimination = 0

    def copie_joueur(self, bateaux: list[Bateau] = None) -> object:
        """Crée un nouveau joueur à partir des informations du joueur actuel.

        Args:
            bateaux (list[Bateau], optional): Bateaux à attribués au nouveau joueur. Si None, copie les bateaux du joueur actuel. Defaults to None.

        Returns:
            object: Le nouveau joueur créé.
        """
        if bateaux == None or len(bateaux) == 0:
            bats = self.bateaux
        else:
            bats = bateaux
        return Joueur(self.nom, bats)
    
    def check_fin_mise_en_place(self) -> bool:
        """Vérifie si la mise en place du joueur est terminée.

        Returns:
            bool: True si le joueur est prêt à jouer, False dans le cas contraire.
        """
        rep = True
        i = 0
        while rep and i < len(self.bateaux):
            rep = self.bateaux[i].est_en_jeu
            i += 1
        return rep
    
    def check_defaite(self) -> bool:
        """Vérifie le joueur à perdu.

        Returns:
            bool: True s'il a perdu, False sinon.
        """
        defaite = True
        if not self.a_perdu:
            i = 0
            while defaite and i < len(self.bateaux):
                defaite = self.bateaux[i].coule
                i += 1
            if defaite:
                self.a_perdu = True
        return defaite
    
    def __getitem__(self, key: int) -> Bateau|bool:
        """Retourne le bateau avec l'indice key.

        Args:
            key (int): L'indice du bateau recherché.

        Returns:
            Bateau|bool: Le bateau assigné à l'indice si celui-ci existe, sinon False.
        """
        if key < len(self.bateaux):
            return self.bateaux[key]
        else:
            return False
        
    def __add__(self, element: Bateau) -> None:
        """Ajoute un bateau au joueur.

        Args:
            element (Bateau): Le bateau à ajouter.
        """
        self.bateaux.append(element)

    def __sub__(self, element: Bateau) -> None:
        """Retire un bateau au joueur.

        Args:
            element (Bateau): Le bateau à retirer au joueur.
        """
        if element in self.bateaux:
            position = self.bateaux.index(element)
            del self.bateaux[position]
            if len(self.bateaux) == 0:
                self.a_perdu = True

    def __len__(self) -> int:
        """Renvoie le nombre de bateaux que possède le joueur.

        Returns:
            int: Nombre de bateaux du joueur.
        """
        return len(self.bateaux)
