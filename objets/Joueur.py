from random import *
from FondMarin import *
from objets.BateauJoueur import Bateau
from objets.plateau import Plateau
from ui.notif import Notification
from Image import Ima

class Joueur(): # Initialise un joueur.
    def __init__(self, code: int):
        a = 'base' + str(code)
        f = 'cTire' + str(code)
        d = 'notifTouche' + str(code)
        e = 'notifCoule' + str(code)
        nomBats = ["Porte Avion", "Croiseur", "Sous-marin n°1", "Sous-marin n°2", "Torpilleur"]
        tailleBats = [5, 4, 3, 3, 2]
        imaBats = [Ima('images/bateaux/5.png'), Ima('images/bateaux/4.png'), Ima('images/bateaux/3.png'), 
                   Ima('images/bateaux/3.png'), Ima('images/bateaux/2.png')]
        self.id = code
        self.nom = f"Joueur {self.id}"
        self.base = Plateau(10, 10, a)
        self.cTire = Plateau(10, 10, f)
        self.SetBateaux = []
        self.pret = False
        self.stats = [0, [0, 0], [0, 0]]
        # bateaux
        for i in range(len(nomBats)):
            bat = Bateau(nomBats[i], tailleBats[i], i, imaBats[i], self)
            self.SetBateaux.append(bat)
        # /bateaux
        shuffle(self.SetBateaux)
        # notifs
        self.notifTouche = Notification("Touché !", d)
        self.notifCoule = Notification("Coulé !", e)
        # /notifs

    def getBateaux(self) -> list:
        """Retourne la liste des bateaux du joueur.

        Returns:
            list: Liste des bateaux
        """
        return self.SetBateaux

    def getId(self) -> int:
        """Retourne l'identifiant du joueur

        Returns:
            int: identifiant du joueur.
        """
        return self.id

    def getNom(self) -> str:
        """Retourne le nom du joueur.

        Returns:
            str: nom du joueur
        """
        return self.nom

    def getStats(self) -> list:
        """Retourne la liste des statistiques du joueur.

        Returns:
            list: Liste des statistiques individuelles.
        """
        return self.stats

    def dessineBateaux(self) -> None:
        """Dessine tous les bateaux du joueur.
        """
        for i in range(len(self.SetBateaux)):
            self.SetBateaux[i].dessine(self.id)

    def montreBase(self) -> None:
        """Affiche le plateau d'installation du joueur.
        """
        lat = fond.coords('pg')
        self.base.dessine((lat[2], yf*0.105))

    def miseEnPlace(self) -> None:
        """Prépare le terrain pour que le joueur puisse positionner ses bateaux.
        """
        self.montreBase()
        self.dessineBateaux()
        self.placeLat()

    def blocVert(self, bateau: Bateau):
        """Déselectionne tous les bateaux sauf celui passé en paramètre.

        Args:
            bateau (Bateau): Bateau à ne pas déseclectionné.
        """
        for i in range(len(self.getBateaux())):
            if bateau != self.SetBateaux[i]:
                if self.SetBateaux[i].defil:
                    self.SetBateaux[i].immobile()

    def vigile(self):
        """Remet tout les bateaux mal positionnés, coorectement en place à côté du plateau.
        """
        a = False
        c = fond.coords('pg')
        l = self.getBateaux()
        for i in range(len(l)):
            t = l[i].getTags()
            b = fond.coords(t[0])
            if int(b[0]) <= int(c[2]*0.5):
                a = True
        if a:
            self.placeLat()
        else:
            fond.after(1000, self.vigile)

    def placeLat(self):
        """Place les bateaux sur le panneau latéral de gauche.
        """
        plateau = fond.coords('pg')
        liste = self.getBateaux()
        for i in range(len(liste)):
            tags = liste[i].getTags()
            rect = fond.coords(tags[0])
            titre = fond.coords(tags[1])
            c = int(plateau[3]*0.05 + (tailleCase*0.8)/2)
            if int(rect[1]) == c:
                fond.move(tags[0], 0, yp*(i+1))
            if int(titre[1]) == int(c*0.3):
                fond.move(tags[1], 0, yp*(i+1))
            self.verifFonction()
        fond.delete('Pharos')

    def setVerif(self, fonction):
        """Paramètre la foction de vérification avec celle passée en paramètre.

        Args:
            fonction (_type_): Le vérificateur
        """
        self.verifFonction = fonction

    def toucheCase(self, case: bool) -> None:
        """Incrémente le compteur de case touchées.
        """
        self.stats[0] = self.stats[0] + 1
        if case:
            self.stats[1][0] = self.stats[1][0] + 1
        else:
            self.stats[2][0] = self.stats[2][0] + 1
        self.stats[1][1] = round(self.stats[1][0]*100/self.stats[0], 1)
        self.stats[2][1] = round(self.stats[2][0]*100/self.stats[0], 1)