from systeme.FondMarin import *
from jeux.archipel.ui.objets.plateau.plateau import Plateau

class Zone:
    """Une zone de positionnement ou de choix.
    """
    def __init__(self, debut: tuple, fin: tuple, plateau: Plateau) -> None:
        """Crée la zone.

        Args:
            debut (tuple): Coordonnées de la première case de la zone.
            fin (tuple): Coordonnées de la dernière case de la zone.
            plateau (Plateau): Le plateau sur le-quelle la zone sera placée.
        """
        self.cases = []
        self.plateau = plateau
        self.largeurBordure = int(xf*0.002)
        self.couleurs = ([255, 255, 255, 150], WHITE)
        self.couleurActives = ([255, 255, 255, 150], WHITE)
        self.mappage(debut, fin)

    def dessine(self) -> None:
        """Dessine la zone.
        """
        for i in range(len(self.cases)):
            Case = self.plateau[self.cases[i][0]][self.cases[i][1]]
            voisines = self.plateau.getVoisines(Case)
            x = Case.pos[0]
            y = Case.pos[1]
            cote = Case.taille
            if self.getContact():
                cf = self.couleurActives[0]
                cb = self.couleurActives[1]
            else:
                cf = self.couleurs[0]
                cb = self.couleurs[1]
            draw_rectangle(x, y, cote, cote, cf)
            if not voisines['n'] or voisines['n'] not in self.cases:
                draw_line_ex((x, y), (x+cote, y), self.largeurBordure, cb)
            if not voisines['e'] or voisines['e'] not in self.cases:
                draw_line_ex((x+cote, y), (x+cote, y+cote), self.largeurBordure, cb)
            if not voisines['s'] or voisines['s'] not in self.cases:
                draw_line_ex((x, y+cote), (x+cote, y+cote), self.largeurBordure, cb)
            if not voisines['o'] or voisines['o'] not in self.cases:
                draw_line_ex((x, y), (x, y+cote), self.largeurBordure, cb)

    def mappage(self, debut: tuple, fin: tuple) -> None:
        """Définit toutes les cases de la zone entre la première et la dernière.

        Args:
            debut (tuple): Les coordonnées de la première case.
            fin (tuple): Les coordonnées de la dernière case.
        """
        if debut == fin:
            self.cases.append((debut[1], debut[0]))
        else:
            if debut[0] <= fin[0]:
                startx = debut[0]
                finx = fin[0]
            else:
                startx = fin[0]
                finx = debut[0]
            if debut[1] <= fin[1]:
                starty = debut[1]
                finy = fin[1]
            else:
                starty = fin[1]
                finy = debut[1]
            for i in range(finy-starty+1):
                for j in range(finx-startx+1):
                    self.cases.append((starty+i, startx+j))

    def getContact(self) -> bool:
        """Vérifie si l'utilisateur survole la zone.

        Returns:
            bool: True si le curseur est sur la zone.
        """
        rep = False
        i = 0
        while i < len(self.cases) and not rep:
            Case = self.plateau[self.cases[i][0]][self.cases[i][1]]
            if Case.getContact():
                rep = True
            else:
                i += 1
        return rep
    
    def setCouleurs(self, fond: Color, bordure: Color, fondActif: Color, bordureActif: Color) -> None:
        """Modifie les couleurs de la zone.

        Args:
            fond (Color): Couleur du fond inactif.
            bordure (Color): Couleur de la bordure inactive.
            fondActif (Color): Couleur du fond actif.
            bordureActif (Color): Couleur de la bordure active.
        """
        self.couleurs = (fond, bordure)
        self.couleurActives = (fondActif, bordureActif)

    def __add__(self, zone) -> object:
        """Agrandit la zone en y ajoutant les cases d'une autre zone.

        Args:
            zone (Zone): La zone utilisée pour copier ses cases.

        Returns:
            Zone: La zone.
        """
        for i in range(len(zone.cases)):
            if zone.cases[i] not in self.cases:
                self.cases.append(zone.cases[i])
        return self
    
    def __getitem__(self, key: int) -> tuple[int]:
        """Renvoie l'une des cases de la zone.

        Args:
            key (int): L'indice de la case recherchée.

        Returns:
            tuple[int]: La position de la case recherché, sur le plateau.
        """
        return self.cases[key]
    
    def __len__(self) -> int:
        """Retourne le nombre de cases de la zone.

        Returns:
            int: Le nombre de cases sur lesquelles s'étirent la zone.
        """
        return len(self.cases)