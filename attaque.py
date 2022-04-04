from FondMarin import *
from objets.Bateau import *
from finPartie import Fin
from objets.Joueur import Joueur

class Attaque:
    def __init__(self, joueur1: object, joueur2: object) -> None:
        self.j1 = joueur1
        self.j2 = joueur2
        self.joueurs = [joueur1, joueur2]
        self.listeBateaux1 = [False]*5
        self.listeBateaux2 = [False]*5
        self.tour = 0
        self.incrementTour()
        self.connect()
        self.affStats(0)
        c = fond.coords(self.j1.cTire[0][0])
        self.attaque(self.j1, c[1])

    def incrementTour(self) -> None:
        """Incrémente le compteur de tour
        """
        self.tour = self.tour + 1
        fond.itemconfigure('tour', text=f"Tour {self.tour}")

    def affStats(self, indice: int) -> None:
        """Affiche les statistiques du joueurs de l'indice pssé en paramètre.

        Args:
            indice (int): Indice du joueur voulu par rapport à `self.joueur`.
        """
        fond.delete('stats')
        l = ["Nb. Cases Touchées", "Touché", "Raté"]
        lv = self.joueurs[indice].getStats()
        y = yf*0.1
        for i in range(len(l)):
            if type(lv[i]) != list:
                t = f"{l[i]} : {lv[i]}"
            else:
                t = f"{l[i]} : {lv[i][0]} ({lv[i][1]}%)"
            x = xf-int(yf*0.01)*(len(t)/2+2)
            fond.create_text(x, y, text=t, font=Lili1, fill=blanc, tags=('stats'))
            y = y + yf*0.04

    def localiseCurseur(self, plateau: list) -> str:
        """Regarde la position du curseur sur le plateau et renvoie le code de la case coresspondante.

        Args:
            plateau (list): Le plateau où se situe le curseur.

        Returns:
            str: Le code de la case sur laquelle se trouve le curseur.
        """
        a = fond.winfo_pointerxy()
        b = False
        i = 0
        while i < len(plateau) and not b:
            j = 0
            while j < len(plateau[i]) and not b:
                c = fond.coords(plateau[i][j])
                if a[0] >= c[0] and a[0] <= c[2] and a[1] >= c[1] and a[1] <= c[3]:
                    b = True
                else:
                    j = j + 1
            if not b:
                i = i + 1
        if b:
            sortie = plateau[i][j]
        else:
            sortie = None
        return sortie

    def dessineViseur(self, coo: tuple, case: str) -> None:
        """Dessine le curseur aux coordonnées passés en paramètres.

        Args:
            coo (tuple): Là où apparaitra le curseur (les coordonnées de la case)
            case (str): Le code de la case (qui contient son nom)
        """
        b = coo
        fond.create_rectangle(b[0], b[1], b[2], b[3], fill='', outline='white', width=4, tag='pointeur')
        fond.create_oval(b[0]+(b[2]-b[0])*0.2, b[1]+(b[3]-b[1])*0.2, b[2]-(b[2]-b[0])*0.2, b[3]-(b[3]-b[1])*0.2, 
                        fill='', outline=grisClair, width=3, tag='pointeur')
        if self.getEtatCase(case):
            case = case[0:len(case)-2]
            col = blanc
        else:
            case = "X"
            col = orange
        fond.create_line(b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])*0.1, b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])*0.35, 
                        width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[2]-(b[2]-b[0])*0.1, b[1]+(b[3]-b[1])/2, b[2]-(b[2]-b[0])*0.35, b[1]+(b[3]-b[1])/2, 
                        width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[0]+(b[2]-b[0])/2, b[3]-(b[3]-b[1])*0.1, b[0]+(b[2]-b[0])/2, b[3]-(b[3]-b[1])*0.35, 
                        width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[0]+(b[2]-b[0])*0.1, b[1]+(b[3]-b[1])/2, b[0]+(b[2]-b[0])*0.35, b[1]+(b[3]-b[1])/2, 
                        width=2, fill=grisClair, tag='pointeur')
        fond.create_text(b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])/2, text=case, font=Lili1, fill=col, 
                        tags=('pointeur', 'affiTgVis'))

    def attaque(self, joueur: object, position: float) -> None:
        """Reboucle tant que le joueur n'a pas attaqué.

        Args:
            joueur (object): Le joueur qui doit attaqué.
            position (float): La position `y du haut du plateau`.
        """
        fond.delete('pointeur')
        d = fond.find_withtag('ecranFin')
        if not self.getEtatNotifs(joueur):
            a = self.localiseCurseur(joueur.cTire)
            if a != None and len(d) == 0:
                b = fond.coords(a)
                self.dessineViseur(b, a)
        c = fond.coords(joueur.cTire[0][0])
        if int(c[1]) == int(position) and len(d) == 0:
            fond.after(50, self.attaque, joueur, c[1])
        else:
            fond.delete('pointeur')

    def getEtatNotifs(self, joueur: Joueur) -> bool:
        """Regarde si les notification d'un joueur son visible à l'écran.

        Args:
            joueur (Joueur): Propriétaire des informations à vérifier.

        Returns:
            bool: True s'il y a au moins une notif et False sinon.
        """
        rep = joueur.notifTouche.getEtat()
        if not rep:
            rep = joueur.notifCoule.getEtat()
        return rep

    def marquerCase(self, idCase: str, idplateau: str, joueurCible: Joueur, joueur: Joueur) -> None:
        """Marque les cases touchées.

        Args:
            idCase (str): Le code de la case.
            idplateau (str): Le plateau auquel elle correspond.
            joueurCible (Joueur): Le joueur victime du tir.
            joueur (Joueur): Le joueur qui est en train de jouer.
        """
        tag = idCase+idplateau
        c = grisBlanc
        listeBateau = self.listeBateaux1
        if joueurCible == self.j2:
            listeBateau = self.listeBateaux2
        repTouche = estToucheBateau(joueurCible, idCase)
        if repTouche[0]:
            c = 'red'
        fond.itemconfigure(tag, fill=c)
        bateaux = joueurCible.getBateaux()
        if estCoule(bateaux[repTouche[1]]) and not listeBateau[repTouche[1]]:
            plongerDanslAbysse(bateaux[repTouche[1]])
            listeBateau[repTouche[1]] = True
            joueur.notifCoule.modifMessage(joueurCible.getBateaux()[repTouche[1]].nom)
            joueur.notifCoule.montre()
        elif repTouche[0]:
            joueur.notifTouche.modifMessage(case=idCase)
            joueur.notifTouche.montre()

    def getEtatCase(self, idCase: str, idPlateau: str="") -> bool:
        """Renvoie True si la case passée en paramètre est touchable.

        Args:
            idCase (str): Le code de la case à tester
            idPlateau (str, optional): Le code du plateau si l'on ne dispose que du nom de la case. Defaults to "".

        Returns:
            bool: Vrai ou Faux selon la possibilité de touché ou non la case.
        """
        tag = idCase+idPlateau
        c = fond.itemcget(tag, 'fill')
        rep = True
        if c == 'red' or c == grisBlanc:
            rep = False
        return rep

    def monter(self, pas: float):
        """Fait descendre les plateaux (animations)

        Args:
            pas (float): La vitesse de déplacement du plateau.
        """
        for i in range(len(self.joueurs)):
            fond.move(('cTire'+str(i+1)), 0, pas)
        a = fond.coords(self.j1.cTire[0][0])
        if int(a[1]) != int(origyp):
            fond.after(30, self.monter, pas)
        else:
            fond.itemconfigure('titre', text=self.j1.nom)
            self.incrementTour()
            self.connect()
            self.affStats(0)
            self.attaque(self.j1, a[1])

    def descendre(self, pas: float):
        """Fait monter les plateaux (animations)

        Args:
            pas (float): La vitesse de déplacement du plateau.
        """
        for i in range(len(self.joueurs)):
            fond.move(('cTire'+str(i+1)), 0, -pas)
        a = fond.coords(self.j2.cTire[0][0])
        if int(a[1]) != int(origyp):
            fond.after(30, self.descendre, pas)
        else:
            fond.itemconfigure('titre', text=self.j2.nom)
            self.connect()
            self.affStats(1)
            self.attaque(self.j2, a[1])

    def monterOuQuitter(self):
        """Vérifie si le premier joueur a perdu, ou si le second joueur n'a pas de notif, 
           sinon il déclenche le tour du premier joueur.
        """
        if aPerduJoueur(self.j1):
            Fin(self.joueurs, 1, self.tour)
        elif not self.getEtatNotifs(self.j2):
            self.monter(pasApas)
        else:
            fond.after(50, self.monterOuQuitter)

    def descendreOuQuitter(self):
        """Vérifie si le second joueur a perdu, ou si le premier joueur n'a pas de notif, 
           sinon il déclenche le tour du second joueur.
        """
        if aPerduJoueur(self.j2):
            Fin(self.joueurs, 0, self.tour)
        elif not self.getEtatNotifs(self.j1):
            self.descendre(pasApas)
        else:
            fond.after(50, self.descendreOuQuitter)

    def deconnect(self):
        """Supprimme les événements liés au clic de la souris.
        """
        fond.tag_unbind('pointeur', '<Button-1>')
        fond.tag_unbind('cTire2', '<Button-1>')
        fond.tag_unbind('cTire1', '<Button-1>')

    def connect(self):
        """(Re)crée les événements liés au clic de la souris.
        """
        fond.tag_bind('cTire1', '<Button-1>', self.aj2)
        fond.tag_bind('cTire2', '<Button-1>', self.aj1)
        fond.tag_bind('pointeur', '<Button-1>', self.cliqueCurseur)

    def cliqueCurseur(self, event):
        """Réagis à un clique sur le curseur.

        Args:
            event (_type_): _description_
        """
        t = fond.itemcget('affiTgVis', 'text')
        if t != "X":
            self.deconnect()
            p1 = self.getEtatCase(t, 'c1')
            p2 = self.getEtatCase(t, 'c2')
            if p1 or p2:
                c = fond.coords(self.j1.cTire[0][0])
                if int(c[1]) == int(origyp):
                    self.j1.toucheCase(estToucheBateau(self.j2, t)[0])
                    self.affStats(0)
                    self.marquerCase(t, 'c1', self.j2, self.j1)
                    fond.after(1000, self.descendreOuQuitter)
                else:
                    self.j2.toucheCase(estToucheBateau(self.j1, t)[0])
                    self.affStats(1)
                    self.marquerCase(t, 'c2', self.j1, self.j2)
                    fond.after(1000, self.monterOuQuitter)

    def aj1(self, event):
        """Réagit à un clique sur le plateau d'attaque du second joueur.

        Args:
            event (_type_): _description_
        """
        t = fond.itemcget('affiTgVis', 'text')
        if t != "X":
            self.deconnect()
            p = self.getEtatCase(t, 'c2')
            self.j2.toucheCase(estToucheBateau(self.j1, t)[0])
            self.affStats(1)
            if p:
                self.marquerCase(t, 'c2', self.j1, self.j2)
                fond.after(1000, self.monterOuQuitter)

    def aj2(self, event):
        """Réagit à un clique sur le plateau d'attaque du premier joueur.

        Args:
            event (_type_): _description_
        """
        t = fond.itemcget('affiTgVis', 'text')
        if t != "X":
            self.deconnect()
            p = self.getEtatCase(t, 'c1')
            self.j1.toucheCase(estToucheBateau(self.j2, t)[0])
            self.affStats(0)
            if p:
                self.marquerCase(t, 'c1', self.j2, self.j1)
                fond.after(1000, self.descendreOuQuitter)