from systeme.FondMarin import *
from interpreteur.article import Article

class Categorie:
    def __init__(self) -> None:
        self.titre = None
        self.contenu = []
        self.editArticle = False

    def decodeur(self, ligne: str) -> None:
        rep = False
        if not self.editArticle:
            if len(ligne) > 0 and ligne[0] == "#":
                li = ligne.split(" ")
                del li[0]
                self.setTitre(" ".join(li))
            elif ligne == "//cat_":
                rep = True
            elif ligne == "_art//":
                self.ajouteArticle(Article())
                self.editArticle = True
        else:
            rep = self.contenu[len(self.contenu)-1].decodeur(ligne)
            if rep:
                self.editArticle = False
        return rep

    def setTitre(self, titre: str) -> None:
        self.titre = titre

    def ajouteArticle(self, article: Article) -> None:
        self.contenu.append(article)