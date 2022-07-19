from systeme.FondMarin import *

class BlocTexte:
    def __init__(self, texte: str, police: object, taille: int, limites:list=[]) -> None:
        """Crée un bloc de texte.

        Args:
            texte (str): Le texte à mettre dans le bloc.
            police (object): La police utilisée par le bloc.
            taille (int): La taille souhaitée pour la police.
            limites (list, optional): Eventuelles dimensions maximales souhatées pour le bloc. Defaults to [].
        """
        self.texte = texte
        self.police = police
        self.taille = taille
        if len(limites) == 2:
            self.tCadre = limites
            self.adapte()
        else:
            tt = measure_text_ex(self.police, self.texte, self.taille, 0)
            self.tCadre = [tt.x, tt.y]
    
    def dessine(self, position: list, couleur:list=WHITE) -> None:
        """Dessine le texte du bloc à l'écran.

        Args:
            position (list): Position voulue pour le bloc sous forme [[x, y], indication].
            couleur (list, optional): Couleur du texte. Defaults to WHITE.
        """
        centre = self.trouveOrigine(position[0], position[1])
        tt = measure_text_ex(self.police, self.texte, self.taille, 0)
        decomposition = self.texte.split("\n")
        axeY = 0.37 + 0.054*(len(decomposition)-1)
        draw_text_pro(self.police, self.texte, (centre[0]-int(tt.x/2), centre[1]-int(tt.y*axeY)), 
                      (0, 0), 0, self.taille, 0, couleur)

    def trouveOrigine(self, position: tuple, indication: str) -> tuple:
        """Regarde les indications fournis pour trouver la bonne origine pour le bloc.

        Args:
            position (tuple): Positions x et y fournies par l'utilisateur.
            indication (str): Indicaton fournie par l'utilisateur.

        Returns:
            tuple: Coordonnées x et y de l'origine du bloc.
        """
        rep = position
        indic = indication.lower()
        if indic == 'no':
            rep = (position[0]+self.tCadre[0]/2, position[1]+self.tCadre[1]/2)
        elif indic == 'ne':
            rep = (position[0]-self.tCadre[0]/2, position[1]+self.tCadre[1]/2)
        elif indic == 'se':
            rep = (position[0]-self.tCadre[0]/2, position[1]-self.tCadre[1]/2)
        elif indic == 'so':
            rep = (position[0]+self.tCadre[0]/2, position[1]-self.tCadre[1]/2)
        return rep

    def adapte(self) -> None:
        """Adapte le texte à la taille du bloc si celui-ci n'est pas redimensionnable.
        """
        texte = self.texte.split(" ")
        grosseChaine = ""
        chaine = ""
        i = 0
        while i < len(texte):
            tt = measure_text_ex(self.police, texte[i], self.taille, 0)
            ttt = measure_text_ex(self.police, chaine+texte[i], self.taille, 0)
            if tt.x >= self.tCadre[0]:
                chaine += texte[i][0:int(len(texte[i])/2)] + "-\n"
                grosseChaine += chaine
                chaine = texte[i][int(len(texte[i])/2):int(len(texte[i])-1)] + " "
            elif ttt.x >= self.tCadre[0]:
                grosseChaine = grosseChaine + chaine + "\n"
                chaine = ""
            else:
                chaine = chaine + texte[i] + " "
            tgc = measure_text_ex(self.police, grosseChaine, self.taille, 0)
            if tgc.x >= self.tCadre[0] or tgc.y >= self.tCadre[1]:
                i = 0
                self.taille = self.taille - 1
                texte = self.texte.split(" ")
                grosseChaine = ""
                chaine = ""
            else:
                i = i + 1
        grosseChaine += chaine
        self.texte = grosseChaine