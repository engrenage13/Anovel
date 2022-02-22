from FondMarin import fond, xf, yf, dpd, tlatba, version, Poli1, Lili1, Lili3, gris, mauve, blanc, noir, rouge
from installation import Install
from objets.Joueur import Joueur
from attaque import attaque

class Partie:
    def __init__(self):
        self.joueurs = []

    def getJoueurs(self) -> list:
        if len(self.joueurs) == 0:
            raise IndexError("getJoueurs : Aucun joueur n'a était créé.")
        return self.joueurs

    def getJoueur(self, indice: int) -> object:
        if indice < 0 or indice > 1:
            raise IndexError("getJoueur : L'indice fournis n'est pas recevable, il doit être 0 ou 1.")
        elif len(self.joueurs) == 0:
            raise IndexError("getJoueur : Aucun joueur n'a était créé.")
        return self.joueurs[indice]

    def creerJoueurs(self) -> None:
        self.joueurs = []
        for i in range(2):
            j = Joueur(i+1)
            self.joueurs.append(j)

    def barreTitre(self) -> None:
        fond.create_rectangle(0, 0, xf, yf*0.05, fill=mauve)
        fond.create_text(xf*0.1, yf*0.027, text="", font=Poli1, fill=blanc, tag='titre')
        fond.create_text(xf*0.5, yf*0.027, text="", font=Poli1, fill=blanc, tag='tour')
        fond.create_text(xf*0.985, yf*0.022, text="x", font=Lili3, fill=rouge, tag='auRevoir')

    def miseEnPlace(self) -> None:
        fond.delete('accueil')
        fond.create_rectangle(0, yf*0.05, tlatba, yf, fill=noir, tags=('pg'))
        fond.create_rectangle(dpd, yf*0.05, xf, yf, fill=noir, tags=('pd'))
        fond.create_text(xf*0.015, yf*0.987, text=version, font=Lili1, fill=gris)
        self.creerJoueurs()
        self.barreTitre()
        self.inst = Install(self.getJoueur(0), self.checkEtat)

    def suite(self) -> None:
        self.inst.sup()
        del(self.inst)
        self.inst = Install(self.getJoueur(1), self.checkEtat)

    def jeu(self) -> None:
        j = self.getJoueurs()
        self.inst.sup()
        del(self.inst)
        fond.itemconfigure('titre', text=(self.getJoueur(0).nom))
        fond.move('titre', -xf*0.055, 0)
        for i in range(len(j)):
            t = 'cTire' + str(j[i].id)
            fond.itemconfigure(t, state='normal')
            fond.move(t, 0, yf*i)
        c = fond.coords(j[0].cTire[0][0])
        attaque(j[0], c[1])

    def checkEtat(self) -> None: # Vérifie l'état du bouton de validation, quand on clique dessus.
        a = fond.itemcget('btV', 'fill')
        b = 0
        i = 0
        if a != gris:
            j = self.getJoueurs()
            while i < len(j) and b < 2:
                if not j[i].pret:
                    b = b + 1
                    if b == 1:
                        j[i].pret = True
                i = i + 1
            if b < 2:
                self.jeu()
            else:
                self.suite()