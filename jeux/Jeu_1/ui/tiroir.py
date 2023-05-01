from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from jeux.BN.collectionImage import corail1, corail2, poisson

class Tiroir:
    def __init__(self, bateaux: list[Bateau]) -> None:
        """Crée le tiroir à bateaux.

        Args:
            bateaux (list[Bateau]): les bateaux à afficher.
        """
        self.liste = []
        self.positions = [(1, [50]), (2, [30, 70]), (3, [20, 50, 80]), (4, [15, 37, 63, 85]), 
                          (5, [10, 30, 50, 70, 90])]
        self.soulevement = []
        # Graphique
        self.tCase = 1.35*bateaux[0].image.height
        self.originex = -40
        self.originey = int(yf/2)
        self.largeur = int(xf*0.12)
        self.lumCadre = [0, 5]
        self.hauteur_rect = int(bateaux[0].image.height*1.1)
        # Images
        self.decos = [corail1, corail2, poisson]
        # positionnement
        self.setListe(bateaux)

    def dessine(self) -> None:
        """Dessine le tiroir et les bateaux qui sont dedans.
        """
        if len(self.liste) > 0:
            tailley = int(self.tCase*len(self.liste))
            y = int(self.originey-(self.tCase/2*len(self.liste)))
            draw_rectangle_rounded((self.originex, y, self.largeur+self.originex*-1, tailley), 
                                   0.2, 30, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[0], self.largeur-self.decos[0].width, 
                         y+tailley-self.decos[0].height, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[1], self.largeur-self.decos[1].width, y, 
                         [255, 255, 255, self.lumCadre[0]])
            draw_rectangle_rounded_lines((self.originex, y, self.largeur+self.originex*-1, tailley), 
                                         0.2, 30, 3, [255, 255, 255, self.lumCadre[1]])
            self.apparition()
            i = 0
            while i < len(self.liste):
                xbat = 0
                if self.getContactBateau(i):
                    xbat = int(xf*0.01)
                    self.soulevement[i][0] = True
                    self.dessineNom(self.liste[i])
                self.liste[i].dessine()
                # Animation des bateaux
                self.bougeBat(i, xbat)
                i = i + 1

    def dessineNom(self, bateau: Bateau) -> None:
        """Dessine l'encadré du nom et de la taille des bateaux.

        Args:
            bateau (Bateau): Bateau dont on doit afficher le nom et la taille.
            x (int): position cible de l'origine x voulu pour la bannière.
            y (int): position cible de l'origine y voulu pour la bannière.
        """
        x = 0
        y = int(bateau.pos[1])
        chaine = f"{bateau.vie} VIES"
        tt1 = measure_text_ex(police1, bateau.nom.upper(), int(self.hauteur_rect*0.37), 0)
        tt2 = measure_text_ex(police2i, chaine, int(self.hauteur_rect*0.27), 0)
        max = tt1.x
        if tt2.x > max:
            max = tt2.x
        longueur = int(x+bateau.image.width+max+self.hauteur_rect/3)
        pourcentage = self.soulevement[self.liste.index(bateau)][2]
        draw_rectangle(0, y-int(self.hauteur_rect/2), int(longueur*pourcentage), self.hauteur_rect, 
                       [0, 12, 72, 155])
        draw_texture(self.decos[2], 0, y-int(self.decos[2].height/2), [255, 255, 255, int(255*pourcentage)])
        draw_text_pro(police1, bateau.nom.upper(), (int(x+bateau.image.width+self.hauteur_rect/6), y-tt1.y), 
                      (0, 0), 0, int(self.hauteur_rect*0.37), 0, [255, 255, 255, int(255*pourcentage)])
        draw_text_pro(police2i, chaine, (int(x+bateau.image.width+self.hauteur_rect/6), y), (0, 0), 0, 
                      int(self.hauteur_rect*0.27), 0, [102, 191, 255, int(255*pourcentage)])
        # animations
        if self.soulevement[self.liste.index(bateau)][0] and pourcentage < 1:
            addit = 0.1
            if 1 - pourcentage < addit:
                addit = 1 - pourcentage
            self.soulevement[self.liste.index(bateau)][2] += addit
        elif not self.soulevement[self.liste.index(bateau)][0] and pourcentage > 0:
            addit = 0.1
            if pourcentage < addit:
                addit = pourcentage
            self.soulevement[self.liste.index(bateau)][2] -= addit

    def positioneBateaux(self) -> None:
        tailley = int(self.tCase*len(self.liste))
        segment = 100/(len(self.liste)+1)/100
        y = int(self.originey-tailley/2+tailley*segment)
        for i in range(len(self.liste)):
            x = int(self.liste[i].image.width/2)
            self.liste[i].setPos(x, y)
            y += int(tailley*segment)

    def setListe(self, liste: list[Bateau]) -> None:
        """Permet de changer la liste de bateaux exploitée par le tiroir.

        Args:
            liste (list[Bateau]): Nouvelle liste pour le tiroir.
        """
        self.liste = liste[:]
        self.lumCadre = [0, 5]
        for i in range(len(self.liste)):
            self.soulevement.append([False, -self.liste[i].image.width, 0])
        self.positioneBateaux()

    def supValListe(self, indice: int) -> None:
        """Supprime un bateau de la liste de bateaux exploitée.

        Args:
            indice (int): Indice du bateau à supprimer.
        """
        if indice >= 0 and indice < len(self.liste):
            del self.liste[indice]
            del self.soulevement[indice]
            if len(self.liste) == 0:
                self.lumCadre = [0, 5]
        self.positioneBateaux()

    def ajValListe(self, valeur: Bateau) -> None:
        """Ajoute un bateau à la liste des bateaux exploitées.

        Args:
            valeur (Bateau): Bateau à ajouter à la liste.
        """
        self.liste.append(valeur)
        self.soulevement.append([False, 0-valeur.image.width, 0])
        self.positioneBateaux()

    def getContactBateau(self, indice: int) -> bool:
        """Vérifie si le curseur est sur le bateau.

        Args:
            indice (int): L'indice du bateau testé.

        Returns:
            bool: True si le curseur est sur le bateau.
        """
        bateau = self.liste[indice]
        return bateau.getContact()

    def checkSelect(self, bateau: Bateau) -> bool:
        """Vérifie si la bateau est sélectionné par l'utilisateur.

        Args:
            bateau (Bateau): Bateau à tester.

        Returns:
            bool: True si le bateau est sélectionné, False sinon.
        """
        rep = False
        if is_mouse_button_pressed(0):
            self.supValListe(self.liste.index(bateau))
            rep = True
        return rep

    def apparition(self) -> None:
        """Gère l'apparition du tiroir lors de l'apparation de l'éditeur.
        """
        if self.lumCadre[0] < 50:
            self.lumCadre[0] += 1
            self.lumCadre[1] += 5

    def bougeBat(self, bateau: int, verif: int) -> None:
        """Gère le mouvement de va et viens d'un bateau dans le tiroir.

        Args:
            bateau (int): Bateau à déplacer.
            verif (int): Condition de verification.
        """
        if self.soulevement[bateau][1] < verif:
            pas = int((verif-self.soulevement[bateau][1])/9)
            if pas < 1:
                pas = 1
            self.soulevement[bateau][1] += pas
        elif self.soulevement[bateau][1] > verif:
            pas = int((self.soulevement[bateau][1]-verif)/9)
            if pas < 1:
                pas = 1
            self.soulevement[bateau][1] -= pas