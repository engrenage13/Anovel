from random import choice, randint
from systeme.FondMarin import *
from jeux.archipel.ui.objets.plateau.case import Case, TypeCase
from jeux.archipel.fonctions.bases import TAILLECASE, EAUX, marqueCases
from jeux.archipel.fonctions.deplacement import glisse
from jeux.archipel.jeu.plateau.plateau import Plateau as P

class Plateau(P):
    """Le plateau de jeu.
    """
    def __init__(self, taille: int, nb_iles: int, taille_cases: int = TAILLECASE, envirronement: bool = True, plan: bool = False, accroche: tuple[int] = (0, 0)) -> None:
        """Crée le plateau.

        Args:
            taille (int): Nombre de cases dans une ligne (plateau carré).
            nb_iles (int): Nombre maximal de cases pouvant être des îles.
            taille_cases (int, optional): La taille des cases du plateau. Defaults to TAILLECASE.
            envirronement (bool, optional): Est-ce qu'il faut afficher l'envirronement ou non ? Defaults to True.
            plan (bool, optional): Le plateau est-il utilisé comme un plan ? Defaults to False.
            accroche (tuple[int], optional): L'origine du plateau pour la caméra (c'est technique). Defaults to (0, 0).
        """
        super().__init__(taille, nb_iles)
        if envirronement:
            self.largeur_envirronement = TAILLECASE
        else:
            self.largeur_envirronement = 0
        self.taille_case = taille_cases
        self.is_plan = plan
        self.env = envirronement
        # Position
        self.accroche = accroche
        # Défilement du plateau
        if self.is_plan:
            self.bloque = True
        else:
            self.bloque = False
        self.glisse = False
        # /
        # Dessin
        self.elements_prioritaires = []
        self.grise = False
        # Décors
        carreau = load_image("jeux/archipel/images/carrelage.png")
        image_resize(carreau, self.tailleCase, self.tailleCase)
        self.carrelage = load_texture_from_image(carreau)
        unload_image(carreau)

    def dessine(self) -> None:
        """Dessine le plateau.
        """
        self.dessineEnvirronement()
        if len(self.elements_prioritaires) > 0:
            for i in range(self.taille):
                for j in range(self.taille):
                    self.cases[i][j].dessine(self.grise)
            for i in range(len(self.elements_prioritaires)):
                self.elements_prioritaires[i].dessine()
            for i in range(self.taille):
                for j in range(self.taille):
                    self.cases[i][j].dessineContenu()
        else:
            for i in range(self.taille):
                for j in range(self.taille):
                    self.cases[i][j].dessine(self.grise)
                    self.cases[i][j].dessineContenu()
        if self.glisse and self.cases[0][0].pos != self.position_cible:
            self.rePlace()

    def mise_en_place(self) -> None:
        """Met le plateau en place.
        """
        typIles = [type.value for type in TypeCase]
        countIle = 0
        x = self.accroche[0]+self.largeur_envirronement
        y = self.accroche[1]+self.largeur_envirronement
        for i in range(self.taille):
            ligne = []
            for j in range(self.taille):
                if countIle < self.nb_iles:
                    typIle = choice(typIles)
                    countIle += 1
                else:
                    typIle = TypeCase.MER
                ligne.append(Case(x, y, self.taille_case, [0, 0, 0, 150], typIle))
                x += self.taille_case
            self.cases.append(ligne)
            x = self.accroche[0]+self.largeur_envirronement
            y += self.taille_case
        self.position_cible = (x, y)

    def dessineEnvirronement(self) -> None:
        """Dessine l'envirronement.
        """
        p = self.cases[0][0].pos
        l = self.largeur_envirronement
        if self.env:
            x = p[0]-l
            y = p[1]-l
            for i in range(self.taille+2):
                for j in range(self.taille+2):
                    draw_texture(self.carrelage, x, y, WHITE)
                    x += self.carrelage.width
                y += self.carrelage.height
                x = p[0]-l
            draw_rectangle(p[0]-l, p[1]-l, int(self.carrelage.width*(self.taille+2)), int(self.carrelage.height*(self.taille+2)), [11, 23, 62, 150])

    def deplace(self, x: int, y: int) -> None:
        """Permet de déplacer le plateau à l'écran (scroll).

        Args:
            x (int): Valeur à ajouter aux abscisses du plateau et de toutes ses cases.
            y (int): Valeur à ajouter aux ordonnées du plateau et de toutes ses cases.
        """
        if not self.passeFrontiereHorizontale(x) and self.passeFrontiereVerticale(y):
            y = 0
        elif self.passeFrontiereHorizontale(x) and not self.passeFrontiereVerticale(y):
            x = 0
        elif self.passeFrontiereHorizontale(x) and self.passeFrontiereVerticale(y):
            x = y = 0
        for i in range(self.taille):
            for j in range(self.taille):
                self.cases[i][j].deplace(x, y)

    def place(self, x: int, y: int, glisse: bool = False) -> None:
        """Permet de démarrer une glissade du plateau.

        Args:
            x (int): L'abscisse cible.
            y (int): L'ordonnée cible.
            glisse (bool, optional): Est-ce que le plateau doit s'arrêter pile sur ces coordonnées ou peut-il glisser un peu plus loin ? Defaults to False.
        """
        self.position_cible = (x, y)
        self.glisse = glisse
        if not glisse:
            px = x
            py = y
            tCase = TAILLECASE
            for i in range(self.taille):
                for j in range(self.taille):
                    self.cases[i][j].setPos(px, py)
                    px += tCase
                py += tCase
                px = x

    def rePlace(self) -> None:
        """Execute le déplacement par glissade du plateau.
        """
        px = self.cases[0][0].pos[0]
        py = self.cases[0][0].pos[1]
        dep = glisse((px, py), self.position_cible, int(xf*0.01))
        tCase = TAILLECASE
        x = dep[0]
        y = dep[1]
        for i in range(self.taille):
            for j in range(self.taille):
                self.cases[i][j].setPos(x, y)
                x += tCase
            y += tCase
            x = dep[0]
        if self.cases[0][0].pos == self.position_cible:
            self.glisse = False

    def passeFrontiereHorizontale(self, x: int, absolue: bool = False) -> bool:
        """Vérifie si les frontières horizontales du plateau ne se décrochent pas du bord de l'écran.

        Args:
            x (int): Le point à vérifier.
            absolue (bool, optional): Est-ce une position absolue ? Defaults to False.

        Returns:
            bool: True si aucune des frontières ne dépassent leurs limites.
        """
        rep = False
        tCase = self.taille_case
        if absolue:
            xcomp1 = x
            xcomp2 = int(x+len(self.cases)*tCase)
        else:
            xcomp1 = self.cases[0][0].pos[0]+x
            xcomp2 = self.cases[0][self.taille-1].pos[0]+tCase+x
        if xcomp1 > self.largeur_envirronement:
            rep = True
        elif xcomp2 < xf-self.largeur_envirronement:
            rep = True
        return rep
    
    def passeFrontiereVerticale(self, y: int, absolue: bool = False) -> bool:
        """Vérifie si les frontières verticales du plateau ne se décrochent pas du bord de l'écran.

        Args:
            y (int): Le point à vérifier.
            absolue (bool, optional): Est-ce une position absolue ? Defaults to False.

        Returns:
            bool: True si aucune des frontières ne dépassent leurs limites.
        """
        rep = False
        tCase = self.taille_case
        if absolue:
            xcomp1 = y
            xcomp2 = int(y+len(self.cases)*tCase)
        else:
            xcomp1 = self.cases[0][0].pos[1]+y
            xcomp2 = self.cases[self.taille-1][0].pos[1]+tCase+y
        if xcomp1 > self.largeur_envirronement:
            rep = True
        elif xcomp2 < yf-self.largeur_envirronement:
            rep = True
        return rep
    
    def getVoisines(self, case: Case) -> dict[tuple|bool]:
        """Retourne les coordonnées des cases voisines de la cible.

        Args:
            case (Case): La case dont on cherhche les voisines.

        Returns:
            dict[tuple|bool]: Renvoie les voisines nord, sud, est et ouest de la case si elle en a, sinon, renvoie False.
        """
        voisines = {'n': False, 's': False, 'o': False, 'e': False}
        pos = self.trouveCoordsCase(case)
        if pos:
            if pos[0] > 0:
                voisines['o'] = (pos[1], pos[0]-1)
            if pos[1] > 0:
                voisines['n'] = (pos[1]-1, pos[0])
            if pos[0] < self.nbCases-1:
                voisines['e'] = (pos[1], pos[0]+1)
            if pos[1] < self.nbCases-1:
                voisines['s'] = (pos[1]+1, pos[0])
        return voisines
    
    def focusCase(self, case: tuple) -> None:
        """Permet à la caméra de positionner une case précise du plateau au centre de l'écran.

        Args:
            case (tuple): La case qui doit être sous les feux de la rampe.
        """
        if type(case) != bool:
            x = self.cases[0][0].pos[0]
            y = self.cases[0][0].pos[1]
            cx = int(self.cases[case[0]][case[1]].pos[0]+self.tailleCase/2)
            cy = int(self.cases[case[0]][case[1]].pos[1]+self.tailleCase/2)
            if cx <= int(xf/2):
                dx = int(xf/2-cx)
                mulx = 1
            else:
                dx = int(cx-xf/2)
                mulx = -1
            if cy <= int(yf/2):
                dy = int(yf/2-cy)
                muly = 1
            else:
                dy = int(cy-yf/2)
                muly = -1
            nx = x+(dx*mulx)
            ny = y+(dy*muly)
            if self.passeFrontiereHorizontale(nx, True):
                if mulx > 0:
                    nx = self.largeurEnvirronement
                else:
                    nx = xf-(len(self.cases)*self.tailleCase)-self.largeurEnvirronement
            if self.passeFrontiereVerticale(ny, True):
                if muly > 0:
                    ny = self.largeurEnvirronement
                else:
                    ny = yf-(len(self.cases)*self.tailleCase)-self.largeurEnvirronement
            self.place(nx, ny, True)
    
    def vide(self) -> None:
        """Permet de vider le plateau.
        """
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].vide()
        self.elementsPrioritaires = []

    def setIles(self) -> None:
        """Modifie la présence et la structure des îles sur le plateau.
        """
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                case = self.cases[i][j]
                if case.marqueur:
                    dossierSpecifique = self.definiOriNomb(self.getIlesVoisines(case), case)
                    case.setIle(dossierSpecifique)

    def getIlesVoisines(self, centre: Case) -> dict[bool]:
        """Permet de vérifier si les cases alentours ont également un marqueur d'île.

        Args:
            centre (Case): La case d'où on commence les recherches.

        Returns:
            dict[bool]: Vérifie pour les cases nord, sud, est et ouest (si elles existent) si elles possèdent un marqueur d'île.
        """
        ilesVoisines = {'n': False, 'e': False, 's': False, 'o': False}
        voisines = self.getVoisines(centre)
        if voisines['n']:
            if self.cases[voisines['n'][0]][voisines['n'][1]].marqueur:
                ilesVoisines['n'] = True
        if voisines['e']:
            if self.cases[voisines['e'][0]][voisines['e'][1]].marqueur:
                ilesVoisines['e'] = True
        if voisines['s']:
            if self.cases[voisines['s'][0]][voisines['s'][1]].marqueur:
                ilesVoisines['s'] = True
        if voisines['o']:
            if self.cases[voisines['o'][0]][voisines['o'][1]].marqueur:
                ilesVoisines['o'] = True
        return ilesVoisines
    
    def definiOriNomb(self, ilesVoisines: dict[bool], case: Case) -> str:
        """Définit de quel type de segment d'île puis duquel précisément la case doit se munir.

        Args:
            ilesVoisines (dict[bool]): dictionnaire précisant pour chaque case voisines si elles ont ou non un marqueur d'île.
            case (Case): La case sur laquelle la méthode travaille.

        Returns:
            str: précision sur le dossier du segment choisi.
        """
        dossier = 'a'
        compte = 0
        orientations = ['n', 'e', 's', 'o']
        for i in range(len(orientations)):
            if ilesVoisines[orientations[i]]:
                compte += 1
        j = 0
        stop = False
        while j < len(orientations) and not stop:
            if ilesVoisines[orientations[j]]:
                stop = True
            else:
                j += 1
        case.typeIle = compte
        if compte == 0 or compte == 4:
            case.orienteIle = randint(0, 3)
        elif compte == 1:
            case.orienteIle = j
        elif compte == 3:
            if not ilesVoisines['n']:
                case.orienteIle = 0
            elif not ilesVoisines['e']:
                case.orienteIle = 1
            elif not ilesVoisines['s']:
                case.orienteIle = 2
            elif not ilesVoisines['o']:
                case.orienteIle = 3
        elif compte == 2:
            if (ilesVoisines['n'] and ilesVoisines['s']) or (ilesVoisines['e'] and ilesVoisines['o']):
                dossier = 'b'
                if ilesVoisines['n']:
                    possibilites = [0, 2]
                else:
                    possibilites = [1, 3]
                case.orienteIle = choice(possibilites)
            else:
                if ilesVoisines['n'] and ilesVoisines['e']:
                    case.orienteIle = 0
                elif ilesVoisines['e'] and ilesVoisines['s']:
                    case.orienteIle = 1
                elif ilesVoisines['s'] and ilesVoisines['o']:
                    case.orienteIle = 2
                elif ilesVoisines['o'] and ilesVoisines['n']:
                    case.orienteIle = 3
        return dossier

    def rejouer(self) -> None:
        """Modifie certaines informations pour rejouer une nouvelle partie.
        """
        for i in range(self.nbCases):
            for j in range(self.nbCases):
                self.cases[i][j].rejouer()
        self.elementsPrioritaires = []
        marqueCases(self, 20, 40)
        self.setIles()

    def copieContenu(self, plateau) -> None:
        """Permet de copier la répartition des îles sur les cases d'un plateau sur celles du plateau actuel.

        Args:
            plateau (Plateau): Le plateau d'où la méthode doit tirer les informations.
        """
        for i in range(len(self.cases)):
            for j in range(len(self.cases[i])):
                if i < plateau.nbCases and j < plateau.nbCases:
                    self.cases[i][j].marqueur = plateau[i][j].marqueur
    
    def __getitem__(self, key: int) -> list[Case]:
        """Retourne l'une des lignes de case du plateau.

        Args:
            key (int): L'indice de la ligne recherchée.

        Returns:
            list[Case]: La ligne retournée.
        """
        return self.cases[key]
    
    def __len__(self) -> int:
        """Retourne le nombre de cases sur un côté du plateau.

        Returns:
            int: Nombre de cases sur le côté du plateau.
        """
        return self.nbCases
    
    def __add__(self, element) -> None:
        """Ajoute un élément dans la liste des éléments prioritaires.

        Args:
            element (_type_): L'élément à ajouter à la liste des éléments prioritaires.
        """
        if element not in self.elementsPrioritaires:
            self.elementsPrioritaires.append(element)

    def __sub__(self, element) -> None:
        """Supprime un élément de la liste des éléments prioritaires.

        Args:
            element (_type_): L'élément à supprimer de la liste des éléments prioritaires.
        """
        if element in self.elementsPrioritaires:
            pos = self.elementsPrioritaires.index(element)
            del self.elementsPrioritaires[pos]