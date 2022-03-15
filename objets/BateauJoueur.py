from FondMarin import *

class Bateau(): # Crée les bateaux.
    def __init__(self, nom: str, taille: int, id: int, joueur: object):
        self.taille = taille
        self.orient = 'h'
        self.nom = nom
        self.pos = None
        self.defil = False
        self.tag = 'bat' + str(id) + '.' + str(joueur.getId())
        self.tagPlus = 'tbat' + str(id) + '.' + str(joueur.getId())
        self.proprio = joueur
        self.etatSeg = ['o']*taille
        self.coule = False
        self.sens = 1
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
        x = a[2]*0.05
        y = a[3]*0.05
        fond.create_text(a[2]/2, y*0.4, text=self.nom, fill='white', font=Poli1, 
                         tags=(self.tagPlus, 'nomBat', ('nSet'+str(cdJ))))
        fond.create_rectangle(x, y, x+(a[2]*0.12)*self.taille, y+(a[3]*0.05), fill="#444444", 
                              tags=('bateaux', self.tag, ('set'+str(cdJ))))
        self.miniature = fond.coords(self.tag)

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
        fond.itemconfigure(self.tag, outline='black', width=1)
        a = fond.find_withtag('Pharos')
        if len(a) >= 1:
            b = fond.itemcget('Pharos', 'outline')
            if b == 'white':
                c = fond.coords('Pharo1')
                e = (c[2]-c[0])*0.1
                self.positionneBien((c[0]+e, c[1]+e))
            else:
                self.resetBat()
        else:
            self.resetBat()

    def declenMouv(self):
        """Sélectionne le bateau.
        """
        self.defil = True
        self.orient = 'h'
        fond.itemconfigure(self.tag, outline=vertFluo, width=3)
        a = fond.coords(self.proprio.base[0][0])
        b = self.miniature
        x = a[2]-a[0]
        y = a[3]-a[1]
        fond.coords(self.tag, b[0], b[1], b[0]+(self.taille*x-(2*(x/10))), b[1]+y*0.8)
        self.proprio.blocVert(self)
        self.scotchBat()

    def scotchBat(self):
        """Fait en sorte que le bateau suive la souris.
        """
        a = fond.winfo_pointerxy()
        e = fond.find_withtag(self.tag)
        if len(e) >= 1:
            b = fond.coords(self.tag)
            c = (b[2]-b[0])/2
            d = (b[3]-b[1])/2
            self.glisseListe((a[0], a[1]), (c, d))
            fond.coords(self.tag, a[0]-c, a[1]-d, a[0]+c, a[1]+d)
            self.neonCase()
        if self.defil:
            fond.after(5, self.scotchBat)

    def neonCase(self):
        """Liste les cases actuellement occupées par le bateau.
        """
        co = fond.coords(self.tag)
        milieu = co[1]+((co[3]-co[1])/2)
        fixe1 = (co[0], milieu)
        fixe2 = (co[2], milieu)
        if self.orient == 'v':
            milieu = co[0]+((co[2]-co[0])/2)
            fixe1 = (milieu, co[1])
            fixe2 = (milieu, co[3])
        a = self.localCase(fixe1)
        b = self.localCase(fixe2)
        c = self.iNon(a)
        d = self.iNon(b)
        if d:
            li = []
            e = self.trouveCase(b)
            self.rempliListe(e, li, 'ar')
        elif c:
            li = []
            e = self.trouveCase(a)
            self.rempliListe(e, li, 'av')
        else:
            li = [None]*self.taille
            e = 'error'
        self.pos = li
        self.brillePlacement(self.proprio.getBateaux())

    def tourne(self, event):
        """Fait tourner le bateau.

        Args:
            event (_type_): _description_
        """
        if self.defil:
            a = fond.coords(self.tag)
            l = (a[2]-a[0])/2
            h = (a[3]-a[1])/2
            x1 = a[0] + l - h
            y1 = a[1] + h - l
            x2 = a[0] + l + h
            y2 = a[1] + h + l
            if self.orient == 'h':
                self.orient = 'v'
            else:
                self.orient = 'h'
            fond.coords(self.tag, x1, y1, x2, y2)

    def positionneBien(self, coo: tuple): 
        """Fait en sorte que le bateau appelé soit bien positionné sur le plateau.

        Args:
            coo (tuple): position du bateau.
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

    def resetBat(self):
        """Supprime le modèle "grande taille" du bateau pour recréer le modèle "petite taille."
        """
        c = fond.coords('pg')
        x = c[2]*0.05
        y = c[3]*0.05
        t = self.getTags()
        a = fond.coords(t[0])
        fond.delete(t[0])
        fond.create_rectangle(a[0], a[1], a[0]+(c[2]*0.12)*self.taille, a[1]+(c[3]*0.05), fill="#444444", 
                            tags=('bateau', t[0], ('set'+str(self.proprio.id))))
        self.reposeBat((x, y))

    def reposeBat(self, coo: tuple):
        """Remet le bateau en place dans le panneau latéral de gauche.

        Args:
            coo (tuple): coordonnées du bateau.
        """
        t = self.getTags()
        a = fond.coords(t[0])
        b = int(a[0])-int(coo[0])
        d = int(a[1])-int(coo[1])
        fond.move(t[0], -b, -d)
        if int(b) != 0:
            fond.after(50, self.reposeBat, coo)
        else:
            self.pos = None
            self.proprio.vigile()

    def glisseListe(self, souris: tuple, milieu: tuple):
        """Corrige les éventuels problèmes de vitesse rencontrés lors de la localisation des bateaux.

        Args:
            souris (tuple): Position de la souris.
            milieu (tuple): Position du milieu du bateau.
        """
        if self.orient == 'h':
            if souris[0] < milieu[0]:
                self.sens = -1
            else:
                self.sens = 0
        else:
            if souris[1] < milieu[1]:
                self.sens = -2
            else:
                self.sens = 0

    def localCase(self, coo: tuple) -> str:
        """Trouve les cases individuellement.

        Args:
            coo (tuple): Coordonnée du bateau.

        Returns:
            str: Nom d'une case.
        """
        b = None
        for i in range(len(self.proprio.base)):
            for j in range(len(self.proprio.base[i])):
                a = fond.coords(self.proprio.base[i][j])
                if coo[0] >= a[0] and coo[0] <= a[2] and coo[1] >= a[1] and coo[1] <= a[3]:
                    b = self.proprio.base[i][j]
        return b

    def iNon(self, val) -> bool:
        """Check si la valeur passée en paramètre est nulle ou non...

        Args:
            val (_type_): valeur à comparer.

        Returns:
            bool: True, si pas nul, et False, sinon...
        """
        a = True
        if val == None:
            a = False
        return a

    def trouveCase(self, case: str) -> list:
        """Cherche la position sur le plateau de la case passée en paramètre.

        Args:
            case (str): Nom de la case.

        Returns:
            list: coordonnées d'une case.
        """
        y = 0
        a = False
        while y < len(self.proprio.base) and not a:
            x = 0
            while x < len(self.proprio.base[y]) and not a:
                if self.proprio.base[y][x] == case:
                    a = True
                x = x + 1
            y = y + 1
        return [x-1, y-1]

    def rempliListe(self, coo: list, position: list, bout: str):
        """Remplis la liste de position du bateau.

        Args:
            coo (list): Coordonnées de la base du bateau.
            position (list): Position du bateau.
            bout (str): Extrémité du bateau.
        """
        if bout == 'av':
            mul = 1
        elif bout == 'ar':
            mul = -1
        for i in range(self.taille):
            if self.orient == 'h':
                a = coo[0]+(i)*mul+self.sens
                if a >= 0 and a <= 9:
                    position.append(self.proprio.base[coo[1]][a])
                else:
                    position.append(None)
            else:
                a = coo[1]+(i)*mul+self.sens
                if a >= 0 and a <= 9:
                    position.append(self.proprio.base[a][coo[0]])
                else:
                    position.append(None)
        if bout == 'ar':
            position.reverse()

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