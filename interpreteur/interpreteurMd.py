from systeme.FondMarin import *
from ui.blocTexte import BlocTexte
from ui.scrollBarre import ScrollBarre

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
        self.position = 'gen'
        self.element = None
        self.contenu = []
        self.largeurContenu = int(self.largeur*0.95)
        self.pasx = int(xf*0.0125)
        self.oyc = self.origine[1] + self.espace
        self.pasy = int(yf*0.05)
        # Autres
        self.taillePolice = int(yf*0.035)
        # Scroll
        self.scrollBarre = ScrollBarre([self.origine[0], self.origine[1], self.largeur, self.hauteur], self.hauteurTotale)
        self.pos = self.scrollBarre.getPos()

    def dessine(self) -> None:
        """Dessine le contenu du fichier à l'écran.
        """
        if not self.decode:
            self.startDecode()
        if not self.evaluation:
            self.mesureTaille()
        if self.codeErreur == None:
            x = self.origine[0]
            ph = self.oyc
            for i in range(len(self.contenu)):
                contenu = self.contenu[i]
                if type(contenu) == list:
                    if contenu[0][0]:
                        h = self.espace
                        for j in range(len(contenu)-1):
                            h += contenu[j+1].getDims()[1]
                            if j < len(contenu)-1:
                                h += self.espace
                        couleur = contenu[0][1]
                        draw_rectangle_rounded([x+self.pasx, ph, self.largeurContenu, int(h)], 0.2, 30, couleur)
                        ph += int(self.espace/2)
                        for j in range(len(contenu)-1):
                            pt = [int(x+self.pasx*2), int(ph+self.espace/2)]
                            contenu[j+1].dessine([pt, 'no'])
                            ph += contenu[j+1].getDims()[1] + self.espace
                elif type(contenu) == BlocTexte:
                    pt = [int(x+self.pasx), int(ph+self.espace/2)]
                    contenu.dessine([pt, 'no'])
                    ph += contenu[j+1].getDims()[1] + self.espace
                elif type(contenu) == str:
                    ph += self.espace
            if self.hauteurTotale > self.hauteur:
                self.scrollBarre.dessine()
                self.pos = self.scrollBarre.getPos()
        else:
            self.erreur(self.codeErreur)

    def startDecode(self) -> None:
        """Permet de vérifier si le fichier a été décodé.
        """
        if not self.decode:
            if file_exists(self.fichier):
                if get_file_extension(self.fichier) in self.extensions:
                    self.decodeur()
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
        while len(fil) > 0:
            li = fil[0].split(" ")
            if self.position == 'gen':
                if li[0] == "<[":
                    del li[0]
                    self.position = 'cad'
                    self.element = [['cadre']]
                    li2 = li.split(",")
                    couleur = []
                    for i in range(len(li2)):
                        couleur.append(int(li2[i]))
                    self.element[0].append(couleur)
                elif fil[0] != "":
                    self.ajouteContenu(BlocTexte(fil[0], police2, self.taillePolice, [self.largeurContenu, '']))
                else:
                    self.ajouteContenu("\n")
            elif self.position == 'cad':
                if fil[0] == "]>":
                    self.position = 'gen'
                    self.ajouteContenu(self.element)
                elif fil[0] != "":
                    self.element.append(BlocTexte(fil[0], police2, self.taillePolice, 
                                        [int(self.largeurContenu*0.95), '']))
            del fil[0]

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
        titre = BlocTexte("Un probleme est survenu !", police2, self.taillePolice*1.2, [self.largeurContenu, ''])
        sousTitre = BlocTexte("Chargement interrompue.", police2, self.taillePolice, [self.largeurContenu, ''])
        if mode == 1:
            message = BlocTexte(f"Le fichier \"{self.fichier}\" est manquant.", police2, 
                                self.taillePolice*0.8, [self.largeurContenu, ''])
        elif mode == 2:
            message = BlocTexte(f"Le fichier \"{self.fichier}\" est incompatible.", police2, 
                                self.taillePolice*0.8, [self.largeurContenu, ''])
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
        self.contenu.clear()

    def mesureTaille(self) -> None:
        """Mesure la taille du contenu de la fenêtre.
        """
        h = 0
        for i in range(len(self.contenu)):
            element = self.contenu[i]
            if type(element) == list:
                if element[0][0] == 'cadre':
                    dims = self.espace*2
                    for i in range(len(element)-1):
                        if type(element[i+1]) == BlocTexte:
                            dims += element[i+1].getDims()[1]
                            dims += self.espace
                h += int(dims - self.espace)
            elif type(element) == BlocTexte:
                h += element.getDims()[1] + self.espace
            elif type(element) == str:
                h += self.espace
        if h > self.hauteur:
            self.hauteurTotale = h
            self.scrollBarre.setHtContenu(self.hauteurTotale)
        self.evaluation = True

    def ajouteContenu(self, contenu: list) -> None:
        """Permet d'ajouter du contenu dans la fenêtre.

        Args:
            contenu (list): Le contenu qu'on ajoute.
        """
        self.contenu.append(contenu)
        self.evaluation = False