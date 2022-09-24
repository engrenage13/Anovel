from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from ui.scrollBarre import ScrollBarre

class Menu:
    def __init__(self, fichier: str, dims: tuple) -> None:
        """Crée un menu pour les paramètres.

        Args:
            fichier (str): L'url du fichier qui doit être interprété.
            dims (tuple): La position et les dimensions de la zone où doit s'afficher le menu.
        """
        self.fichier = fichier
        self.extension = '.md'
        self.contenu = []
        self.actif = 0
        # Zone
        self.origine = (dims[0], dims[1])
        self.largeur = dims[2]
        self.hauteur = dims[3]
        self.hauteurTotale = self.hauteur
        self.largeurContenu = int(self.largeur*0.9)
        self.hauteurContenu = int(yf*0.09)
        self.espace = int(yf*0.01)
        # Scroll
        self.scrollBarre = ScrollBarre([self.origine[0], self.origine[1], self.largeur, self.hauteur], self.hauteurTotale)
        self.pos = self.scrollBarre.getPos()
        # Autres
        self.taillePolice = int(yf*0.045)

    def dessine(self) -> None:
        """Permet de dessiner l'interpréteur à l'écran.
        """
        x = int(self.origine[0] + (self.largeur-self.largeurContenu)/2)
        y = self.pos
        for i in range(len(self.contenu)):
            if i == self.actif:
                draw_rectangle_rounded([x*0.3, y+self.hauteurContenu*0.1, self.largeurContenu*0.02, 
                                        self.hauteurContenu*0.8], 1, 30, [43, 55, 234, 255])
                couleur = BLUE
            else:
                couleur = WHITE
            contact = self.getContact(i)
            if contact[0]:
                draw_rectangle_rounded([x, y, self.largeurContenu, self.hauteurContenu], 0.2, 30, 
                                        [120, 120, 120, 70])
            if contact[1]:
                self.actif = i
            self.contenu[i][0].dessine([[int(x+self.largeurContenu*0.05), int(y+self.hauteurContenu*0.2)], 
                                        'no'], couleur, 'g')
            y = y + self.hauteurContenu + self.espace
        if self.hauteurTotale > self.hauteur:
            self.scrollBarre.dessine()
            self.pos = self.scrollBarre.getPos()

    def checkFichier(self) -> bool:
        """Vérifie si le fichier existe et lance le décodage.

        Return:
            bool : True si le fichier a pu être trouvé, False sinon.
        """
        if file_exists(self.fichier) and get_file_extension(self.fichier) == self.extension:
            self.decodeur()
            self.mesureTaille()
            rep = True
        else:
            rep = False
        return rep

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
            self.scrollBarre.setHtContenu(self.hauteurTotale)

    def getContact(self, indice: int) -> bool:
        """Vérifie si le curseur survol et si l'utilisateur clique sur un onglet du menu.

        Args:
            indice (int): L'indice de l'onglet testé.

        Returns:
            list: 1. True si le curseur est sur l'onglet, False dans le cas contraire. 2. True si l'utilisateur a cliqué.
        """
        xc = int(self.origine[0] + (self.largeur-self.largeurContenu)/2)
        yc = self.pos + (self.hauteurContenu + self.espace)*indice
        coord = [xc, yc, self.largeurContenu, self.hauteurContenu]
        survol = False
        clic = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= coord[1] and y <= coord[1]+coord[3]:
            if x >= coord[0] and x <= coord[0]+coord[2]:
                survol = True
                if is_mouse_button_pressed(0):
                    clic = True
        return [survol, clic]