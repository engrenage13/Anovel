from systeme.FondMarin import *

class ScrollBarre:
    def __init__(self, dims: list, hauteurContenu: int) -> None:
        """Crée une barre de défilement.

        Args:
            dims (list): 1. x de la zone, 2. y de la zone, 3. largeur de la zone, 4. hauteur de la zone.
            hauteurContenu (int): Hauteur de la liste du contenu de la zone à équiper.
        """
        self.ecartx = int(xf*0.0125)
        self.dimsFen = dims
        self.htContenu = hauteurContenu
        self.ecarty = int(yf*0.01)
        self.pas = int(yf*0.05)
        self.pos = int(self.dimsFen[1] + self.ecarty*2)
        self.x = self.dimsFen[0]
        self.largeur = 0
        # Affichage
        self.valeursMax = [51, 14]
        self.valeursActuelles = [51, 14]
        self.visible = True
        self.delai = 50
        # Curseur
        self.pYCurseur = 0
        self.setValeurDefaut()

    def setValeurDefaut(self) -> None:
        """Paramètres certaines valeurs utiles au fonctionnement correct de la barre.
        """
        self.nbPas = int((self.htContenu-self.dimsFen[3])/self.pas)
        self.ymin = int(self.dimsFen[1]+self.ecarty*2)
        self.ht = int(self.dimsFen[3]-self.ecarty*4)
        self.hauteur = int(self.ht*(self.dimsFen[3]/self.htContenu))

    def ChangePos(self) -> None:
        """Change la position de la barre.
        """
        if self.getContact():
            facteur = 0.4
        else:
            facteur = 0.2
        self.largeur = int(self.ecartx*facteur)
        self.x = int(self.dimsFen[0]+self.dimsFen[2]-self.ecartx*0.3-self.largeur/2)
        pas = int((self.ht-self.hauteur)/self.nbPas)
        multiplicateur = ((self.dimsFen[1] + self.ecarty) - self.pos)/self.pas
        self.y = int(self.ymin+pas*multiplicateur)

    def dessine(self) -> None:
        """Dessine la barre à l'écran.
        """
        self.ChangePos()
        if self.getContactChariot():
            couleur = [0, 121, 241, self.valeursActuelles[0]*5]
        else:
            couleur = [0, 0, 0, self.valeursActuelles[0]*5]
        draw_rectangle_rounded([self.x, self.ymin, self.largeur, self.ht], 2, 30, 
                               [200, 200, 200, self.valeursActuelles[1]*5])
        draw_rectangle_rounded([self.x, self.y, self.largeur, self.hauteur], 2, 30, couleur)
        self.bougeChariot()
        self.changeVisibilite()

    def changeVisibilite(self) -> None:
        """Gère les animations de fondu et d'apparition de la barre.
        """
        contact = self.getContactZone()
        if contact and not self.visible:
            self.visible = True
            self.delai = 50
        elif not contact:
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

    def getContact(self) -> bool:
        """Vérifie si le curseur est sur la barre.

        Returns:
            bool: True si le curseur est sur la barre.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.x and x <= self.x+self.largeur:
            if y >= self.ymin and y <= self.ht:
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
            if y >= self.y and y <= self.y+self.hauteur:
                rep = True
        return rep

    def bougeChariot(self) -> None:
        """Permet de faire défiler le contenu dans la fenêtre.
        """
        if self.getContactZone():
            # Molette
            roulette = int(get_mouse_wheel_move())
            roro = roulette
            if roro < 0:
                roro = roro*-1
            for i in range(roro):
                if roulette > 0:
                    if self.pos < self.dimsFen[1] + self.ecarty:
                        self.pos = self.pos + self.pas
                elif roulette < 0:
                    if self.pos + self.htContenu > self.dimsFen[1] + self.dimsFen[3]:
                        self.pos = self.pos - self.pas
            # Curseur
            if self.getContactChariot():
                if is_mouse_button_down(0):
                    y = get_mouse_y()
                    if y < self.pYCurseur:
                        if self.pos < self.dimsFen[1] + self.ecarty:
                            self.pos = self.pos + self.pas
                    elif y > self.pYCurseur:
                        if self.pos + self.htContenu > self.dimsFen[1] + self.dimsFen[3]:
                            self.pos = self.pos - self.pas
                    self.pYCurseur = y

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