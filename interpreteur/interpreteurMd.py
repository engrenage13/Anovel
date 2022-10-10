from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from ui.scrollBarre import ScrollBarre
from ui.PosiJauge import PosiJauge
from interpreteur.decodeuses import texte, widget, cadre, checkFinCadre
from interpreteur.dimensions import mesureTaille
from interpreteur.dessin import dessinePosiJauge, dessineTexte, dessineCadre

class InterpreteurMd:
    def __init__(self, fichier: str, dims: tuple) -> None:
        """Crée un interpréteur markdown.

        Args:
            fichier (str): L'url du fichier qui doit être interprété.
            dims (tuple): La position et les dimensions de la zone dans laquelle doit s'afficher le contenu du fichier.
        """
        # Fichier
        self.fichier = fichier
        self.decode = False
        self.extensions = ['.md']
        self.codeErreur = None
        # Zone
        self.origine = (dims[0], dims[1])
        self.largeur = dims[2]
        self.hauteur = dims[3]
        self.hauteurTotale = self.hauteur
        self.espace = int(yf*0.03)
        self.evaluation = False
        # Elements
        self.contenu = []
        self.lContenu = int(self.largeur*0.95)
        self.pasx = int(xf*0.0125)
        self.pasy = int(yf*0.05)
        # Autres
        self.taillePolice = int(yf*0.035)
        # Scroll
        self.scrollBarre = ScrollBarre([self.origine[0], self.origine[1], self.largeur, self.hauteur], 
                                        self.hauteurTotale, [[1, 8, 38], [12, 37, 131]])
        self.oyc = self.scrollBarre.getPos()

    def dessine(self) -> None:
        """Dessine le contenu du fichier à l'écran.
        """
        if not self.decode:
            self.startDecode()
        if not self.evaluation:
            self.setHauteurContenu()
        if self.codeErreur == None:
            x = self.origine[0]+self.pasx
            ph = self.oyc
            for i in range(len(self.contenu)):
                element = self.contenu[i]
                if type(element) == list and type(element[0]) == list:
                    ph += dessineCadre(element, x, ph, self.espace)[1] + self.espace
                elif type(element) == BlocTexte:
                    ph += dessineTexte(element, x, ph)[1] + int(self.espace/2)
                elif type(element) == PosiJauge:
                    ph += dessinePosiJauge(element, x, ph, self.lContenu)[1] + self.espace
                elif type(element) == str:
                    ph += self.espace
            if self.hauteurTotale > self.hauteur:
                self.scrollBarre.dessine()
                self.oyc = self.scrollBarre.getPos()
        else:
            self.erreur(self.codeErreur)

    def startDecode(self) -> None:
        """Permet de vérifier si le fichier a été décodé.
        """
        if not self.decode:
            if file_exists(self.fichier):
                if get_file_extension(self.fichier) in self.extensions:
                    self.decodeur()
                    if self.codeErreur != None:
                        self.chargeImaErreur()
                else:
                    self.codeErreur = 2
                    self.chargeImaErreur()
            else:
                self.codeErreur = 1
                self.chargeImaErreur()
            self.decode = True

    def decodeur(self) -> None:
        """Permet de décoder le texte du fichier traiter.
        """
        fic = load_file_text(self.fichier)
        fil = fic.split("\n")
        cadres = []
        while len(fil) > 0:
            if ">" in fil[0]:
                rep = widget(fil[0])
                if type(rep) == list:
                    if len(rep[1]) > 0:
                        self.codeErreur = rep[1][0]
                    if len(cadres) == 0:
                        self.ajouteContenu(rep[0])
                    else:
                        cadres[len(cadres)-1].append(rep[0])
                    if checkFinCadre(fil[0]):
                        self.finCadre(cadres)
            elif "[" in fil[0]:
                rep = cadre(fil[0])
                prop = self.pasx/self.lContenu
                largeur = int(self.lContenu*(1-prop*2*(len(cadres))))
                cadres.append([[largeur]+rep])
            elif fil[0] == "]":
                self.finCadre(cadres)
            elif fil[0] != "":
                prop = self.pasx/self.lContenu
                rep = texte(fil[0], self.taillePolice, int(self.lContenu*(1-prop*2*(len(cadres)))))
                if len(cadres) == 0:
                    self.ajouteContenu(rep)
                else:
                    cadres[len(cadres)-1].append(rep)
            else:
                if len(cadres) == 0:
                    self.ajouteContenu("\n")
                else:
                    cadres[len(cadres)-1].append("\n")
            del fil[0]

    def finCadre(self, cadres: list) -> list:
        if len(cadres) > 0:
            cad = cadres[len(cadres)-1]
            del cadres[len(cadres)-1]
            if len(cadres) > 0:
                cadres[len(cadres)-1].append(cad)
            else:
                self.ajouteContenu(cad)
        return cadres

    def chargeImaErreur(self) -> None:
        """Permet de charger l'image pour les erreurs.
        """
        tableau = load_image('images/ui/erreur.png')
        ratio = yf/2/tableau.height
        image_resize(tableau, int(tableau.width*ratio), int(tableau.height*ratio))
        self.iErreur = load_texture_from_image(tableau)
        unload_image(tableau)

    def erreur(self, mode: int) -> None:
        """Definit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.

        Args:
            mode (int): Définit le type d'erreur rencontrée.
        """
        draw_rectangle(self.origine[0], self.origine[1], self.largeur, self.hauteur, BLACK)
        draw_texture(self.iErreur, int(self.origine[0]+self.largeur/2-self.iErreur.width/2), 
                     int(yf*0.4-self.iErreur.height/2), WHITE)
        titre = BlocTexte("Un probleme est survenu !", police2, self.taillePolice*1.2, [self.lContenu, ''])
        sousTitre = BlocTexte("Chargement interrompue.", police2, self.taillePolice, [self.lContenu, ''])
        if mode == 1:
            message = BlocTexte(f"Le fichier \"{self.fichier}\" est manquant.", police2, 
                                self.taillePolice*0.8, [self.lContenu, ''])
        elif mode == 2:
            message = BlocTexte(f"Le fichier \"{self.fichier}\" est incompatible.", police2, 
                                self.taillePolice*0.8, [self.lContenu, ''])
        else:
            message = BlocTexte(mode, police2, self.taillePolice*0.8, [self.lContenu, ''])
        titre.dessine([[int(self.origine[0]+self.largeur/2), int(self.origine[1]+self.hauteur*0.7)], 'c'])
        sousTitre.dessine([[int(self.origine[0]+self.largeur/2), int(self.origine[1]+self.hauteur*0.75)], 'c'])
        message.dessine([[int(self.origine[0]+self.largeur/2), int(self.origine[1]+self.hauteur*0.8)], 'c'], 
                        [242, 171, 56, 255])

    def changeFichier(self, fichier: str) -> None:
        """Permet de changer le fichier qu'utilise l'interpréteur.

        Args:
            fichier (str): Nouveau fichier utilisé par l'interpréteur.
        """
        self.fichier = fichier
        self.decode = False
        self.codeErreur = None
        self.contenu.clear()

    def setHauteurContenu(self) -> None:
        """Modifie la taille théorique de la totalité du contenu de la fenêtre.
        """
        self.hauteurTotale = mesureTaille(self.contenu, self.espace)
        if self.hauteurTotale > self.hauteur:
            self.scrollBarre.setHtContenu(self.hauteurTotale)
        self.evaluation = True

    def ajouteContenu(self, contenu: list) -> None:
        """Permet d'ajouter du contenu dans la fenêtre.

        Args:
            contenu (list): Le contenu qu'on ajoute.
        """
        self.contenu.append(contenu)
        self.evaluation = False