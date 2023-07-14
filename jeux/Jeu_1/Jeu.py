from random import choice, randint
from systeme.FondMarin import *
from jeux.Jeu_1.objets.plateau.plateau import Plateau, Case
from jeux.Jeu_1.objets.Joueur import Joueur, Bateau
from jeux.Jeu_1.intro import Intro
from jeux.Jeu_1.pageCarte import PageCarte
from jeux.Jeu_1.objets.bases.fenetre import Fenetre
from jeux.Jeu_1.objets.plateau.zone import Zone
from jeux.Jeu_1.config import config, joueurs as lijo
from jeux.Jeu_1.ui.tiroir import Tiroir
from jeux.Jeu_1.ui.selecBat import SelecBat
from jeux.Jeu_1.ui.editTeleco import Cible, EditTeleco
from jeux.Jeu_1.action.Placement import Placement
from jeux.Jeu_1.ui.fleche import Fleche
from jeux.Jeu_1.ui.barreAction import BarreAction
from jeux.Jeu_1.orgaFen import OrgaFen
from jeux.Jeu_1.recompense.recompFen import RecompFen
from jeux.Jeu_1.fenFin.fin import Fin
from museeNoyee import orga, miniorga, abordage, miniabordage

TOURMAX = 40

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
        self.fen = {"intro": Intro(self.joueurs), 
                    "choix_zone": PageCarte(), 
                    "install": self.plateau, 
                    "jeu": self.plateau, 
                    "organisation": OrgaFen(self.joueurs[self.actuel][0], self.joueurs[self.actuel][1]), 
                    "fin": Fin(self.joueurs), 
                    "recomp_abo": RecompFen()}
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
        # Partie
        self.barre = BarreAction(self.joueurs, self.passe)
        self.fleche = Fleche(self.plateau[0][0], self.joueurs[0][0], self.zone, self.plateau)
        self.setDeplacement = False
        self.indiqueTour = 0
        # Abordage
        self.caseAbordage = None
        self.recompAbordage = False
        self.vainqueur = None
        # Between the world
        self.play = False

    def dessine(self) -> None:
        fenetre = self.fen[self.actif]
        fenetre.dessine()
        if self.actif != 'organisation':
            if isinstance(fenetre, Fenetre) and fenetre.estFini():
                self.switch()
            if self.phase == 'installation':
                self.installation()
                if config['dev'] == 'jeu':
                    self.passePhase()
            elif self.phase == 'jeu':
                self.joueurs[self.actuel].dessine()
                self.tourJoueur()

    def switch(self) -> None:
        if self.actif == 'intro':
            self.actif = 'choix_zone'
            self.setPhase('installation')
        elif self.actif == 'choix_zone':
            self.actif = 'install'
        elif self.actif == 'install':
            self.actif = 'jeu'
            self.setPhase('jeu')
        elif self.actif == 'jeu':
            self.actif = 'fin'
            self.phase = 'fin'
            self.fen[self.actif].setJoueurs(self.joueurs)

    def rejouer(self) -> None:
        for fenetre in self.fen:
            if isinstance(self.fen[fenetre], Fenetre):
                self.fen[fenetre].rejouer()
        self.actif = self.phase = 'intro'
        self.plateau.bloque = True
        self.plateau.vide()
        self.indiqueTour = 0
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
        elif self.phase == 'jeu':
            self.switch()

    def passeTour(self) -> None:
        j = self.actuel
        if self.phase == 'installation':
            while self.actuel == j:
                self.passeAction()
                if isinstance(self.fen[self.actif], Fenetre) and self.fen[self.actif].estFini():
                    self.switch()
                    self.zone.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
        elif self.phase == 'jeu':
            joueur = self.joueurs[self.actuel]
            for i in range(len(joueur)-joueur.actuel):
                self.passeAction()
                self.setParamFleche()

    def passeAction(self) -> None:
        if isinstance(self.fen[self.actif], Fenetre):
            fenetre = self.fen[self.actif]
            if fenetre.action != None:
                fenetre.action.passe()
        elif self.phase == "installation":
            self.passeInstall()
        elif self.phase == "jeu":
            liChoix = [self.passe] + [self.fleche.passe]*99
            choix = choice(liChoix)
            choix()
            # organisation et abordage
            c = self.trouveCase(self.joueurs[self.actuel][self.joueurs[self.actuel].actuel])
            case = self.plateau[c[0]][c[1]]
            idbat = case.contenu.index(self.joueurs[self.actuel][self.joueurs[self.actuel].actuel])
            # Organisation
            if choix == self.fleche.passe and len(case) > 1 and case[len(case)-1-idbat] in self.joueurs[self.actuel]:
                nbMarins = case[len(case)-1-idbat].marins
                nbRedistrib = randint(1, nbMarins)
                self.joueurs[self.actuel][self.joueurs[self.actuel].actuel] + nbRedistrib
                case[len(case)-1-idbat] - nbRedistrib
            # Abordage
            elif choix == self.fleche.passe and len(case) > 1 and case[len(case)-1-idbat] not in self.joueurs[self.actuel]:
                self.abordage(case[0], case[1])
            # /
            if choix != self.passe:
                self.passe()

    def passe(self) -> None:
        self.joueurs[self.actuel].bateauSuivant()
        self.deplaceInstall = self.setDeplacement = False
        if not self.joueurs[self.actuel].actif:
            self.joueurSuivant()

    # Placement

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
            self.plateau.grise = self.setDeplacement = False
            self.zone.setCouleurs([82, 211, 164, 140], [222, 255, 243, 255], [82, 211, 164, 140], [222, 255, 243, 255])
            self.plateau - self.zone
            # important
            bat = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
            ncase = self.trouveCase(bat)
            case = self.plateau[ncase[0]][ncase[1]]
            self.fleche.setBateau(bat)
            self.fleche.setCase(case)

    def joueurSuivant(self) -> None:
        if self.joueurs[self.actuel].compteBateau() == 0:
            self.switch()
        else:
            -self.joueurs[self.actuel]
            self.joueurs[self.actuel].actuel = 0
            self.actuel += 1
            if self.actuel >= len(self.joueurs):
                self.actuel = 0
                if self.phase != "jeu":
                    self.switch()
            +self.joueurs[self.actuel]
            if self.phase == 'installation':
                self.resetInstall()
            elif self.phase == 'jeu':
                self.deplaceInstall = self.setDeplacement = False
                if self.actuel == 0:
                    if self.indiqueTour < TOURMAX:
                        self.indiqueTour += 1
                    else:
                        self.switch()

    # Partie

    def tourJoueur(self) -> None:
        if not self.setDeplacement:
            self.setParamFleche()
        elif not self.barre.deplacement:
            if self.barre.btDep.getContact():
                self.plateau + self.zone
            else:
                self.plateau - self.zone
        else:
            if self.barre.choixAction:
                self.plateau + self.zone
                self.barre.choixAction = False
            self.fleche.dessine()
            self.dessineMarqueur()
            if self.barre.orga:
                if self.play:
                    self.play = False
                orga = self.fen["organisation"]
                orga.dessine()
                if not orga.ok and orga.valide == 1 and not orga.playAnim:
                    orga.playAnim = True
                if orga.valide != 1 and not orga.playAnim:
                    self.barre.orga = False
                    if orga.valide == 2:
                        self.barre.valide = True
                    orga.valide = 1
                    self.play = True
            # Abordage
            if self.barre.abordage:
                case = self.caseAbordage
                recomp = self.fen["recomp_abo"]
                if not self.recompAbordage:
                    self.vainqueur = self.abordage(case[0], case[1])
                    if self.vainqueur > -1:
                        self.recompAbordage = True
                        recomp.setBateaux(case[0], case[1])
                    else:
                        self.barre.abordage = False
                        self.barre.valide = True
                else:
                    if self.play:
                        self.play = False
                    if case[0] in self.joueurs[self.vainqueur]:
                        bat = case[0]
                        op = case[1]
                    else:
                        bat = case[1]
                        op = case[0]
                    if bat in self.joueurs[0]:
                        j1 = self.joueurs[0]
                        j2 = self.joueurs[1]
                    else:
                        j1 = self.joueurs[1]
                        j2 = self.joueurs[0]
                    recomp.dessine()
                    if recomp.valide != -1 and not recomp.playAnim:
                        if recomp.valide == 1:
                            op - 1
                            bat + 1
                        elif recomp.valide == 2:
                            j1 + op
                            j2 - op
                        elif recomp.valide == 3:
                            if bat.marins > op.marins:
                                dif = bat.marins-op.marins
                            else:
                                dif = op.marins-bat.marins
                            if dif-1 > 0:
                                op.setNbPV(op.vie-(dif-1))
                        self.barre.abordage = False
                        self.barre.valide = True
                        recomp.valide = -1
                        recomp.playAnim = True
                        self.play = True
            if self.barre.valide:
                self.barre.deplacement = self.barre.valide = False
                self.passe()
            elif self.barre.annule:
                self.barre.deplacement = self.barre.annule = False
                self.fleche.reset()

    def dessineMarqueur(self) -> None:
        bateau = self.fleche.bateau
        ptBtOrga = 0
        ptBtAbordage = 0
        for i in range(len(self.zone)):
            c = self.zone[i]
            case = self.plateau[c[0]][c[1]]
            if len(case) == 1 and case[0] != bateau:
                if case[0] in self.joueurs[self.actuel]:
                    draw_texture(miniorga, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                else:
                    draw_texture(miniabordage, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
            elif len(case) == 2 and bateau in case:
                if case[0] in self.joueurs[self.actuel]:
                    draw_texture(orga, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                    ptBtOrga += 1
                else:
                    draw_texture(abordage, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                    ptBtAbordage += 1
                    self.caseAbordage = case
                if self.fen["organisation"].bat[0] != case[0] or self.fen["organisation"].bat[1] != case[1]:
                    self.fen["organisation"].setBateaux(case[0], case[1])
        if ptBtOrga > 0:
            self.barre.actionsPossibles["organisation"] = True
        else:
            self.barre.actionsPossibles["organisation"] = False
        if ptBtAbordage > 0:
            self.barre.actionsPossibles["abordage"] = True
        else:
            self.barre.actionsPossibles["abordage"] = False

    def abordage(self, bat1: Bateau, bat2: Bateau) -> int:
        vainqueur = -1
        if bat1.marins > bat2.marins:
            bat2.setNbPV(bat2.vie-1)
            vainqueur = 0
        elif bat2.marins > bat1.marins:
            bat1.setNbPV(bat1.vie-1)
            vainqueur = 1
        else:
            bat1.setNbPV(bat1.vie-1)
            bat2.setNbPV(bat2.vie-1)
        if bat1.coule:
            self.caseAbordage - bat1
        if bat2.coule:
            self.caseAbordage - bat2
        return vainqueur

    def setParamFleche(self) -> None:
        bat = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        if bat.pm > 0:
            ncase = self.trouveCase(bat)
            if not isinstance(ncase, bool):
                case = self.plateau[ncase[0]][ncase[1]]
                self.zone.cases = []
                self.setZonePortee(bat, case, 1)
                if len(self.zone) == 0:
                    self.barre.actionsPossibles["deplacement"] = False
                else:
                    self.barre.actionsPossibles["deplacement"] = True
                self.fleche.setBateau(bat)
                self.fleche.setCase(case)
                self.setDeplacement = True

    def setZonePortee(self, bateau: Bateau, case: Case, progression: int) -> None:
        voisines = self.plateau.getVoisines(case)
        pointsCardinaux = ['e', 's', 'o', 'n']
        if progression == 1:
            devant = voisines[pointsCardinaux[bateau.direction]]
            gauche = voisines[pointsCardinaux[(bateau.direction-1)%len(pointsCardinaux)]]
            droite = voisines[pointsCardinaux[(bateau.direction+1)%len(pointsCardinaux)]]
            if devant and not self.plateau[devant[0]][devant[1]].estPleine():
                self.zone.cases.append(devant)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[devant[0]][devant[1]], progression+1)
            if gauche and not self.plateau[gauche[0]][gauche[1]].estPleine():
                self.zone.cases.append(gauche)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[gauche[0]][gauche[1]], progression+1)
            if droite and not self.plateau[droite[0]][droite[1]].estPleine():
                self.zone.cases.append(droite)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[droite[0]][droite[1]], progression+1)
        else:
            for i in range(len(pointsCardinaux)):
                if voisines[pointsCardinaux[i]] and not voisines[pointsCardinaux[i]] in self.zone.cases:
                    ncase = self.plateau[voisines[pointsCardinaux[i]][0]][voisines[pointsCardinaux[i]][1]]
                    if not ncase.estPleine():
                        casebat = self.trouveCase(bateau)
                        if voisines[pointsCardinaux[i]] != casebat:
                            self.zone.cases.append(voisines[pointsCardinaux[i]])
                            if progression < bateau.pm:
                                self.setZonePortee(bateau, ncase, progression+1)

    def trouveCase(self, bateau) -> tuple|bool:
        trouve = False
        i = 0
        while i < len(self.plateau) and not trouve:
            j = 0
            while j < len(self.plateau[i]) and not trouve:
                if self.plateau[i][j].contient(bateau):
                    trouve = True
                else:
                    j += 1
            if not trouve:
                i += 1
        if trouve:
            return (i, j)
        else:
            return trouve