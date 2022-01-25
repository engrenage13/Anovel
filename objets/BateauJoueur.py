from FondMarin import *
from placement import *

class Bateau(): # Crée les bateaux.
    def __init__(self, nom: str, taille: int, id: int, cdJ: int):
        self.taille = taille
        self.orient = 'h'
        self.nom = nom
        self.pos = None
        self.defil = False
        self.tag = 'bat' + str(id) + '.' + str(cdJ)
        self.tagPlus = 'ttbat' + str(id) + '.' + str(cdJ)
        self.proprio = joueurs[cdJ-1]
        self.etatSeg = ['o']*taille
        self.coule = False
        self.sens = 1
        self.dessBat(cdJ)
        fond.tag_bind(self.tag, '<Button-1>', self.switchMode)
        fond.tag_bind(self.tag, '<Button-3>', self.tourne)
        joueurs[cdJ-1].SetBateaux.append(self)

    def dessBat(self, cdJ: int): # Dessine le bateau.
        a = fond.coords('pg')
        x = a[2]*0.05
        y = a[3]*0.05
        fond.create_text(a[2]/2, y*0.4, text=self.nom, fill='white', tags=(self.tagPlus, 'nomBat', ('nSet'+str(cdJ))))
        fond.create_rectangle(x, y, x+(a[2]*0.12)*self.taille, y+(a[3]*0.05), fill="#444444", 
                              tags=('bateaux', self.tag, ('set'+str(cdJ))))
        self.miniature = fond.coords(self.tag)

    def switchMode(self, event): # Sélectionne et déselectionne le bateau.
        if self.defil:
            self.immobile()
        else:
            self.declenMouv()

    def immobile(self): # Désélectionne le bateau.
        self.defil = False
        fond.itemconfigure(self.tag, outline='black', width=1)
        a = fond.find_withtag('Pharos')
        if len(a) >= 1:
            b = fond.itemcget('Pharos', 'outline')
            if b == 'white':
                c = fond.coords('Pharo1')
                e = (c[2]-c[0])*0.1
                positionneBien(self, (c[0]+e, c[1]+e))
            else:
                resetBat(self)
        else:
            resetBat(self)

    def declenMouv(self): # Sélectionne le bateau.
        self.defil = True
        self.orient = 'h'
        fond.itemconfigure(self.tag, outline=vertFluo, width=3)
        a = fond.coords(self.proprio.base[0][0])
        b = self.miniature
        x = a[2]-a[0]
        y = a[3]-a[1]
        fond.coords(self.tag, b[0], b[1], b[0]+(self.taille*x-(2*(x/10))), b[1]+y*0.8)
        blocVert(self.nom)
        self.scotchBat()

    def scotchBat(self): # Fait en sorte que le bateau suive la souris.
        a = fond.winfo_pointerxy()
        e = fond.find_withtag(self.tag)
        if len(e) >= 1:
            b = fond.coords(self.tag)
            c = (b[2]-b[0])/2
            d = (b[3]-b[1])/2
            glisseListe((a[0], a[1]), (c, d), self)
            fond.coords(self.tag, a[0]-c, a[1]-d, a[0]+c, a[1]+d)
            self.neonCase()
        if self.defil:
            fond.after(5, self.scotchBat)

    def neonCase(self): # Liste les cases actuellement occupées par le bateau.
        co = fond.coords(self.tag)
        milieu = co[1]+((co[3]-co[1])/2)
        fixe1 = (co[0], milieu)
        fixe2 = (co[2], milieu)
        if self.orient == 'v':
            milieu = co[0]+((co[2]-co[0])/2)
            fixe1 = (milieu, co[1])
            fixe2 = (milieu, co[3])
        a = localCase(fixe1, self)
        b = localCase(fixe2, self)
        c = iNon(a)
        d = iNon(b)
        if d:
            li = []
            e = trouveCase(b, self)
            rempliListe(e, li, 'ar', self)
        elif c:
            li = []
            e = trouveCase(a, self)
            rempliListe(e, li, 'av', self)
        else:
            li = [None]*self.taille
            e = 'error'
        self.pos = li
        brillePlacement(self, self.proprio.SetBateaux)

    def tourne(self, event): # Fait tourner le bateau.
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