from systeme.FondMarin import *

class ScrollBarre:
    def __init__(self, dims: list, hauteurContenu: int, couleurs: list=[[0, 0, 0], [0, 121, 241]]) -> None:
        """Crée une barre de défilement.

        Args:
            dims (list): 1. x de la zone, 2. y de la zone, 3. largeur de la zone, 4. hauteur de la zone.
            hauteurContenu (int): Hauteur de la liste du contenu de la zone à équiper.
            couleurs (list): 1. couleur du chariot immobile, 2. couleur du chariot en mouvement.
        """
        self.ecartx = int(xf*0.0125)
        self.dimsFen = dims
        self.htContenu = hauteurContenu
        self.ecarty = int(yf*0.01)
        self.pas = int(yf*0.05)
        self.pos = int(self.dimsFen[1] + self.ecarty*2)
        self.largeur = int(self.ecartx*0.4)
        self.x = int(self.dimsFen[0]+self.dimsFen[2]-self.ecartx*0.3-self.largeur/2)
        # Affichage
        self.valeursMax = [51, 14]
        self.valeursActuelles = [51, 14]
        self.visible = True
        self.delai = 50
        # Chariot
        self.defil = False
        self.couleurs = couleurs
        self.setValeurDefaut()

    def setValeurDefaut(self) -> None:
        """Paramètres certaines valeurs utiles au fonctionnement correct de la barre.
        """
        self.ybarre = int(self.dimsFen[1]+self.ecarty*2)
        self.y = self.ybarre
        self.ht = int(self.dimsFen[3]-self.ecarty*4)
        self.hChariot = int(self.ht*(self.dimsFen[3]/self.htContenu))

    def dessine(self, afficheRail: bool=False) -> None:
        """Dessine la barre à l'écran.

        Args:
            afficheRail (bool): Permet de préciser si oui ou non, on veut afficher le rail.
        """
        if self.getContactChariot() or self.defil:
            c = self.couleurs[1]
        else:
            c = self.couleurs[0]
        couleur = [c[0], c[1], c[2], self.valeursActuelles[0]*5]
        if afficheRail:
            draw_rectangle_rounded([self.x, self.ybarre, self.largeur, self.ht], 2, 30, 
                                    [200, 200, 200, self.valeursActuelles[1]*5])
        draw_rectangle_rounded([self.x, self.y, self.largeur, self.hChariot], 2, 30, couleur)
        self.bougeChariot()
        self.changeVisibilite()

    def changeVisibilite(self) -> None:
        """Gère les animations de fondu et d'apparition de la barre.
        """
        contact = self.getContactZone()
        if contact and not self.visible:
            self.visible = True
            self.delai = 50
        elif not contact and not self.defil:
            if self.visible:
                self.visible = False
            if self.delai > 0:
                self.delai -= 1
        for i in range(len(self.valeursActuelles)):
            if self.visible and self.valeursActuelles[i] < self.valeursMax[i]:
                self.valeursActuelles[i] += 1
            elif not self.visible and self.valeursActuelles[i] > 0:
                if self.delai == 0:
                    self.valeursActuelles[i] -= 1

    def getContactZone(self) -> bool:
        """Vérifie si le curseur est dans la zone équipée.

        Returns:
            bool: True si le curseur est dans la zone
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.dimsFen[0] and x <= self.dimsFen[0]+self.dimsFen[2]:
            if y >= self.dimsFen[1] and y <= self.dimsFen[1]+self.dimsFen[3]:
                rep = True
        return rep

    def getContactChariot(self) -> bool:
        """Vérifie si le curseur est sur le chariot.

        Returns:
            bool: True si le curseur est sur le chariot.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.x and x <= self.x+self.largeur:
            if y >= self.y and y <= self.y+self.hChariot:
                rep = True
        return rep

    def bougeChariot(self) -> None:
        """Permet de faire défiler le contenu dans la fenêtre.
        """
        # Molette
        if self.getContactZone():
            roulette = int(get_mouse_wheel_move())
            roro = roulette
            if roro < 0:
                roro = roro*-1
            for i in range(roro):
                if roulette > 0:
                    if self.y > self.ybarre:
                        if self.pas > self.y-self.ybarre:
                            pas = self.y-self.ybarre
                        else:
                            pas = self.pas
                        self.y = self.y - pas
                elif roulette < 0:
                    if self.y+self.hChariot < self.ybarre + self.ht:
                        if self.pas > (self.ybarre + self.ht)-(self.y+self.hChariot):
                            pas = (self.ybarre + self.ht)-(self.y+self.hChariot)
                        else:
                            pas = self.pas
                        self.y = self.y + pas
                posChariot = (self.y-self.ybarre)/self.ht
                self.pos = int(self.ybarre-self.htContenu*posChariot)
        # Curseur
        if not self.defil:
            if self.getContactChariot() and is_mouse_button_down(0):
                self.defil = True
        else:
            y = get_mouse_y()
            if y < self.ybarre:
                y = self.ybarre
            elif y+self.hChariot > self.ybarre+self.ht:
                y = self.ybarre+self.ht-self.hChariot
            self.y = y
            posChariot = (y-self.ybarre)/self.ht
            self.pos = int(self.ybarre-self.htContenu*posChariot)
            if is_mouse_button_up(0):
                self.defil = False

    def getPos(self) -> int:
        """Retourne la position du chariot sur la barre.

        Returns:
            int: _description_
        """
        return self.pos

    def setHtContenu(self, htContenu: int) -> None:
        """Permet de modifier la hauteur du contenu renseignée.

        Args:
            htContenu (int): Nouvelle hauteur pour le contenu.
        """
        self.htContenu = htContenu
        self.setValeurDefaut()