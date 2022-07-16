from types import NoneType
from systeme.FondMarin import *
from ui.notif import Notification

class Bouton:
    def __init__(self, fonctions: list, couleurs: list, texte:str=None, icone:str=None) -> None:
        """Crée un bouton.

        Args:
            fonctions (list): Fonctions qu'appel le bouton quand il est utilisé.
            couleurs (list): Liste des couleurs utilisés pour le bouton.
            texte (str, optional): Ecritaut sur le bouton.. Defaults to None.
            icone (str, optional): Icône sur le bouton. Defaults to None.
        """
        self.ajustement = False
        self.texte = texte
        self.icone = icone
        self.couleur = couleurs
        self.fonction = fonctions[0]
        if len(fonctions) > 1 and fonctions[1] != '':
            self.verifFonction = fonctions[1]
        else:
            self.verifFonction = self.verification
        self.lmax = int(tlatba*0.7)
        self.hmin = int(yf*0.075)
        self.lmin = self.hmin*2
        self.notif = Notification("Option indisbonible", "Ce bouton est désactivé")
        self.notif.setPosition(1)
        self.etatNotif = False
        # Affichage
        #bouton = load_image('images/ui/bouton.png')
        #image_resize(bouton, int(bouton.width*0.13), int(bouton.height*0.13))
        #self.fond = load_texture_from_image(bouton)

    def dessine(self, coord: tuple, ajustement: bool) -> None:
        """Dessine le bouton à l'écran aux coordonnées passées en paramètre.

        Args:
            coord (tuple): Coordonnées du centre du bouton.
            ajustement (bool): Si True, le bouton sera ajusté à la taille du texte et/ou l'icône qui le composent.
        """
        dims = [self.lmax, self.hmin]
        if ajustement:
            if type(self.texte) is not NoneType:
                if not self.ajustement:
                    self.adapte()
                dims = self.mesureTaille()
        self.coords = [coord[0]-int(dims[0]/2), coord[1]-int(dims[1]/2), coord[0]+int(dims[0]/2), 
                       coord[1]+int(dims[1]/2)]
        couleur = self.couleur[0]
        if self.getContact():
            couleur = self.couleur[1]
        #draw_texture(self.fond, self.coords[0]-2, self.coords[1]-2, WHITE)
        draw_rectangle_rounded((self.coords[0]+2, self.coords[1]+2, dims[0], dims[1]), 0.2, 30, BLACK)
        draw_rectangle_rounded((self.coords[0], self.coords[1], dims[0], dims[1]), 0.2, 30, couleur)
        if type(self.texte) is not NoneType:
            tt = measure_text_ex(police1, self.texte, int(self.hmin*0.45), 0)
            draw_text_pro(police1, self.texte, (coord[0]-int(tt.x/2), coord[1]-int(tt.y*0.39)), 
                          (0, 0), 0, int(self.hmin*0.45), 0, self.couleur[2])
        if self.etatNotif:
            self.notif.dessine()
            if self.notif.getDisparition():
                self.etatNotif = False
        self.execute()

    def mesureTaille(self) -> list:
        dims = [self.lmax, self.hmin]
        decomposition = self.texte.split("\n")
        dims[1] = self.hmin+int(self.hmin*0.5*(len(decomposition)-1))
        return dims

    def adapte(self) -> None:
        if self.texte is not NoneType:
            texte = self.texte.split(" ")
        grosseChaine = ""
        chaine = ""
        for i in range(len(texte)):
            tt = measure_text_ex(police1, texte[i], int(self.hmin*0.45), 0)
            ttt = measure_text_ex(police1, chaine+texte[i], int(self.hmin*0.45), 0)
            if tt.x >= self.lmax - 40:
                chaine += texte[i][0:int(len(texte[i])/2)] + "-\n"
                grosseChaine += chaine
                chaine = texte[i][int(len(texte[i])/2):int(len(texte[i])-1)] + " "
            elif ttt.x >= self.lmax - 40:
                grosseChaine = grosseChaine + chaine + "\n"
                chaine = ""
            else:
                chaine = chaine + texte[i] + " "
        grosseChaine += chaine
        self.texte = grosseChaine
        self.ajustement = True

    def execute(self) -> None:
        """Gère ce qui se passe quand on appuie sur le bouton.
        """
        if is_mouse_button_pressed(0):
            if self.getContact():
                if self.verifFonction():
                    self.fonction()
                else:
                    self.etatNotif = True

    def verification(self) -> bool:
        """Fonction par défaut pour la vérification d'instruction spéciale.

        Returns:
            bool: True.
        """
        return True

    def getTexte(self) -> str:
        """Retourne le texte écrit sur le bouton du bouton.

        Returns:
            str: Texte du bouton.
        """
        return self.texte

    def setTexte(self, texte: str) -> None:
        """Permet de modifier le texte du bouton.

        Args:
            texte (str): Modifie le texte affiché sur le bouton.
        """
        self.texte = texte

    def setTexteNotif(self, titre: str="", texte: str="") -> None:
        """Permet de modifier le texte de la notification liée.

        Args:
            titre (str): Modifie le titre de la notif.
            texte (str): Modifie le message de la notif.
        """
        if titre != "":
            self.notif.modifTitre(str(titre))
        if texte != "":
            self.notif.modifTexte(str(texte))

    def getCouleurs(self) -> list:
        """Retourne les couleurs utilisés par le bouton.

        Returns:
            list: couleur de base du fond, couleur de surbrillement et couleur du texte.
        """
        return self.couleur

    def setCouleurs(self, couleurs: list) -> None:
        """Permet de modifier les couleurs utilisées par le bouton.

        Args:
            couleurs (list): Première pour le fond du bouton, seconde pour surbrillement et 
            troisième pour le texte.
        """
        self.couleur = couleurs

    def getContact(self) -> bool:
        """Vérifie si le curseur est sur le bouton.

        Returns:
            bool: True si le curseur est sur le bouton, False dans le cas contraire.
        """
        rep = False
        x = get_mouse_x()
        y = get_mouse_y()
        if x >= self.coords[0] and x <= self.coords[2]:
            if y >= self.coords[1] and y <= self.coords[3]:
                rep = True
        return rep