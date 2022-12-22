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
        self.calcul = False
        self.limites = limites
        self.construction(limites)
    
    def dessine(self, position: list, couleur:list=WHITE, alignement:str='c') -> None:
        """Dessine le texte du bloc à l'écran.

        Args:
            position (list): Position voulue pour le bloc sous forme [[x, y], indication].
            couleur (list, optional): Couleur du texte. Defaults to WHITE.
            alignement (str, optional): Alignement du texte dans l'encadré. Defaults to 'c'.
        """
        if not self.calcul:
            self.construction(self.limites)
        if type(alignement) != str or alignement.lower() not in ['c', 'g', 'd']:
            alignement = 'c'
        else:
            alignement = alignement.lower()
        centre = self.trouveOrigine(position[0], position[1])
        tt = measure_text_ex(self.police, self.texte, self.taille, 0)
        decomposition = self.texte.split("\n")
        valDep = 0.37
        if len(decomposition) > 1:
            valDep = 0.41
        axeY = valDep + 0.054*(len(decomposition)-1)
        if alignement == 'c':
            draw_text_pro(self.police, self.texte, (centre[0]-int(tt.x/2), centre[1]-int(tt.y*axeY)), 
                          (0, 0), 0, self.taille, 0, couleur)
        elif alignement == 'g':
            draw_text_pro(self.police, self.texte, 
                          (centre[0]-int(self.tCadre[0]/2), centre[1]-int(tt.y*axeY)), 
                          (0, 0), 0, self.taille, 0, couleur)
        else:
            draw_text_pro(self.police, self.texte, 
                          (centre[0]+int(self.tCadre[0]/2-tt.x), centre[1]-int(tt.y*axeY)), 
                          (0, 0), 0, self.taille, 0, couleur)

    def construction(self, limites: list) -> None:
        if len(limites) == 2:
            if type(limites[0]) == int and type(limites[1]) == int:
                self.tCadre = limites
                self.adapte()
            elif type(limites[0]) == int and type(limites[1]) == str:
                self.tCadre = [limites[0], yf]
                self.adapte()
                tt = measure_text_ex(self.police, self.texte, self.taille, 0)
                self.tCadre = [limites[0], tt.y]
            elif type(limites[0]) == str and type(limites[1]) == int:
                tt = measure_text_ex(self.police, self.texte, self.taille, 0)
                self.tCadre = [tt.x, limites[1]]
            else:
                tt = measure_text_ex(self.police, self.texte, self.taille, 0)
                self.tCadre = [tt.x, tt.y]
        else:
            tt = measure_text_ex(self.police, self.texte, self.taille, 0)
            self.tCadre = [tt.x, tt.y]
        self.calcul = True

    def trouveOrigine(self, position: list, indication: str) -> tuple:
        """Regarde les indications fournis pour trouver la bonne origine pour le bloc.

        Args:
            position (list): Positions x et y fournies par l'utilisateur.
            indication (str): Indicaton fournie par l'utilisateur.

        Returns:
            tuple: Coordonnées x et y de l'origine du bloc.
        """
        indic = indication.lower()
        if indic == 'no':
            rep = (position[0]+self.tCadre[0]/2, position[1]+self.tCadre[1]/2)
        elif indic == 'ne':
            rep = (position[0]-self.tCadre[0]/2, position[1]+self.tCadre[1]/2)
        elif indic == 'se':
            rep = (position[0]-self.tCadre[0]/2, position[1]-self.tCadre[1]/2)
        elif indic == 'so':
            rep = (position[0]+self.tCadre[0]/2, position[1]-self.tCadre[1]/2)
        else:
            rep = (position[0], position[1])
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
                chaine = texte[i] + " "
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

    def getDims(self) -> list:
        """Renvoi les dimensions du bloc de texte.

        Returns:
            list: Largeur puis hauteur du bloc de texte.
        """
        return self.tCadre

    def getNbLignes(self) -> int:
        """Retourne le nombre de ligne du texte.
        """
        texte = self.texte.split("\n")
        return len(texte)

    def setPolice(self, police: Font) -> None:
        """Modifie la police utilisée.

        Args:
            police (Font): Nouvelle police à utiliser.
        """
        self.police = police
        self.calcul = False