from FondMarin import *
from animations.Carrelage import Etincelle
from ui.bouton import Bouton

class Fin:
    def __init__(self, joueurs: list, gagnant: int, tour: int) -> None:
        self.joueurs = joueurs
        self.gagnant = gagnant
        self.longPartie = tour
        self.distance = 0
        fond.delete('pointeur')
        fond.create_rectangle(0, 0, xf, yf, fill='black', tag='ecranFin')
        self.victoire()
        self.maitreGlisse(['vict1', 'vict2'])

    def victoire(self) -> None:
        """Crée les éléments permettants de dire qui a gagner la partie.
        """
        fond.create_text(xf*0.5, yf+yf*0.4, text=self.joueurs[self.gagnant].getNom(), font=Poli3, fill=bleu2, 
                         tags=('ecranFin', 'plafDec', 'vict1', 'artifice'))
        fond.create_text(xf*0.5, yf+yf*0.5, text="A Gagné !", font=Lili3, fill=vertFluo, 
                         tags=('ecranFin', 'vict1', 'artifice'))
        etincelle = Etincelle(couleurs=[rouge, gris]+mer)
        etincelle.eblouissement()
        suite = Bouton(self.suite, "Continuer", bleuBt, nom=['btsuite', 'ecranFin', 'vict2', 'artifice'])
        suite.dessine((xf/2, yf+yf*0.7))

    def maitreGlisse(self, liste: list, indice: int=0) -> None:
        """Fait défiler vers le haut de 1 écran, tout les tags se trouvant dans la liste en partant de l'indice.

        Args:
            liste (list): Liste de tags
            indice (int, optional): L'indice de position de la liste ou la fonction doit commencer. Defaults to 0.
        """
        if self.distance == 0:
            self.glisse(liste[indice])
            indice = indice + 1
        if indice < len(liste):
            fond.after(80, self.maitreGlisse, liste, indice)

    def glisse(self, cible: str) -> None:
        """Fait défiler vers le haut de 1 écran, les éléments marqué du tag cible à passer en paramètre.

        Args:
            cible (str): Tag des éléments à faire défiler.
        """
        p = yf*0.025
        fond.move(cible, 0, -p)
        if self.distance < 40:
            self.distance = self.distance + 1
            fond.after(20, self.glisse, cible)
        else:
            self.distance = 0

    def dessStats(self) -> None:
        """Dessine les cadres de stats des 2 joueurs.
        """
        xo = xf*0.05
        l = xf*0.65
        yo = yf*1.1
        h = yf*0.3
        titres = ["Nb. Cases Touchées", "Nb. Touché", "Nb. Raté"]
        for i in range(len(self.joueurs)):
            c = grisClair
            j = self.joueurs[len(self.joueurs)-self.gagnant-1]
            valeurs = self.joueurs[len(self.joueurs)-self.gagnant-1].getStats()
            desc = "Perdant"
            if i == 0:
                c = bleuBt
                j = self.joueurs[self.gagnant]
                valeurs = self.joueurs[self.gagnant].getStats()
                desc = "Gagnant"
            t = j.getNom()
            fond.create_rectangle(xo, yo, xo+l, yo+h, fill=gris, width=3, 
                                  tags=('ecranFin', 'statsCad'))
            fond.create_rectangle(xo, yo, xo+l, yo+yf*0.08, fill=c, tags=('ecranFin', 'statsCad'))
            fond.create_text(xo+xf*0.01*len(t), yo+yf*0.04, text=t.upper(), font=Lili3, fill=blanc, 
                            tags=('ecranFin', 'statsCad'))
            fond.create_text(xo+l*0.93, yo+yf*0.04, text=desc, font=Lili2, fill=blanc, 
                             tags=('ecranFin', 'statsCad'))
            x = xo*2.5
            y = yo+h*0.35
            for j in range(len(titres)):
                if type(valeurs[j]) != list:
                    valeur = valeurs[j]
                else:
                    valeur = f"{valeurs[j][0]} ({valeurs[j][1]}%)"
                taille = Lili3
                if len(str(valeur)) > 4:
                    taille = Lili2
                fond.create_text(x, y, text=titres[j], font=Lili2, fill=blanc, tags=('ecranFin', 'statsCad'))
                fond.create_text(x, y+yf*0.04, text=valeur, font=taille, fill=blanc, 
                                 tags=('ecranFin', 'statsCad'))
                x = x + l/6
            yo = yo + h*1.3

    def suite(self) -> None:
        """Réagit au clic sur le bouton "Continuer" de la première partie (fait apparaître les stats).
        """
        fond.create_text(xf-tlatba*0.55, yf*1.1, text=f"Nombre de tours : {self.longPartie}", font=Poli1, 
                         fill=blanc, tags=('ecranFin', 'vict3'))
        quit = Bouton(auRevoir, "Quitter", rouge, nom=['auRevoir', 'ecranFin', 'vict3'])
        quit.dessine((xf-tlatba*0.55, yf*1.7))
        self.maitreGlisse(['artifice', 'statsCad', 'vict3'])
        self.dessStats()