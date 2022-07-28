from systeme.FondMarin import *
from interpreteur.article import Article
from interpreteur.fenetre import Fenetre
from ui.blocTexte import BlocTexte

class InterpreteurMd:
    def __init__(self, fichier: str) -> None:
        self.fichier = fichier
        self.decode = False
        self.position = 'gen'
        # Fenetre
        self.fenetre = Fenetre()
        self.element = None

    def dessine(self) -> None:
        if not self.decode:
            self.decodeur()
        self.fenetre.dessine()

    def decodeur(self) -> None:
        if file_exists(self.fichier):
            fic = load_file_text(self.fichier)
            fil = fic.split("\n")
            while len(fil) > 0:
                if self.position == 'gen':
                    if len(fil[0]) > 0 and fil[0][0] == "#":
                        ligne = fil[0].split(" ")
                        del ligne[0]
                        self.fenetre.setTitre(" ".join(ligne))
                    elif fil[0] == "_fen//":
                        self.position = 'fen'
                    elif fil[0] == "_art//":
                        self.element = Article()
                        self.element.redim(int(self.fenetre.largeur*0.95), self.element.hauteur)
                        self.position = 'art'
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
            self.decode = True

    def ouvre(self) -> None:
        self.fenetre.ouvre()

    def ferme(self) -> None:
        self.fenetre.ferme()