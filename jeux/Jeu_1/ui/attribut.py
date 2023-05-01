from systeme.FondMarin import draw_texture, police2, yf, Texture
from ui.blocTexte import BlocTexte

class Attribut:
    def __init__(self, valeur: int, icone: Texture) -> None:
        self.pos = (0, 0)
        self.setValeur(valeur)
        self.icone = icone

    def dessine(self, transparence: int = 255) -> None:
        x = int(self.pos[0])
        self.valeur.dessine([[x, self.pos[1]], 'no'], [255, 255, 255, transparence])
        x += int(self.valeur.getDims()[0])
        draw_texture(self.icone, x, self.pos[1], [255, 255, 255, transparence])

    def setValeur(self, valeur: str|int) -> None:
        self.valeur = BlocTexte(str(valeur), police2, int(yf*0.035))

    def getDims(self) -> tuple[int]:
        return (self.valeur.getDims()[0]+self.icone.width, self.icone.height)