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
from jeux.Jeu_1.ui.editTeleco import Cible, EditTeleco
from jeux.Jeu_1.action.Placement import Placement

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
        self.fen = {"intro": Intro(self.joueurs), "choix_zone": PageCarte(), "install": self.plateau, "jeu": self.plateau}
        if config['dev']:
            if config['dev'].lower() == 'jeu':
                self.actif = 'install'
            else:
                self.actif = config['dev'].lower()
            if self.actif != 'intro' or self.actif != 'choix_zone':
                self.fen['choix_zone'].action.passe()
        else:
            self.actif = 'intro'
        self.phase = config[self.actif]["phase"]
        # /
        self.cible = Cible(self.plateau[0][0], self.joueurs[self.actuel][0])
        self.teleco = EditTeleco(self.plateau[0][0], self.joueurs[self.actuel][0])
        # Installation
        self.deplaceInstall = False
        self.pause = 100
        self.zone = Zone((0, 0), (0, 0), self.plateau)
        self.zone.setCouleurs([255, 161, 0, 60], ORANGE, [255, 161, 0, 60], ORANGE)
        self.rectangle = SelecBat()
        self.affRec = False
        self.affTeleco = False

    def dessine(self) -> None:
        fenetre = self.fen[self.actif]
        fenetre.dessine()
        if isinstance(fenetre, Fenetre) and fenetre.estFini():
            self.switch()
        if self.phase == 'installation':
            self.installation()
            if config['dev'] == 'jeu':
                self.passePhase()
        elif self.phase == 'jeu':
            self.joueurs[self.actuel].dessine()

    def switch(self) -> None:
        if self.actif == 'intro':
            self.actif = 'choix_zone'
            self.setPhase('installation')
        elif self.actif == 'choix_zone':
            self.actif = 'install'
        elif self.actif == 'install':
            self.actif = 'jeu'
            self.setPhase('jeu')

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
        +self.joueurs[self.actuel]
        # Installation
        self.resetInstall()

    def resetInstall(self) -> None:
        self.deplaceInstall = self.affRec = self.affTeleco = False
        self.pause = 100
        self.tiroir.setListe(self.joueurs[self.actuel].bateaux)
        self.tiroir.allume = True
        self.rectangle.contenu = None
        self.rectangle.disparition()

    def passePhase(self) -> None:
        if self.phase == 'installation':
            phase = self.phase
            while self.phase == phase:
                self.passeTour()
                if self.actuel == 1 and self.phase == 'installation':
                    self.zone.cases = self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+4)%8].cases

    def passeTour(self) -> None:
        j = self.actuel
        if self.phase == 'installation':
            while self.actuel == j:
                self.passeAction()
                if isinstance(self.fen[self.actif], Fenetre) and self.fen[self.actif].estFini():
                    self.switch()
                    self.zone.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
        elif self.phase == 'jeu':
            self.joueurSuivant()

    def passeAction(self) -> None:
        if isinstance(self.fen[self.actif], Fenetre):
            fenetre = self.fen[self.actif]
            if fenetre.action != None:
                fenetre.action.passe()
        elif self.phase == "installation":
            self.passeInstall()
        elif self.phase == "jeu":
            self.joueurs[self.actuel].bateauSuivant()
            self.deplaceInstall = False
            if not self.joueurs[self.actuel].actif:
                self.joueurSuivant()

    def passeInstall(self) -> None:
        cases = []
        for i in range(len(self.zone.cases)):
            tuile = self.plateau[self.zone[i][0]][self.zone[i][1]]
            if not tuile.estPleine():
                cases.append(tuile)
        if not self.affRec:
            placement = Placement(self.tiroir.liste, cases)
        else:
            placement = Placement([self.rectangle.contenu], cases)
        placement.passe()
        if not self.affRec:
            bateau = self.tiroir[placement.resultat[0]]
        else:
            bateau = self.rectangle.contenu
        Case = cases[placement.resultat[1]]
        self.tiroir.supValListe(placement.resultat[0])
        self.affTeleco = self.affRec = False
        for i in range(placement.resultat[2]-bateau.direction):
            bateau.droite()
        Case.ajoute(bateau)
        if len(self.tiroir) == 0:
            self.joueurSuivant()

    def installation(self) -> None:
        if self.actif == 'install':
            if not self.deplaceInstall:
                if self.actuel == 0 and self.zone.cases != self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases:
                    self.zone.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
                    self.setPlateauInstall()
                elif self.actuel == 1 and self.zone.cases != self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+4)%8].cases:
                    self.zone.cases = self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+4)%8].cases
                    self.setPlateauInstall()
                if self.pause > 0:
                    self.pause -= 1
            else:
                if not self.affRec and not self.affTeleco:
                    self.tiroir.dessine()
                    bat = self.tiroir.checkSelect()
                    if bat > -1:
                        self.rectangle.setContenu(self.tiroir[bat])
                        self.cible.setBateau(self.tiroir[bat])
                        self.tiroir.supValListe(bat)
                        self.affRec = True
                        self.tiroir.allume = False
                    else:
                        if self.tiroir.play:
                            self.verifEditPlacement()
                elif self.affRec and not self.affTeleco:
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
                elif not self.affRec and self.affTeleco:
                    self.teleco.dessine()
                    if self.teleco.fini:
                        self.affTeleco = self.affRec = False
                    if self.teleco.retire:
                        self.tiroir.ajValListe(self.teleco.bateau)
                        self.teleco.case.retire(self.teleco.bateau)
                    if self.teleco.veutBouger:
                        voisines = self.plateau.getVoisines(self.teleco.case)
                        ncase = self.plateau[voisines[self.teleco.veutBouger][0]][voisines[self.teleco.veutBouger][1]]
                        ncase.ajoute(self.teleco.bateau)
                        self.teleco.case.retire(self.teleco.bateau)
                        self.teleco.setCase(ncase)
                        self.setFleches(ncase)

    def setPlateauInstall(self) -> None:
        self.plateau.bloque = True
        self.plateau + self.zone
        self.plateau.grise = True

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
                while i < len(self.zone) and not bonnePlace:
                    Case = self.plateau[self.zone[i][0]][self.zone[i][1]]
                    if Case.getContact():
                        bonnePlace = True
                        if self.cible.case != Case:
                            self.cible.setCase(Case)
                    else:
                        i += 1

    def verifEditPlacement(self) -> None:
        if is_mouse_button_pressed(0):
            trouve = False
            i = 0
            while i < len(self.zone) and not trouve:
                Case = self.plateau[self.zone[i][0]][self.zone[i][1]]
                if Case.getContact() and not Case.estVide():
                    trouve = True
                    indice = 0
                    if len(Case) > 1:
                        j = 0
                        bat = False
                        while j < len(Case) and not bat:
                            if Case[j].getContact():
                                bat = True
                                indice = j
                            else:
                                j += 1
                    self.teleco.setCase(Case)
                    self.teleco.setBateau(Case[indice])
                    self.setFleches(Case)
                    self.affTeleco = True
                else:
                    i += 1

    def setFleches(self, case) -> None:
        voisines = self.plateau.getVoisines(case)
        li1 = ["n", "e", "s", "o"]
        li2 = ["nord", "est", "sud", "ouest"]
        for i in range(len(li1)):
            if voisines[li1[i]] and voisines[li1[i]] in self.zone.cases:
                if not self.plateau[voisines[li1[i]][0]][voisines[li1[i]][1]].estPleine():
                    self.teleco.activeDep[li2[i]] = True
                else:
                    self.teleco.activeDep[li2[i]] = False
            else:
                self.teleco.activeDep[li2[i]] = False

    def setPhase(self, phase: str) -> None:
        self.phase = phase
        for i in range(len(self.joueurs)):
            self.joueurs[i].phase = phase
        if self.phase == 'jeu':
            self.plateau - self.zone
            self.plateau.grise = False

    def joueurSuivant(self) -> None:
        -self.joueurs[self.actuel]
        self.joueurs[self.actuel].actuel = 0
        self.actuel += 1
        if self.actuel >= len(self.joueurs):
            self.actuel = 0
            self.switch()
        +self.joueurs[self.actuel]
        if self.phase == 'installation':
            self.resetInstall()
        elif self.phase == 'jeu':
            self.deplaceInstall = False
