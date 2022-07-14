from systeme.FondMarin import *
from objets.BateauJoueur import *

class Tiroir:
    def __init__(self, createur: object) -> None:
        """Crée le tiroir à bateaux.

        Args:
            createur (object): Elément qui crée le tiroir (normalment l'editeur).
        """
        self.createur = createur
        self.liste = []
        self.positions = [(1, [50]), (2, [30, 70]), (3, [20, 50, 80]), (4, [15, 37, 63, 85]), 
                          (5, [10, 30, 50, 70, 90])]
        self.soulevement = []
        # Graphique
        self.tCase = 1.45*tailleCase
        self.originex = -40
        self.largeur = int(xf*0.16)
        self.lumCadre = [0, 5]
        self.hauteur_rect = int(tailleCase*1.2)
        # Images
        deco1 = load_image('images/decors/coraux1.png')
        ratio = self.largeur/deco1.width
        image_resize(deco1, int(deco1.width*ratio), int(deco1.height*ratio))
        self.decos = [load_texture_from_image(deco1)]
        image_flip_vertical(deco1)
        self.decos.append(load_texture_from_image(deco1))
        deco2 = load_image('images/decors/poissons.png')
        ratio = self.hauteur_rect/deco2.height
        image_resize(deco2, int(deco2.width*ratio), int(deco2.height*ratio))
        self.decos.append(load_texture_from_image(deco2))

    def dessine(self, y: int) -> None:
        """Dessine le tiroir et les bateaux qui sont dedans.

        Args:
            y (int): Position cible du centre du tiroir en hauteur.
        """
        if len(self.liste) > 0:
            tailley = int(self.tCase*len(self.liste))
            originey = y-int(self.tCase/2*len(self.liste))
            draw_rectangle_rounded((self.originex, originey, self.largeur+self.originex*-1, tailley), 
                                   0.2, 30, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[0], self.largeur-self.decos[0].width, 
                         originey+tailley-self.decos[0].height, [255, 255, 255, self.lumCadre[0]])
            draw_texture(self.decos[1], self.largeur-self.decos[1].width, originey, 
                         [255, 255, 255, self.lumCadre[0]])
            draw_rectangle_rounded_lines((self.originex, originey, self.largeur+self.originex*-1, tailley), 
                                         0.2, 30, 4, [255, 255, 255, self.lumCadre[1]])
            self.apparition()
            i = 0
            while i < len(self.liste):
                xbat = 0
                contact = self.getContactBateau(i)
                if not contact[1]:
                    ybat = int(tailley*(self.positions[len(self.liste)-1][1][i]/100)+originey)
                    if contact[0]:
                        xbat = int(xf*0.01)
                        self.soulevement[i][0] = True
                        self.dessineNom(self.liste[i], xbat, ybat)
                    else:
                        self.soulevement[i][0] = False
                        if self.liste[i].images[0].width >= (self.largeur)*0.9:
                            xbat = int((self.largeur)*0.9-self.liste[i].images[0].width)
                    if self.soulevement[i][2] > 0:
                        self.dessineNom(self.liste[i], xbat, ybat)
                    self.liste[i].dessine(self.soulevement[i][1], ybat-int(self.liste[i].images[0].height/2))
                    # Animation des bateaux
                    self.bougeBat(i, xbat)
                i = i + 1

    def dessineNom(self, bateau: BateauJoueur, x: int, y: int) -> None:
        """Dessine l'encadré du nom et de la taille des bateaux.

        Args:
            bateau (BateauJoueur): Bateau dont on doit afficher le nom et la taille.
            x (int): position cible de l'origine x voulu pour la bannière.
            y (int): position cible de l'origine y voulu pour la bannière.
        """
        tt1 = measure_text_ex(police2, bateau.nom, int(self.hauteur_rect*0.37), 0)
        tt2 = measure_text_ex(police2, f"{bateau.taille} cases", int(self.hauteur_rect*0.27), 0)
        max = tt1.x
        if tt2.x > max:
            max = tt2.x
        longueur = int(x+bateau.images[0].width+max+self.hauteur_rect/3)
        pourcentage = self.soulevement[self.liste.index(bateau)][2]
        draw_rectangle(0, y-int(self.hauteur_rect/2), int(longueur*pourcentage), self.hauteur_rect, 
                       [0, 12, 72, 155])
        draw_texture(self.decos[2], 0, y-int(self.decos[2].height/2), [255, 255, 255, int(255*pourcentage)])
        draw_text_pro(police2, bateau.nom, (int(x+bateau.images[0].width+self.hauteur_rect/6), y-tt1.y), 
                      (0, 0), 0, int(self.hauteur_rect*0.37), 0, [255, 255, 255, int(255*pourcentage)])
        draw_text_pro(police2, f"{bateau.taille} cases", 
                      (int(x+bateau.images[0].width+self.hauteur_rect/6), y), (0, 0), 0, 
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

    def setListe(self, liste: list) -> None:
        """Permet de changer la liste de bateaux exploitée par le tiroir.

        Args:
            liste (list): Nouvelle liste pour le tiroir.
        """
        self.liste = liste[:]
        self.lumCadre = [0, 5]
        for i in range(len(self.liste)):
            self.soulevement.append([False, 0-self.liste[i].images[0].width, 0])

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
            self.createur.ordreBateaux()

    def ajValListe(self, valeur: BateauJoueur) -> None:
        """Ajoute un bateau à la liste des bateaux exploitées.

        Args:
            valeur (BateauJoueur): Bateau à ajouter à la liste.
        """
        self.liste.append(valeur)
        self.soulevement.append([False, 0-valeur.images[0].width, 0])

    def getContactBateau(self, indice: int) -> list:
        """Vérifie si le curseur est sur le bateau.

        Returns:
            list: 1. True si le curseur est sur le bateau, False dans le cas contraire. 2. Valeurs spécifiques.
        """
        bateau = self.liste[indice]
        rep = False
        onse = False
        x = get_mouse_x()
        y = get_mouse_y()
        if y >= bateau.coord[1] and y <= bateau.coord[1]+bateau.coord[3]:
            if (not self.soulevement[indice][0] and x <= int(self.largeur)) or (self.soulevement[indice][0] and x <= int(bateau.coord[0]+bateau.coord[2])):
                rep = True
                onse = self.checkSelect(bateau)
                if onse:
                    rep = False
        return [rep, onse]

    def checkSelect(self, bateau: BateauJoueur) -> bool:
        """Vérifie si la bateau est sélectionné par l'utilisateau.

        Args:
            bateau (BateauJoueur): Bateau à tester.

        Returns:
            bool: True si le bateau est sélectionné, False sinon.
        """
        rep = False
        if is_mouse_button_pressed(0):
            parasite = self.checkBateauVolant()
            bateau.defil = True
            self.createur.attente = 50
            self.createur.bateaux.append(bateau)
            if parasite >= 0:
                self.createur.bateaux[parasite].pos = False
                self.createur.bateaux[parasite].immobile()
                self.liste[self.liste.index(bateau)] = self.createur.bateaux[parasite]
                del self.createur.bateaux[parasite]
                self.createur.ordreBateaux()
            else:
                self.supValListe(self.liste.index(bateau))
            rep = True
        return rep

    def checkBateauVolant(self) -> int:
        """Vérifie si il n'y a pas de bateau en déplacement dans ceux qui ne sont pas dans le tiroir.

        Returns:
            int: -1 s'il n'y en a pas ou l'indice du bateau s'il y en a un.
        """
        rep = -1
        i = 0
        while i < len(self.createur.bateaux) and rep == -1:
            if self.createur.bateaux[i].defil:
                rep = i
            else:
                i = i + 1
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