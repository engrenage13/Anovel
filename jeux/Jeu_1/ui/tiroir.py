from systeme.FondMarin import *
from jeux.Jeu_1.objets.Bateau import Bateau
from museeNoyee import corail1, corail2, poisson, coeur, fleche, marin
from jeux.Jeu_1.ui.attribut import Attribut

class Tiroir:
    def __init__(self, bateaux: list[Bateau]) -> None:
        """Crée le tiroir à bateaux.

        Args:
            bateaux (list[Bateau]): les bateaux à afficher.
        """
        self.liste = []
        self.soulevement = []
        # Graphique
        self.tCase = 1.35*bateaux[0].image.height
        self.originex = -40
        self.originey = int(yf/2)
        self.largeur = int(xf*0.11)
        self.lumCadre = [0, 5]
        self.hauteur_rect = int(bateaux[0].image.height*1.1)
        self.allume = True
        self.play = True
        # Images
        self.decos = [corail1, corail2, poisson]
        # positionnement
        self.setListe(bateaux)
        # étiquettes
        self.etiCoeur = Attribut(0, coeur)
        self.etiMarin = Attribut(0, marin)
        self.etiFleche = Attribut(0, fleche)

    def dessine(self) -> None:
        """Dessine le tiroir et les bateaux qui sont dedans.
        """
        if len(self.liste) > 0:
            tailley = int(self.tCase*len(self.liste))
            y = int(self.originey-(self.tCase/2*len(self.liste)))
            draw_rectangle_rounded((self.originex, y, self.largeur+self.originex*-1, tailley), 
                                   0.2, 30, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[0], int(self.largeur-self.decos[0].width*0.9), 
                         y+tailley-self.decos[0].height, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[1], int(self.largeur-self.decos[1].width*0.9), y, 
                         [255, 255, 255, self.lumCadre[0]])
            draw_rectangle_rounded_lines((self.originex, y, self.largeur+self.originex*-1, tailley), 
                                         0.2, 30, 3, [255, 255, 255, self.lumCadre[1]])
            if self.allume:
                self.apparition()
            else:
                self.disparition()
            i = 0
            while i < len(self.liste):
                if self.allume:
                    xbat = int(self.liste[i].image.width/3)
                    if self.getContactBateau(i):
                        xbat = int(self.liste[i].image.width/2)
                        self.soulevement[i][0] = True
                    elif self.soulevement[i][0]:
                        self.soulevement[i][0] = False
                else:
                    xbat = -int(self.liste[i].image.width*0.6)
                if self.play:
                    self.dessineNom(self.liste[i])
                self.liste[i].dessine()
                # Animation des bateaux
                if self.play:
                    self.bougeBat(i, xbat)
                i = i + 1

    def dessineNom(self, bateau: Bateau) -> None:
        """Dessine l'encadré du nom des bateaux.

        Args:
            bateau (Bateau): Bateau où il y a le curseur.
        """
        x = 0
        y = int(bateau.pos[1])
        self.etiCoeur.setValeur(bateau.pvi)
        self.etiFleche.setValeur(bateau.pmi)
        self.etiMarin.setValeur(bateau.marins)
        tt1 = measure_text_ex(police1, bateau.nom.upper(), int(self.hauteur_rect*0.37), 0)
        ttiret = measure_text_ex(police2i, " - ", int(self.hauteur_rect*0.27), 0)
        tt2 = self.etiCoeur.getDims()[0]+self.etiFleche.getDims()[0]+self.etiMarin.getDims()[0]+ttiret.x*2
        max = tt1.x
        if tt2 > max:
            max = tt2
        longueur = int(x+bateau.image.width+max+self.hauteur_rect/3)
        pourcentage = self.soulevement[self.liste.index(bateau)][2]
        draw_rectangle(0, y-int(self.hauteur_rect/2), int(longueur*pourcentage), self.hauteur_rect, 
                       [0, 12, 72, 155])
        draw_texture(self.decos[2], 0, y-int(self.decos[2].height/2), [255, 255, 255, int(255*pourcentage)])
        draw_text_pro(police1, bateau.nom.upper(), (int(x+bateau.image.width+self.hauteur_rect/6), y-tt1.y), 
                      (0, 0), 0, int(self.hauteur_rect*0.37), 0, [255, 255, 255, int(255*pourcentage)])
        xeti = x+bateau.image.width+self.hauteur_rect/6
        self.etiCoeur.pos = (xeti, y)
        self.etiCoeur.dessine(int(255*pourcentage))
        xeti += self.etiCoeur.getDims()[0] + ttiret.x
        self.etiMarin.pos = (xeti, y)
        self.etiMarin.dessine(int(255*pourcentage))
        xeti += self.etiMarin.getDims()[0] + ttiret.x
        self.etiFleche.pos = (xeti, y)
        self.etiFleche.dessine(int(255*pourcentage))
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
            # Réorienter correctement les bateaux
            while self.liste[i].direction != 0:
                if self.liste[i].direction == 1:
                    self.liste[i].gauche()
                else:
                    self.liste[i].droite()
            # /
            x = self.soulevement[i][1]
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
            self.soulevement.append([False, -int(self.liste[i].image.width*0.6), 0])
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
        self.soulevement.append([False, -int(valeur.image.width*0.6), 0])
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

    def checkSelect(self) -> int:
        """Vérifie si un bateau est sélectionné par l'utilisateur.

        Returns:
            int: l'indice du bateau sélectionné ou -1 s'il n'y en a pas.
        """
        rep = -1
        if self.play:
            if is_mouse_button_pressed(0):
                i = 0
                while i < len(self.liste) and rep < 0:
                    if self.getContactBateau(i):
                        rep = i
                    else:
                        i += 1
        return rep

    def apparition(self) -> None:
        """Gère l'apparition du tiroir.
        """
        if self.lumCadre[0] < 50:
            self.lumCadre[0] += 1
            self.lumCadre[1] += 5

    def disparition(self) -> None:
        """Gère la disparition du tiroir.
        """
        if self.lumCadre[0] > 0:
            self.lumCadre[0] -= 1
            self.lumCadre[1] -= 5

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
            self.liste[bateau].deplace(pas, 0)
        elif self.soulevement[bateau][1] > verif:
            pas = int((self.soulevement[bateau][1]-verif)/9)
            if pas < 1:
                pas = 1
            self.soulevement[bateau][1] -= pas
            self.liste[bateau].deplace(-pas, 0)

    def estApparu(self) -> bool:
        if self.lumCadre[0] >= 50:
            return True
        else:
            return False

    def __getitem__(self, key) -> Bateau:
        return self.liste[key]
    
    def __len__(self) -> int:
        return len(self.liste)