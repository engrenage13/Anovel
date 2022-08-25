from systeme.FondMarin import *
from ui.blocTexte import BlocTexte

class Menu:
    def __init__(self, fichier: str, dims: tuple) -> None:
        """Crée un menu pour les paramètres.

        Args:
            fichier (str): L'url du fichier qui doit être interprété.
            dims (tuple): La position et les dimensions de la zone où doit s'afficher le menu.
        """
        self.fichier = fichier
        self.decode = False
        self.bug = False
        self.extension = '.md'
        self.contenu = []
        # Zone
        self.origine = (dims[0], dims[1])
        self.largeur = dims[2]
        self.hauteur = dims[3]
        self.hauteurTotale = self.hauteur
        self.largeurContenu = int(self.largeur*0.9)
        self.hauteurContenu = int(yf*0.09)
        self.espace = int(yf*0.02)
        self.pos = int(self.origine[1] + self.espace)
        self.pas = int(yf*0.05)
        self.nbPas = 0
        # Autres
        self.taillePolice = int(yf*0.045)

    def dessine(self) -> None:
        """Permet de dessiner l'interpréteur à l'écran.
        """
        if not self.decode:
            if file_exists(self.fichier) and get_file_extension(self.fichier) == self.extension:
                self.decodeur()
                self.mesureTaille()
            else:
                self.erreur()
            self.decode = True
        elif not self.bug:
            x = int(self.origine[0] + (self.largeur-self.largeurContenu)/2)
            y = self.pos
            for i in range(len(self.contenu)):
                draw_rectangle_rounded([x, y, self.largeurContenu, self.hauteurContenu], 0.2, 30, 
                                        [120, 120, 120, 70])
                self.contenu[i][0].dessine([[int(x+self.largeurContenu*0.05), int(y+self.hauteurContenu*0.2)], 
                                           'no'], alignement='g')
                y = y + self.hauteurContenu + self.espace
            if self.hauteurTotale > self.hauteur:
                self.dessineBarre()
                self.bougeChariot()
        else:
            titre = BlocTexte("Un probleme est survenu !", police2, self.taillePolice*1.2, 
                              [self.largeurContenu, ''])
            texte = BlocTexte("Chargement interrompue.", police2, self.taillePolice, [self.largeurContenu, ''])
            titre.dessine([[int(self.origine[0]+self.largeur/2), int(self.origine[1]+self.hauteur*0.34)], 'c'])
            texte.dessine([[int(self.origine[0]+self.largeur/2), int(self.origine[1]+self.hauteur*0.4)], 'c'])

    def dessineBarre(self) -> None:
        """Dessine la barre indiquant le défilement du contenu.
        """
        ecart = int(xf*0.0125)
        ymin = int(self.origine[1]+self.espace*0.5)
        l = int(ecart*0.2)
        ht = int(self.hauteur-self.espace)
        h = int(ht*(self.hauteur/self.hauteurTotale))
        x = int(self.origine[0]+self.largeur-ecart*0.3-l/2)
        pas = int((ht-h)/self.nbPas)
        multiplicateur = ((self.origine[1] + self.espace) - self.pos)/self.pas
        y = int(ymin+pas*multiplicateur)
        draw_rectangle_rounded([x, y, l, h], 2, 30, BLACK)

    def bougeChariot(self) -> None:
        """Permet de faire défiler le contenu dans la fenêtre.
        """
        roulette = int(get_mouse_wheel_move())
        roro = roulette
        if roro < 0:
            roro = roro*-1
        for i in range(roro):
            if roulette > 0:
                if self.pos < self.origine[1] + self.espace:
                    self.pos = self.pos + self.pas
            elif roulette < 0:
                if self.pos + self.hauteurTotale > self.origine[1] + self.hauteur:
                    self.pos = self.pos - self.pas

    def decodeur(self) -> None:
        """Permet de décoder le texte du fichier traiter.
        """
        fic = load_file_text(self.fichier)
        fil = fic.split("\n")
        while len(fil) > 0:
            if len(fil[0]) > 0 and fil[0][0] == '-':
                li = fil[0]
                titre = ""
                fichier = ""
                go = False
                for i in range(len(li)):
                    if go == 't':
                        if li[i] == ']':
                            go = False
                        else:
                            titre = titre + li[i]
                    elif go == 'f':
                        if li[i] == ')':
                            go = False
                        else:
                            fichier = fichier + li[i]
                    else:
                        if li[i] == '[':
                            go = 't'
                        elif li[i] == '(':
                            go = 'f'
                self.contenu.append([BlocTexte(titre, police2, self.taillePolice, 
                                    [int(self.largeurContenu*0.9), '']), fichier])
            del fil[0]

    def mesureTaille(self) -> None:
        """Mesure la taille du contenu de la fenêtre.
        """
        h = self.espace
        for i in range(len(self.contenu)):
            h += int(self.hauteurContenu + self.espace)
        if h > self.hauteur:
            self.hauteurTotale = h
            self.nbPas = int((self.hauteurTotale-self.hauteur)/self.pas)

    def erreur(self) -> None:
        """Déclenche l'affichage d'un message d'erreur concernant le fichier.
        """
        self.bug = True