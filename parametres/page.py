from systeme.FondMarin import *
from interpreteur.interpreteurMd import InterpreteurMd
from ui.blocTexte import BlocTexte

class Page(InterpreteurMd):
    def __init__(self, fichier: str, dims: tuple) -> None:
        super().__init__(fichier, dims)