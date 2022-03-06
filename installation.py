from FondMarin import fond, dpd, tlatba, xf, yf, yp, Poli2, gris, bleuBt, blanc
from ui.bouton import Bouton

class Install:
    def __init__(self, joueur: object, fonction) -> None:
        self.joueur = joueur
        self.liBat = self.joueur.getBateaux()
        fond.itemconfigure('titre', text=f"{joueur.nom.upper()} - INSTALLATION")
        self.bt = Bouton(fonction, "VALIDER LE PLAN", bleuBt, False, ['valid', 'install'])
        self.bt.dessine((xf-tlatba/2, (yf*0.945)-(yf*0.84/20)))
        self.joueur.setVerif(self.fin)
        self.joueur.miseEnPlace()

    def sup(self) -> None:
        """Gère la suppression correcte de l'installateur.
        """
        l = self.joueur.getBateaux()
        for i in range(len(l)):
            t = l[i].getTags()
            fond.delete(t[1])
            fond.itemconfigure(t[0], state='hidden')
            fond.tag_unbind(t[0], '<Button-1>')
            fond.tag_unbind(t[0], '<Button-3>')
        fond.delete('install')
        fond.itemconfigure('base'+str(self.joueur.id), state='hidden')

    def fin(self):
        """Place le bouton dans les états "veille" et "actif", en fonction de la position des bateaux.
        """
        d = True
        i = 0
        l = self.joueur.getBateaux()
        while d and i < len(l):
            if l[i].pos == None:
                d = False
            elif type(l[i].pos) == list:
                if None in l[i].pos:
                    d = False
                    l[i].pos = None
            i = i + 1
        if d:
            self.bt.setEtat(True)
        else:
            self.bt.setEtat(False)