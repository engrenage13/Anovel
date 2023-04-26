from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.Joueur import Joueur
#from jeux.Jeu_1.fonctions.bases import modifDestination
from jeux.Jeu_1.objets.bases.pivote import Pivote
from jeux.Jeu_1.intro import Intro
from jeux.Jeu_1.pageCarte import PageCarte
from jeux.Jeu_1.objets.bases.fenetre import Fenetre
from jeux.Jeu_1.config import config

class Jeu:
    def __init__(self) -> None:
        self.plateau = Plateau(14)
        self.plateau.bloque = True
        self.joueurs = []
        #bateaux = [[["gbb", 1], ["pbb", 4]], [["gbr", 1], ["pbr", 4]]]
        image1 = "jeux/Jeu_1/images/Bateaux/gbb.png"
        image2 = "jeux/Jeu_1/images/Bateaux/pbr.png"
        self.bateaux = [Pivote(image1), Pivote(image1), Pivote(image1), Pivote(image1), Pivote(image2), Pivote(image2), Pivote(image2), Pivote(image2)]
        y = 0
        i = 0
        while i < len(self.bateaux):
            for j in range(i):
                self.bateaux[i].gauche()
            a = self.plateau[y][0] + self.bateaux[i]
            if not a:
                y += 1
            else:
                i += 1
        #self.actuel = 0
        couleurs = [BLUE, RED]
        for i in range(len(couleurs)):
            self.joueurs.append(Joueur(i+1, [], couleurs[i]))
        #+self.joueurs[self.actuel]
        self.fen = {"intro": Intro(self.joueurs), "page_carte": PageCarte(), "plateau": self.plateau}
        if config['dev']:
            self.fenActif = config['dev'].lower()
        else:
            self.fenActif = 'intro'

    def dessine(self) -> None:
        fenetre = self.fen[self.fenActif]
        fenetre.dessine()
        if isinstance(fenetre, Fenetre) and fenetre.estFini():
            self.switch()

    def switch(self) -> None:
        if self.fenActif == 'intro':
            self.fenActif = 'page_carte'
        elif self.fenActif == 'page_carte':
            self.fenActif = 'plateau'

    def rejouer(self) -> None:
        for fenetre in self.fen:
            if isinstance(self.fen[fenetre], Fenetre):
                self.fen[fenetre].rejouer()
        self.fenActif = 'intro'
        self.plateau.bloque = True

    '''def tour(self) -> None:
        joueur = self.joueurs[self.actuel]
        if self.play:
            passe = self.setPosViseur(joueur.bateaux[joueur.actuel])
            if not passe:
                joueur.jouer(self.coordsViseur)
                self.joueurSuivant()

    def joueurSuivant(self) -> None:
        if not self.joueurs[self.actuel].actif:
            self.actuel += 1
            if self.actuel >= len(self.joueurs):
                self.actuel = 0
            +self.joueurs[self.actuel]

    def setPosViseur(self, bateau) -> bool:
        passe = False
        if is_mouse_button_pressed(0):
            i = 0
            while i < len(self.opt) and not passe:
                if self.opt[i][0].getContact():
                    passe = True
                else:
                    i += 1
            if not passe:
                x = get_mouse_x()
                y = get_mouse_y()
                if check_collision_point_circle((x, y), (int(bateau.pos[0]-bateau.image.width*0.04), bateau.pos[1]), bateau.RCD):
                    self.coordsViseur = modifDestination([x, y], bateau, self.joueurs[0].bateaux+self.joueurs[1].bateaux)
                else:
                    passe = True
        return passe'''