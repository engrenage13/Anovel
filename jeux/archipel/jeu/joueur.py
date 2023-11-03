from jeux.archipel.jeu.bateau import Bateau

class Joueur:
    def __init__(self, nom: str, bateaux: list[Bateau]) -> None:
        self.nom = nom
        self.bateaux = bateaux
        self.a_perdu = False

    def copie_joueur(self, bateaux: list[Bateau] = None) -> object:
        if bateaux == None or len(bateaux) == 0:
            bats = self.bateaux
        else:
            bats = bateaux
        return Joueur(self.nom, bats)
    
    def check_fin_mise_en_place(self) -> bool:
        rep = True
        i = 0
        while rep and i < len(self.bateaux):
            rep = self.bateaux[i].est_en_jeu
            i += 1
        return rep
    
    def check_defaite(self) -> bool:
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
        if key < len(self.bateaux):
            return self.bateaux[key]
        else:
            return False
        
    def __add__(self, element: Bateau) -> None:
        self.bateaux.append(element)

    def __sub__(self, element: Bateau) -> None:
        if element in self.bateaux:
            position = self.bateaux.index(element)
            del self.bateaux[position]
            if len(self.bateaux) == 0:
                self.a_perdu = True

    def __len__(self) -> int:
        return len(self.bateaux)
