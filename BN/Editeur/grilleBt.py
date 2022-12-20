from systeme.FondMarin import *
from ui.bouton import Bouton
from ui.ptiBouton import PtiBouton

class GrilleBt:
    def __init__(self) -> None:
        """Crée une grille à boutons.
        """
        self.grille = [[]]
        self.largeur = 0
        self.hauteur = 0
        self.espaceX = int(tlatba*0.06)
        self.espaceY = int(yf*0.05)
        # Compte à rebours
        self.car = False
        self.decompte = 0
        self.valeurInitiale = self.decompte
        self.objectif = None
        self.play = False
        self.temps = 0
        self.t2 = 0.0
        self.tdep = None
        self.largeurChrono = 0
        self.hauteurChrono = 0
        # Décors
        self.adresse = "images/BN/ui/jauge.png"
    
    def dessine(self, x: int, y: int, important: list) -> None:
        """Dessine la grille.

        Args:
            x (int): Position x du coin gauche supérieur.
            y (int): Position y du coin gauche supérieur.
            important (list): Liste de booléens pour l'option important de chacun des boutons.
        """
        draw_rectangle_rounded([x, y, self.largeur, self.hauteur], 0.2, 30, [255, 255, 255, 50])
        draw_rectangle_rounded_lines([x, y, self.largeur, self.hauteur], 0.2, 30, 3, WHITE)
        if self.car:
            self.dessineChrono(x, int(y+yf*0.02))
        py = y + self.hauteur - int(yf*0.02)
        k = 0
        for i in range(len(self.grille)):
            px = x + self.largeur - int(tlatba*0.05)
            idligne = len(self.grille)-1-i
            if len(self.grille[idligne]) == 1:
                actif = important[len(important)-1-k]
                k = k + 1
                telem = self.grille[idligne][0].getDims()
                self.grille[idligne][0].dessine((x+int(self.largeur/2), py-int(telem[1]/2)), actif)
            else:
                for j in range(len(self.grille[idligne])):
                    idcol = len(self.grille[idligne])-1-j
                    actif = important[len(important)-1-k]
                    k = k + 1
                    telem = self.grille[idligne][idcol].getDims()
                    self.grille[idligne][idcol].dessine((px-int(telem[0]/2), py-int(telem[1]/2)), actif)
                    px -= telem[0] + self.espaceX
            py -= telem[1] + self.espaceY

    def dessineChrono(self, x: int, y: int) -> None:
        """Permet de dessiner le compte à rebours.

        Args:
            x (int): Position des abcisses du coin supérieur gauche du cadre de la grille.
            y (int): Position des ordonnées correspondant au sommet du compte à rebours.
        """
        if self.tdep == None and self.play:
            temps = int(get_time())
            self.tdep = round(temps, 2)
            self.temps = 0
        c = int(self.largeur/2)
        r = int(self.hauteurChrono*0.25)
        lmax = int(self.largeur*0.29)
        prop = (self.valeurInitiale-self.temps-self.t2)/self.valeurInitiale
        l = int(lmax*prop)
        draw_rectangle(int(x+c-r*0.9-l), int(y+self.hauteurChrono*0.4), l, int(self.hauteurChrono*0.2), 
                       [117, 200, 235, 80])
        draw_rectangle(int(x+c+r*0.9), int(y+self.hauteurChrono*0.4), l, int(self.hauteurChrono*0.2), 
                       [117, 200, 235, 80])
        draw_circle_gradient(int(x+c-self.largeurChrono*0.44), int(y+self.hauteurChrono*0.52), int(r/5), 
                             [32, 45, 226, 200], [0, 12, 72, 200])
        draw_circle_gradient(int(x+c+self.largeurChrono*0.44), int(y+self.hauteurChrono*0.52), int(r/5), 
                             [32, 45, 226, 200], [0, 12, 72, 200])
        draw_circle(x+c, int(y+self.hauteurChrono/2), r, [117, 200, 235, 80])
        draw_texture(self.decoJauge, int(x+c-self.decoJauge.width/2), 
                     int(y+self.hauteurChrono/2-self.decoJauge.height/2), [213, 222, 226, 255])
        tx = measure_text_ex(police1, str(self.decompte), int(self.hauteurChrono*0.3), 0)
        draw_text_ex(police1, str(self.decompte), (int(x+c-tx.x*0.54), int(y+self.hauteurChrono/2-tx.y*0.37)), 
                     int(self.hauteurChrono*0.3), 0, WHITE)
        if self.play:
            if self.decompte > 0:
                t = round(get_time(), 2)
                if round(t-self.tdep-self.temps, 2) >= 1:
                    self.decompte -= 1
                    self.temps += 1
                    self.t2 = 0.0
                else:
                    self.t2 = round(t-self.tdep-self.temps, 2)
            else:
                self.objectif()

    def ajouteElement(self, element: object, x: int, y: int) -> None:
        """Permet d'ajouter un nouvel élément à la grille.

        Args:
            element (object): Element à ajouter.
            x (int): Colonne de la grille sur la-quelle ajouter l'element.
            y (int): Ligne de la grille sur la-quelle ajouter l'element.
        """
        if type(element) in [Bouton, PtiBouton]:
            if y < len(self.grille):
                ligne = self.grille[y]
                if x <= 0:
                    self.grille[y] = [element] + ligne
                else:
                    self.grille[y].append(element)
            else:
                self.grille.append([element])
            self.setDims()

    def setDims(self) -> None:
        """Modifie les dimensions de la grille pour qu'elle s'adapte à son contenu.
        """
        l = 0
        h = 0
        ligne = 0
        g = len(self.grille[0])
        for i in range(len(self.grille)):
            if g < len(self.grille[i]):
                g = len(self.grille[i])
                ligne = i
        for i in range(g):
            taille = self.grille[ligne][i].getDims()
            l = l + taille[0]
        l = l + int(self.espaceX*(g-1)+tlatba*0.05*2)
        for i in range(len(self.grille)):
            taille = self.grille[i][0].getDims()
            h = h + taille[1]
        h = h + int(yf*0.02*2+self.espaceY*(len(self.grille)-1))
        self.largeur = l
        self.hauteur = h
        if self.car:
            self.setDimsChrono()

    def setDimsChrono(self) -> None:
        """Permet de modifier les dimensions du compte à rebours en fonction des dimensions du cadre.
        """
        jauge = load_image(self.adresse)
        t = self.largeur*0.9
        if t < tlatba*0.7:
            t = tlatba*0.7
        prop = t/jauge.width
        image_resize(jauge, int(jauge.width*prop), int(jauge.height*prop))
        self.decoJauge = load_texture_from_image(jauge)
        unload_image(jauge)
        self.largeurChrono = int(self.decoJauge.width)
        self.hauteurChrono = int(self.decoJauge.height*1.05)
        if self.largeurChrono >= self.largeur:
            self.largeur = int(self.largeurChrono*1.1)
        self.hauteur += int(self.hauteurChrono+self.espaceY*0.1)

    def setChrono(self, temps: int, fonction) -> None:
        """Permet de paramètrer un compte un rebours dans la grille de bouton.

        Args:
            temps (int): Le temps imparti pour le compte à rebours.
            fonction (_type_): la fonction à executer lorsque le décompte arrive à 0.
        """
        if temps < 0:
            temps = temps*-1
        self.car = True
        self.play = False
        self.decompte = temps
        self.valeurInitiale = temps
        self.objectif = fonction

    def startChrono(self) -> None:
        """Permet de lancer le compte à rebours (il doit être programmé avant).
        """
        self.play = True
        self.temps = 0
        self.t2 = 0.0
        self.tdep = None
        self.decompte = self.valeurInitiale

    def stopChrono(self) -> None:
        """Permet d'arrêter le compte à rebours.
        """
        self.play = False