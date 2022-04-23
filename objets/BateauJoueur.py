from FondMarin import fond, tailleCase, Poli1
from Image import Ima
from objets.Bateau import Bateau

class BateauJoueur(Bateau):
    def __init__(self, nom: str, taille: int, id: int, image: Ima, proprietaire: object):
        """Crée un bateau lié à un joueur.

        Args:
            nom (str): Le nom du bateau.
            taille (int): Le nombre de cases qu'occupe le bateau sur le plateau.
            id (int): Le numéro d'identification du bateau pour son propriétaire.
            image (Ima): Apparence du bateau.
            propriétaire (Joueur): Propriétaire du bateau.
        """
        super().__init__(nom, taille, id, image, proprietaire)
        self.defil = False
        fond.tag_bind(self.tag, '<Button-1>', self.switchMode)
        fond.tag_bind(self.tag, '<Button-3>', self.tourne)

    def getTags(self) -> list:
        """Retourne les tags du bateau

        Returns:
            list: Tag du bateau et de son nom.
        """
        return [self.tag, self.tagPlus]

    def dessine(self, cdJ: int):
        """Dessine le bateau.

        Args:
            cdJ (int): Le code du joueur (propriétaire).
        """
        a = fond.coords('pg')
        case = tailleCase
        x = a[2]*0.5
        y = a[3]*0.05 + (case*0.8)/2
        fond.create_text(x, y*0.3, text=self.nom, fill='white', font=Poli1, 
                         tags=(self.tagPlus, 'nomBat', ('nSet'+str(cdJ))))
        fond.create_image(x, y, image=self.horiz, tags=('bateaux', self.tag, ('set'+str(cdJ))))

    def switchMode(self, event):
        """Sélectionne et déselectionne le bateau.

        Args:
            event (_type_): _description_
        """
        if self.defil:
            self.immobile()
        else:
            self.declenMouv()

    def immobile(self):
        """Désélectionne le bateau.
        """
        self.defil = False
        debaras = fond.coords('pg')
        a = fond.find_withtag('Pharos')
        if len(a) >= 1:
            b = fond.itemcget('Pharos', 'outline')
            if b == 'white':
                c1 = fond.coords('Pharo1')
                cmax = fond.coords('Pharo'+str(self.taille))
                x = c1[0]+(cmax[2]-c1[0])/2
                y = c1[1]+(c1[3]-c1[1])/2
                if self.orient == 'v':
                    x = c1[0]+(c1[2]-c1[0])/2
                    y = c1[1]+(cmax[3]-c1[1])/2
                self.positionneBien((x, y))
            else:
                self.repose((debaras[2]*0.5, debaras[3]*0.05 + (tailleCase*0.8)/2))
        else:
            self.repose((debaras[2]*0.5, debaras[3]*0.05 + (tailleCase*0.8)/2))

    def declenMouv(self):
        """Sélectionne le bateau.
        """
        self.defil = True
        self.orient = 'h'
        fond.itemconfigure(self.tag, image=self.horiz)
        self.proprio.blocVert(self)
        self.scotchBat()

    def scotchBat(self):
        """Fait en sorte que le bateau suive la souris.
        """
        a = fond.winfo_pointerxy()
        e = fond.find_withtag(self.tag)
        if len(e) >= 1:
            fond.coords(self.tag, a[0], a[1])
            self.neonCase()
        if self.defil:
            fond.after(5, self.scotchBat)

    def neonCase(self):
        """Liste les cases actuellement occupées par le bateau.
        """
        co = fond.coords(self.tag)
        milieu = self.localCase((co[0], co[1]))
        if milieu != None:
            self.rempliListe(milieu)
        else:
            self.pos = [None]*self.taille
        self.brillePlacement(self.proprio.getBateaux())

    def tourne(self, event):
        """Fait tourner le bateau.

        Args:
            event (_type_): _description_
        """
        if self.defil:
            if self.orient == 'h':
                self.orient = 'v'
                fond.itemconfigure(self.tag, image=self.verti)
            else:
                self.orient = 'h'
                fond.itemconfigure(self.tag, image=self.horiz)

    def positionneBien(self, coo: tuple): 
        """Fait en sorte que le bateau appelé soit bien positionné sur le plateau.

        Args:
            coo (tuple): position que le bateau doit atteindre.
        """
        t = self.getTags()
        a = fond.coords(t[0])
        b = coo[0] - a[0]
        c = coo[1] - a[1]
        fond.move(t[0], int(b), int(c))
        if int(b) != 0:
            fond.after(50, self.positionneBien, coo)
        else:
            fond.delete('Pharos')
            self.proprio.verifFonction()

    def repose(self, coo: tuple):
        """Remet le bateau en place dans le panneau latéral de gauche.

        Args:
            coo (tuple): coordonnées du bateau.
        """
        t = self.getTags()
        a = fond.coords(t[0])
        b = int(a[0])-int(coo[0])
        d = int(a[1])-int(coo[1])
        fond.move(t[0], -b, -d)
        fond.itemconfigure(self.tag, image=self.horiz)
        if int(b) != 0:
            fond.after(50, self.repose, coo)
        else:
            self.pos = None
            self.proprio.vigile()

    def localCase(self, coo: tuple) -> str:
        """Trouve les cases individuellement.

        Args:
            coo (tuple): Coordonnée du bateau.

        Returns:
            str: Nom d'une case.
        """
        b = None
        for i in range(self.proprio.base.getDimensions()[0]):
            ligne = self.proprio.base.getLigne(self.alphabet[i])
            for j in range(len(ligne)):
                a = fond.coords(ligne[j])
                if coo[0] >= a[0] and coo[0] <= a[2] and coo[1] >= a[1] and coo[1] <= a[3]:
                    b = ligne[j]
        return b

    def rempliListe(self, nom: str):
        """Remplis la liste de position du bateau.

        Args:
            nom (str): Nom de la case occupée par le centre du bateau.
        """
        avant = int((self.taille-1)/2)
        arriere = self.taille-1-avant
        if self.orient == 'h':
            ligne = self.proprio.base.getLigne(nom[0])
        else:
            ligne = self.proprio.base.getColonne(int(nom[1:len(nom)-2]))
        liste = []
        base = ligne.index(nom)
        for i in range(avant):
            if base-1-i >= 0:
                liste.append(ligne[base-1-i])
            else:
                liste.append(None)
        liste.reverse()
        liste.append(nom)
        for i in range(arriere):
            if base+1+i < len(ligne):
                liste.append(ligne[base+1+i])
            else:
                liste.append(None)
        self.pos = liste

    def brillePlacement(self, liste: list):
        """Mets en évidence les cases où le bateau sélectionné se trouvera une fois relaché.

        Args:
            liste (list): Liste des cases du bateau.
        """
        fond.delete('Pharos')
        c = 'white'
        if None in self.pos:
            c = 'red'
        else:
            for j in range(len(liste)):
                if liste[j] != self and liste[j].pos != None:
                    if not self.voisin(liste[j]):
                        c = 'red'
        for i in range(len(self.pos)):
            if self.pos[i] != None:
                a = fond.coords(self.pos[i])
                b = 'Pharo' + str(i+1)
                fond.create_rectangle(a[0], a[1], a[2], a[3], fill='', outline=c, width=4, tags=(b, 'Pharos'))
                fond.tag_raise(self.tag, 'Pharos')

    def voisin(self, bateau: object) -> bool:
        """Vérifie si le bateau sélectionné n'empiète pas sur un autre bateau déjà placé.

        Args:
            bateau (object): bateau.

        Returns:
            bool: True si les deux bateaux ont au moins une case en commun.
        """
        a = True
        i = 0
        while i < len(self.pos) and a:
            if self.pos[i] in bateau.pos:
                a = False
            i = i + 1
        return a