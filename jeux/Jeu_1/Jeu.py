from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.plateau import Plateau
from jeux.Jeu_1.objets.Joueur import Joueur
from jeux.Jeu_1.intro import Intro
from jeux.Jeu_1.pageCarte import PageCarte
from jeux.Jeu_1.objets.bases.fenetre import Fenetre
from jeux.Jeu_1.objets.plateau.zone import Zone
from jeux.Jeu_1.config import config, joueurs as lijo
from jeux.Jeu_1.ui.tiroir import Tiroir
from jeux.Jeu_1.ui.selecBat import SelecBat
from jeux.Jeu_1.ui.cible import Cible

class Jeu:
    def __init__(self) -> None:
        self.plateau = Plateau(14)
        self.plateau.bloque = True
        self.joueurs = []
        for joueur in lijo:
            joueur = lijo[joueur]
            self.joueurs.append(Joueur(joueur["nom"], joueur["bateaux"], joueur["couleur"]))
        self.actuel = 0
        +self.joueurs[self.actuel]
        self.tiroir = Tiroir(self.joueurs[self.actuel].bateaux)
        # Phases
        self.fen = {"intro": Intro(self.joueurs), "choix_zone": PageCarte(), "plateau": self.plateau}
        if config['dev']:
            self.actif = config['dev'].lower()
            if self.actif == 'plateau':
                self.fen['choix_zone'].action.passe()
        else:
            self.actif = 'intro'
        self.phase = config[self.actif]["phase"]
        # /
        self.cible = Cible(self.plateau.cases[0][0], self.joueurs[self.actuel][0])
        # Installation
        self.deplaceInstall = False
        self.pause = 100
        self.zone = Zone((0, 0), (0, 0), self.plateau)
        self.zone.setCouleurs([255, 161, 0, 60], ORANGE, [255, 161, 0, 60], ORANGE)
        self.rectangle = SelecBat()
        self.affRec = False

    def dessine(self) -> None:
        fenetre = self.fen[self.actif]
        fenetre.dessine()
        if isinstance(fenetre, Fenetre) and fenetre.estFini():
            self.switch()
        if self.phase == 'installation':
            self.installation()

    def switch(self) -> None:
        if self.actif == 'intro':
            self.actif = 'choix_zone'
            self.setPhase('installation')
        elif self.actif == 'choix_zone':
            self.actif = 'plateau'

    def rejouer(self) -> None:
        for fenetre in self.fen:
            if isinstance(self.fen[fenetre], Fenetre):
                self.fen[fenetre].rejouer()
        self.actif = self.phase = 'intro'
        self.plateau.bloque = True
        self.plateau.vide()
        # Joueurs 
        self.actuel = 0
        for i in range(len(self.joueurs)):
            self.joueurs[i].rejouer()
        # Installation
        self.deplaceInstall = False
        self.pause = 100
        self.tiroir.setListe(self.joueurs[self.actuel].bateaux)
        self.tiroir.allume = True
        self.rectangle.contenu = None
        self.affRec = False
        self.rectangle.disparition()

    def passeAction(self) -> None:
        if isinstance(self.fen[self.actif], Fenetre):
            fenetre = self.fen[self.actif]
            if fenetre.action != None:
                fenetre.action.passe()

    def installation(self) -> None:
        if self.actif == 'plateau':
            if not self.deplaceInstall:
                if self.actuel == 0 and self.zone.cases != self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases:
                    self.zone.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
                    self.plateau.bloque = True
                    self.plateau + self.zone
                    self.plateau.grise = True
                if self.pause > 0:
                    self.pause -= 1
            else:
                if not self.affRec:
                    self.tiroir.dessine()
                    bat = self.tiroir.checkSelect()
                    if bat > -1:
                        self.rectangle.setContenu(self.tiroir[bat])
                        self.cible.setBateau(self.tiroir[bat])
                        self.tiroir.supValListe(bat)
                        self.affRec = True
                        self.tiroir.allume = False
                else:
                    if self.tiroir.lumCadre[0] > 0:
                        self.tiroir.dessine()
                    self.deplaceCible()
                    if self.zone.getContact() and self.cible.play:
                        self.cible.dessine()
                    self.rectangle.dessine()
                    if self.rectangle.annule or self.cible.checkBateauEstPlace():
                        if self.rectangle.annule:
                            self.tiroir.ajValListe(self.rectangle.contenu)
                        self.rectangle.contenu = None
                        self.affRec = False
                        self.rectangle.disparition()
                        self.tiroir.allume = True

    def deplaceCible(self) -> None:
        if self.cible.play:
            bonnePlace = False
            i = 0
            if self.phase != "installation":
                while i < self.plateau.nbCases and not bonnePlace:
                    j = 0
                    while j < self.plateau.nbCases and not bonnePlace:
                        if self.plateau[i][j].getContact():
                            bonnePlace = True
                            if self.cible.case != self.plateau[i][j]:
                                self.cible.setCase(self.plateau[i][j])
                        else:
                            j += 1
                    i += 1
            else:
                while i < len(self.zone.cases) and not bonnePlace:
                    Case = self.plateau[self.zone.cases[i][0]][self.zone.cases[i][1]]
                    if Case.getContact():
                        bonnePlace = True
                        if self.cible.case != Case:
                            self.cible.setCase(Case)
                    else:
                        i += 1

    def setPhase(self, phase: str) -> None:
        self.phase = phase
        for i in range(len(self.joueurs)):
            self.joueurs[i].phase = phase

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