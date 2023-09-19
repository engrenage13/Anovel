from pyray import Font

class Apparence:
    def __init__(self, couleurs: list, police: Font, icone: int, afficheTexte: bool) -> None:
        if len(couleurs) == 0:
            couleurs = [(255, 255, 255, 150)]
        if len(couleurs) < 2:
            self.zoom = True
            self.couleur2 = False
        else:
            self.zoom = False
            self.couleur2 = couleurs[1]
        self.couleur1 = couleurs[0]
        self.police = police
        self.icone = icone
        self.texte = afficheTexte