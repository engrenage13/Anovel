from systeme.FondMarin import *

class InfoBulle:
    """Les infobulles qui apparaissent au dessus des bateaux.
    """
    def __init__(self, contenu: list[list[str, int, Image]]) -> None:
        """Génère l'infobulle.

        Args:
            contenu (list[list[str, int, Image]]): Les attributs du bateau qu'il faut afficher.
        """
        self.contenu = {contenu[i][0]: [contenu[i][1], contenu[i][2]] for i in range(len(contenu))}
        self.cles = [contenu[i][0] for i in range(len(contenu))]
        # dims
        self.ecartx = int(xf*0.008)
        self.ecartx2 = int(xf*0.003)
        self.ecarty = int(yf*0.01)

    def dessine(self, x: int, y: int) -> None:
        """Dessine l'infobulle à l'écran.

        Args:
            x (int): Abscisse de l'origine de l'infobulle.
            y (int): Ordonnée de l'origine de l'infobulle.
        """
        decalx = int(xf*0.007)
        decaly = int(yf*0.02)
        dims = self.mesureTaille()
        draw_triangle((x-decalx, y-decaly), (x, y), (x+decalx, y-decaly), WHITE)
        draw_rectangle_rounded([int(x-dims[0]/2), int(y-decaly-dims[1]), dims[0], dims[1]], 0.2, 50, WHITE)
        px = int(x-dims[0]/2+self.ecartx*0.7)
        py = int(y-decaly-dims[1]+self.ecarty)
        for i in range(len(self.cles)):
            cle = self.cles[i]
            contenu = self.contenu[cle]
            h = contenu[1].height
            draw_texture(contenu[1], px, py, WHITE)
            px += int(contenu[1].width + self.ecartx2)
            tt = measure_text_ex(police1, str(contenu[0]), h, 0)
            draw_text_ex(police1, str(contenu[0]), (px, py), h, 0, BLACK)
            px += int(tt.x + self.ecartx)

    def mesureTaille(self) -> tuple:
        """Mesure la taille du contenu de l'infobulle.

        Returns:
            tuple: (largeur, hauteur).
        """
        l = self.ecartx*2
        h = 0
        for i in range(len(self.cles)):
            dims = self.mesureTailleElement(i)
            l += dims[0]
            if dims[1] > h:
                h = dims[1]
        h += self.ecarty*2
        l += self.ecartx*(len(self.contenu)-1)
        return (l, h)

    def mesureTailleElement(self, element: int) -> tuple:
        """Renvoie les dimensions d'un des éléments à afficher.

        Args:
            element (int): L'élément dont on souhaite connaître les dimensions.

        Returns:
            tuple: (largeur, hauteur).
        """
        l = h = 0
        if element < len(self.cles):
            cle = self.cles[element]
            elem = self.contenu[cle]
            h = elem[1].height
            tt = measure_text_ex(police1, str(elem[0]), h, 0)
            l = int(elem[1].width + self.ecartx2 + tt.x)
        return (l, h)
    
    def setValeurElement(self, element: str, valeur: int) -> None:
        """Modifie les valeurs d'un élément.

        Args:
            element (str): L'élément dont la valeur doit changer.
            valeur (int): La nouvelle valeur de l'élément.
        """
        if element in self.cles:
            self.contenu[element][0] = valeur