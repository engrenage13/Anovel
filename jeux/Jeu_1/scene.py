from math import atan2, cos, sin
from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.objets.plateau import Plateau
from jeux.Jeu_1.objets.Joueur import Joueur
from jeux.Jeu_1.fonctions.jeu import viseur

class Scene:
    def __init__(self) -> None:
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.g1 = Grille(int(xf*0.04), [False], False)
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.plateau = Plateau()
        self.joueurs = []
        self.coordsViseur = (0, 0)
        bateaux = [[["gbb", 1], ["pbb", 4]], [["gbr", 1], ["pbr", 4]]]
        for i in range(2):
            self.joueurs.append(Joueur(i+1, bateaux[i]))
        +self.joueurs[0]
        # Between the worlds
        self.play = False
        self.message = ''
        self.lu = True

    def dessine(self) -> None:
        draw_rectangle(0, 0, xf, yf, BLACK)
        self.plateau.dessine(0, 0)
        self.joueurs[0].dessine()
        self.joueurs[1].dessine()
        self.tour()
        if self.play:
            self.g1.dessine(int(xf-self.g1.largeur), 0)
            if self.plateau.bloque:
                self.plateau.bloque = False
        else:
            if not self.plateau.bloque:
                self.plateau.bloque = True

    def tour(self) -> None:
        joueur = self.joueurs[0]
        if self.play:
            self.setPosViseur(joueur.bateaux[0])
        joueur.jouer(self.coordsViseur)

    def setPosViseur(self, bateau) -> None:
        passe = False
        i = 0
        while i < len(self.opt) and not passe:
            if self.opt[i][0].getContact():
                passe = True
            else:
                i += 1
        if not passe:
            i = 0
            while i < len(self.joueurs) and not passe:
                joueur = self.joueurs[i]
                j = 0
                while j < len(joueur.bateaux) and not passe:
                    bat = joueur.bateaux[j]
                    if check_collision_circle_rec((bateau.pos[0], bateau.pos[1]), bateau.portee, [bat.coords[0], bat.coords[1], bat.image.width, bat.image.height]):
                        if bat != bateau and bat.getContact():
                            passe = True
                        else:
                            j += 1
                    else:
                        j += 1
                i += 1
            if not passe:
                self.coordsViseur = self.metDansCercle(viseur(), bateau)

    def metDansCercle(self, coord: tuple, bateau) -> tuple:
        x = bateau.pos[0]
        y = bateau.pos[1]
        if not check_collision_point_circle(coord, (x, y), bateau.portee):
            dx = coord[0]-x
            dy = coord[1]-y
            angle = atan2(dy, dx)
            dxx = (bateau.portee-1)*cos(angle)
            dyy = (bateau.portee-1)*sin(angle)
            return (int(x+dxx), int(y+dyy))
        else:
            return coord

    # Between the worlds
    def portailAustral(self) -> None:
        if self.play:
            i = 0
            v = False
            while i < len(self.opt) and not v:
                if self.opt[i][0].getContact():
                    v = True
                    self.nouveauMessage(self.opt[i][1])
                else:
                    i += 1

    def nouveauMessage(self, message: str) -> None:
        self.message = message
        self.lu = False