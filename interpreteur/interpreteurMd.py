from systeme.FondMarin import *
from interpreteur.article import Article
from interpreteur.fenetre import Fenetre
from ui.blocTexte import BlocTexte

class InterpreteurMd:
    def __init__(self, fichier: str, dims:tuple=(int(xf/2), int(yf/2)), redim:bool=True) -> None:
        """Crée un interpréteur markdown.

        Args:
            fichier (str): L'url du fichier qui doit être interpréteur.
            dims (tuple, optional): Les dimensions souhaitées pour la fenêtre. Defaults to (int(xf/2), int(yf/2)).
            redim (bool, optional): Option permettant de dire si la fenêtre est redimensionnable. Defaults to True.
        """
        self.fichier = fichier
        self.decode = False
        self.position = 'gen'
        self.extensions = ['.md']
        # Fenetre
        self.fenetre = Fenetre(dims, redim)
        self.element = None
        # Balises
        self.balises = ['//', 'i/', '!/']
        self.types = ['cad', 'ast', 'imp']
        # Autres
        self.taillePolice = int(yf*0.035)

    def dessine(self) -> None:
        """Permet de dessiner l'interpréteur à l'écran.
        """
        if self.fenetre.ouvert:
            if not self.decode:
                if file_exists(self.fichier):
                    if get_file_extension(self.fichier) in self.extensions:
                        self.decodeur()
                    else:
                        self.erreur(2)
                else:
                    self.erreur(1)
                self.decode = True
            self.fenetre.dessine()

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
                    self.fenetre.ajouteContenu([balise, BlocTexte(" ".join(li), police2, self.taillePolice, 
                                                [int(self.fenetre.largeurContenu*0.95), ''])])
                elif fil[0] == "_fen//":
                    self.position = 'fen'
                elif fil[0] == "_art//":
                    self.element = Article()
                    self.element.redim(self.fenetre.largeurContenu, self.element.hauteur)
                    self.position = 'art'
                elif fil[0] != "":
                    self.fenetre.ajouteContenu(['t', BlocTexte(fil[0], police2, self.taillePolice, 
                                                [self.fenetre.largeurContenu, ''])])
            elif self.position == 'fen':
                rep = self.fenetre.decodeur(fil[0])
                if rep:
                    self.position = 'gen'
            elif self.position == 'art':
                rep = self.element.decodeur(fil[0])
                if rep:
                    self.element.getDims()
                    self.fenetre.ajouteContenu(self.element)
                    self.position = 'gen'
            del fil[0]

    def erreur(self, mode: int) -> None:
        """Definit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.

        Args:
            mode (int): Définit le type d'erreur rencontrer.
        """
        self.fenetre.setTitre("Erreur")
        if mode == 1:
            self.fenetre.ajouteContenu(['cad', BlocTexte("Le fichier n'existe pas ou n'est pas au bon endroit.", 
                                       police2, self.taillePolice, [self.fenetre.largeurContenu, ''])])
        elif mode == 2:
            self.fenetre.ajouteContenu(['cad', BlocTexte("Ce fichier n'est pas prit en compte", 
                                       police2, self.taillePolice, [self.fenetre.largeurContenu, ''])])

    def ouvre(self) -> None:
        """Permet d'afficher l'interpréteur.
        """
        self.fenetre.ouvre()

    def ferme(self) -> None:
        """Permet de masquer l'interpréteur.
        """
        self.fenetre.ferme()