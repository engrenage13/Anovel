from systeme.FondMarin import *
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from jeux.Jeu_1.objets.plateau import Plateau
from jeux.Jeu_1.objets.Joueur import Joueur
from jeux.Jeu_1.fonctions.jeu import modifDestination

class Scene:
    def __init__(self) -> None:
        self.opt = [[Bouton(TB2n, PTIBT1, "MENU", 'images/ui/pause.png', [self.portailAustral]), "J1_MENU"]]
        self.g1 = Grille(int(xf*0.04), [False], False)
        self.g1.ajouteElement(self.opt[0][0], 0, 0)
        self.plateau = Plateau()
        self.joueurs = []
        self.coordsViseur = (0, 0)
        bateaux = [[["gbb", 1], ["pbb", 4]], [["gbr", 1], ["pbr", 4]]]
        self.actuel = 0
        for i in range(2):
            self.joueurs.append(Joueur(i+1, bateaux[i]))
        +self.joueurs[self.actuel]
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
        return passe

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