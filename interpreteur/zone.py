from systeme.FondMarin import *
from interpreteur.article import Article

class Zone:
    def __init__(self, dims: tuple) -> None:
        """Crée la fenêtre de l'interpréteur.

        Args:
            dims (tuple): Dimensions souhaitées pour la fenêtre.
        """
        self.contenu = []
        self.origine = (dims[0], dims[1])
        self.largeur = dims[2]
        self.hauteur = dims[3]
        self.hauteurTotale = self.hauteur
        self.espace = int(yf*0.03)
        self.evaluation = False
        self.types = ['cad', 'ast', 'imp']
        # Contenu
        self.largeurContenu = int(self.largeur*0.95)
        self.pasx = int(xf*0.0125)
        self.oyc = self.origine[1] + self.espace
        self.pasy = int(yf*0.05)

    def dessine(self) -> None:
        """Dessine la fenêtre.
        """
        if not self.evaluation:
            self.mesureTaille()
        x = self.origine[0]
        y = self.origine[1]
        ph = self.oyc
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                dims = self.contenu[i].getDims()
                self.contenu[i].dessine(x+self.pasx, ph)
                ph = int(ph + dims[1] + self.espace)
            else:
                typ = self.contenu[i][0]
                contenu = self.contenu[i][1]
                tt = contenu.getDims()
                pt = [x+self.pasx, ph]
                if typ in self.types:
                    couleur = [20, 20, 20, 145]
                    if typ == 'ast':
                        couleur = [22, 29, 124, 145]
                    elif typ == 'imp':
                        couleur = [145, 18, 18, 145]
                    draw_rectangle_rounded([x+self.pasx, ph, self.largeurContenu, int(tt[1]+self.espace)], 
                                           0.2, 30, couleur)
                    pt = [int(x+self.pasx*2), int(ph+self.espace/2)]
                alig = 'g'
                if typ in self.types and contenu.getNbLignes() == 1:
                    alig = 'c'
                contenu.dessine([pt, 'no'], alignement=alig)
                nbEspace = 1
                if typ in self.types:
                    nbEspace = 2
                ph = int(ph + tt[1] + self.espace*nbEspace)
        if self.hauteur == yf:
            self.dessineBarre()
        self.bougeChariot()

    def dessineBarre(self) -> None:
        """Dessine la barre indiquant le défilement du contenu.
        """
        ymin = int(self.origine[1]+self.espace*0.5)
        l = int(self.pasx*0.4)
        ht = int(self.hauteur-ymin-self.espace)
        h = int(ht*(self.hauteur/self.hauteurTotale))
        x = int(xf/2+self.largeur/2-self.pasx/2-l/2)
        ecart = int(round((self.oyc+self.hauteurTotale-self.hauteur)/self.hauteurTotale, 2)*100)
        if int(h*100/ht+ecart) > 100:
            ecart = int(100-h*100/ht)
        elif ecart < 0:
            ecart = 0
        y = int(ymin+ht-h-ht*(ecart/100))
        draw_rectangle(x, y, l, h, BLUE)

    def bougeChariot(self) -> None:
        """Permet de faire défiler le contenu dans la fenêtre.
        """
        roulette = int(get_mouse_wheel_move())
        roro = roulette
        if roro < 0:
            roro = roro*-1
        for i in range(roro):
            if roulette > 0:
                if self.oyc < self.origine[1] + self.espace:
                    self.oyc = self.oyc + self.pasy
            elif roulette < 0:
                if self.oyc + self.hauteurTotale > self.origine[1] + self.hauteur:
                    self.oyc = self.oyc - self.pasy

    def mesureTaille(self) -> None:
        """Mesure la taille du contenu de la fenêtre.
        """
        h = 0
        for i in range(len(self.contenu)):
            if type(self.contenu[i]) == Article:
                dims = self.contenu[i].getDims()
                h += int(dims[1] + self.espace)
            elif type(self.contenu[i]) == list:
                nbEspace = 1
                if self.contenu[i][0] in self.types:
                    nbEspace = 2
                dims = self.contenu[i][1].getDims()
                h += int(dims[1] + self.espace*nbEspace)
        if h > self.hauteur:
            self.hauteurTotale = h
        self.evaluation = True

    def ajouteContenu(self, contenu: object) -> None:
        """Permet d'ajouter du contenu dans la fenêtre.

        Args:
            contenu (list): Le contenu qu'on ajoute.
        """
        self.contenu.append(contenu)
        self.evaluation = False