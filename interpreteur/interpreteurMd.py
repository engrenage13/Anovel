from systeme.FondMarin import *
from interpreteur.article import Article
from interpreteur.zone import Zone
from ui.blocTexte import BlocTexte

class InterpreteurMd:
    def __init__(self, fichier: str, dims: tuple) -> None:
        """Crée un interpréteur markdown.

        Args:
            fichier (str): L'url du fichier qui doit être interprété.
            dims (tuple): La position et les dimensions de la zone dans laquelle doit s'afficher le contenu du fichier.
        """
        self.fichier = fichier
        self.decode = False
        self.position = 'gen'
        self.extensions = ['.md']
        # Zone
        self.zone = Zone(dims)
        self.element = None
        # Balises
        self.balises = ['//', 'i/', '!/']
        self.types = ['cad', 'ast', 'imp']
        # Autres
        self.taillePolice = int(yf*0.035)

    def dessine(self) -> None:
        """Permet de dessiner l'interpréteur à l'écran.
        """
        if not self.decode:
            if file_exists(self.fichier):
                if get_file_extension(self.fichier) in self.extensions:
                    self.decodeur()
                else:
                    self.erreur(2)
            else:
                self.erreur(1)
            self.decode = True
        self.zone.dessine()

    def decodeur(self) -> None:
        """Permet de décoder le texte du fichier traiter.
        """
        fic = load_file_text(self.fichier)
        fil = fic.split("\n")
        while len(fil) > 0:
            li = fil[0].split(" ")
            if self.position == 'gen':
                if li[0] in self.balises:
                    balise = self.types[self.balises.index(li[0])]
                    del li[0]
                    self.zone.ajouteContenu([balise, BlocTexte(" ".join(li), police2, self.taillePolice, 
                                                [int(self.zone.largeurContenu*0.95), ''])])
                elif fil[0] == "_art//":
                    self.element = Article()
                    self.element.redim(self.zone.largeurContenu, self.element.hauteur)
                    self.position = 'art'
                elif fil[0] != "":
                    self.zone.ajouteContenu(['t', BlocTexte(fil[0], police2, self.taillePolice, 
                                                [self.zone.largeurContenu, ''])])
            elif self.position == 'art':
                rep = self.element.decodeur(fil[0])
                if rep:
                    self.element.getDims()
                    self.zone.ajouteContenu(self.element)
                    self.position = 'gen'
            del fil[0]

    def erreur(self, mode: int) -> None:
        """Definit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.

        Args:
            mode (int): Définit le type d'erreur rencontrer.
        """
        self.zone.ajouteContenu(['', BlocTexte("Un probleme est survenu !", police2, self.taillePolice*1.2, 
                                [self.zone.largeurContenu, ''])])
        self.zone.ajouteContenu(['', BlocTexte("Chargement interrompue.", police2, self.taillePolice, 
                                [self.zone.largeurContenu, ''])])
        if mode == 1:
            self.zone.ajouteContenu(['', BlocTexte("Le fichier n'existe pas ou n'est pas au bon endroit.", 
                                       police2, self.taillePolice*0.8, [self.zone.largeurContenu, ''])])
        elif mode == 2:
            self.zone.ajouteContenu(['', BlocTexte("Ce fichier n'est pas prit en compte", 
                                       police2, self.taillePolice*0.8, [self.zone.largeurContenu, ''])])

    def changeFichier(self, fichier: str) -> None:
        """Permet de changer le fichier qu'utilise l'interpréteur.

        Args:
            fichier (str): Nouveau fichier utilisé par l'interpréteur.
        """
        self.fichier = fichier
        self.decode = False
        self.zone.contenu.clear()