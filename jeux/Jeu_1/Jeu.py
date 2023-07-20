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
        self.tiroir = Tiroir(self.joueurs[self.actuel].bateaux, self.joueurs[self.actuel].couleur)
        # Phases
        self.fen = {"intro": Intro(self.joueurs), 
                    "choix_zone": PageCarte(), 
                    "placement": self.plateau, 
                    "jeu": self.plateau, 
                    "organisation": OrgaFen(self.joueurs[self.actuel][0], self.joueurs[self.actuel][1]), 
                    "fin": Fin(self.joueurs), 
                    "recomp_abo": RecompFen()}
        if config['dev']:
            if config['dev'].lower() == 'jeu':
                self.actif = 'placement'
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
        # Placement
        self.deplaPlacement = False
        self.pause = 100
        self.zoneDep = Zone((0, 0), (0, 0), self.plateau)
        self.zoneDep.setCouleurs([255, 161, 0, 60], ORANGE, [255, 161, 0, 60], ORANGE)
        self.zoneAt = Zone((0, 0), (0, 0), self.plateau)
        self.zoneAt.setCouleurs([255, 0, 0, 60], RED, [255, 0, 0, 60], RED)
        self.rectangle = SelecBat()
        self.affRec = False
        self.affTeleco = False
        # Partie
        self.barre = BarreAction(self.joueurs, self.passe)
        self.fleche = Fleche(self.plateau[0][0], self.joueurs[0][0], self.zoneDep, self.plateau)
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
            if self.phase == 'placement':
                self.placement()
                if config['dev'] == 'jeu':
                    self.passePhase()
            elif self.phase == 'jeu':
                self.joueurs[self.actuel].dessine()
                self.tourJoueur()

    def switch(self) -> None:
        if self.actif == 'intro':
            self.actif = 'choix_zone'
            self.setPhase('placement')
        elif self.actif == 'choix_zone':
            self.actif = 'placement'
        elif self.actif == 'placement':
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
        # Placement
        self.resetPlacement()

    def resetPlacement(self) -> None:
        self.deplaPlacement = self.affRec = self.affTeleco = False
        self.pause = 100
        self.tiroir.setListe(self.joueurs[self.actuel].bateaux)
        self.tiroir.couleur = self.joueurs[self.actuel].couleur
        self.tiroir.allume = True
        self.rectangle.contenu = None
        self.rectangle.disparition()

    def passePhase(self) -> None:
        if self.phase == 'placement':
            phase = self.phase
            while self.phase == phase:
                self.passeTour()
                if self.actuel == 1 and self.phase == 'placement':
                    self.zoneDep.cases = self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+int(len(self.fen['choix_zone'].zones)/1))%len(self.fen['choix_zone'].zones)].cases
        elif self.phase == 'jeu':
            self.switch()

    def passeTour(self) -> None:
        j = self.actuel
        if self.phase == 'placement':
            while self.actuel == j:
                self.passeAction()
                if isinstance(self.fen[self.actif], Fenetre) and self.fen[self.actif].estFini():
                    self.switch()
                    self.zoneDep.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
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
        elif self.phase == "placement":
            self.passePlacement()
        elif self.phase == "jeu":
            liChoix = [self.passe] + [self.fleche.passe]*80 + [self.attaPasse]*19
            choix = choice(liChoix)
            choix()
            # organisation et abordage
            c = self.trouveCase(self.joueurs[self.actuel][self.joueurs[self.actuel].actuel])
            if not isinstance(c, bool):
                case = self.plateau[c[0]][c[1]]
                self.caseAbordage = case
                idbat = case.contenu.index(self.joueurs[self.actuel][self.joueurs[self.actuel].actuel])
                # Organisation
                if choix == self.fleche.passe and len(case) > 1 and case[len(case)-1-idbat] in self.joueurs[self.actuel].bateaux:
                    nbMarins = case[len(case)-1-idbat].marins
                    nbRedistrib = randint(1, nbMarins)
                    self.joueurs[self.actuel][self.joueurs[self.actuel].actuel] + nbRedistrib
                    case[len(case)-1-idbat] - nbRedistrib
                # Abordage
                elif choix == self.fleche.passe and len(case) > 1 and case[len(case)-1-idbat] not in self.joueurs[self.actuel].bateaux:
                    vainqueur = self.abordage(case[0], case[1])
                    if vainqueur > -1:
                        actions = []
                        if vainqueur == 0:
                            bat = case[0]
                            op = case[1]
                        else:
                            bat = case[1]
                            op = case[0]
                        if bat in self.joueurs[0].bateaux:
                            j1 = self.joueurs[0]
                            j2 = self.joueurs[1]
                        else:
                            j1 = self.joueurs[1]
                            j2 = self.joueurs[0]
                        if op.marins > 0:
                            actions.append(1)
                            if bat.marins-op.marins >= 5:
                                actions.append(2)
                        else:
                            actions.append(2)
                        if bat.marins > op.marins and bat.marins-op.marins-1 > 0:
                            actions.append(3)
                        elif op.marins > bat.marins and op.marins-bat.marins-1 > 0:
                            actions.append(3)
                        cx = choice(actions)
                        if cx == 1:
                            op - 1
                            bat + 1
                        elif cx == 2:
                            j1 + op
                            j2 - op
                        elif cx == 3:
                            if bat.marins > op.marins:
                                dif = bat.marins-op.marins
                            else:
                                dif = op.marins-bat.marins
                            if dif-1 > 0:
                                op.setNbPV(op.vie-(dif-1))
                                if op.coule:
                                    case - op
                                    j1.nbelimination += 1
            # /
            if choix != self.passe:
                self.passe()

    def attaPasse(self) -> None:
        attaquant = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        if self.verifAttaquePossible():
            stop = False
            cases = [j for j in range(len(self.zoneAt))]
            while not stop and len(cases) > 0:
                i = choice(cases)
                del cases[cases.index(i)]
                c = self.zoneAt[i]
                Case = self.plateau[c[0]][c[1]]
                if len(Case) > 0:
                    if len(Case) == 1 and Case[0] != attaquant:
                        cible = Case[0]
                    elif len(Case) == 2:
                        if attaquant not in Case.contenu:
                            aleat = randint(0, 1)
                            cible = Case[aleat]
                        else:
                            pos = Case.contenu.index(attaquant)
                            cible = Case[len(Case)-1-pos]
                    else:
                        cible = None
                    if isinstance(cible, Bateau):
                        cible.setNbPV(cible.vie-attaquant.degats)
                        stop = True
                        if cible.coule:
                            Case - cible
                            self.joueurs[self.actuel].nbelimination += 1
                            if cible in self.joueurs[0].bateaux:
                                self.joueurs[0] - cible
                            else:
                                self.joueurs[1] - cible

    def passe(self) -> None:
        self.joueurs[self.actuel].bateauSuivant()
        self.deplaPlacement = self.setDeplacement = False
        if not self.joueurs[self.actuel].actif:
            self.joueurSuivant()

    # Placement

    def passePlacement(self) -> None:
        cases = []
        for i in range(len(self.zoneDep.cases)):
            tuile = self.plateau[self.zoneDep[i][0]][self.zoneDep[i][1]]
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

    def placement(self) -> None:
        if self.actif == 'placement':
            if not self.deplaPlacement:
                if self.actuel == 0 and self.zoneDep.cases != self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases:
                    self.zoneDep.cases = self.fen['choix_zone'].zones[self.fen['choix_zone'].action.resultat].cases
                    self.setPlateauPlacer()
                elif self.actuel == 1 and self.zoneDep.cases != self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+int(len(self.fen['choix_zone'].zones)/1))%len(self.fen['choix_zone'].zones)].cases:
                    self.zoneDep.cases = self.fen['choix_zone'].zones[(self.fen['choix_zone'].action.resultat+int(len(self.fen['choix_zone'].zones)/1))%len(self.fen['choix_zone'].zones)].cases
                    self.setPlateauPlacer()
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
                    if self.zoneDep.getContact() and self.cible.play:
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

    def setPlateauPlacer(self) -> None:
        self.plateau.bloque = True
        self.plateau + self.zoneDep
        self.plateau.grise = True

    def deplaceCible(self) -> None:
        if self.cible.play:
            bonnePlace = False
            i = 0
            if self.phase != "placement":
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
                while i < len(self.zoneDep) and not bonnePlace:
                    Case = self.plateau[self.zoneDep[i][0]][self.zoneDep[i][1]]
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
            while i < len(self.zoneDep) and not trouve:
                Case = self.plateau[self.zoneDep[i][0]][self.zoneDep[i][1]]
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
            if voisines[li1[i]] and voisines[li1[i]] in self.zoneDep.cases:
                if not self.plateau[voisines[li1[i]][0]][voisines[li1[i]][1]].estPleine():
                    self.teleco.activeDep[li2[i]] = True
                else:
                    self.teleco.activeDep[li2[i]] = False
            else:
                self.teleco.activeDep[li2[i]] = False

    def setPhase(self, phase: str) -> None:
        self.phase = phase
        for i in range(len(self.joueurs)):
            self.joueurs[i].setPhase(phase)
        if self.phase == 'jeu':
            self.plateau.grise = self.setDeplacement = False
            self.zoneDep.setCouleurs([82, 211, 164, 140], [222, 255, 243, 255], [82, 211, 164, 140], [222, 255, 243, 255])
            self.plateau - self.zoneDep
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
            if self.phase == 'placement':
                self.resetPlacement()
            elif self.phase == 'jeu':
                self.deplaPlacement = self.setDeplacement = False
                if self.actuel == 0:
                    if self.indiqueTour < TOURMAX:
                        self.indiqueTour += 1
                    else:
                        self.switch()

    # Partie

    def tourJoueur(self) -> None:
        if not self.setDeplacement:
            self.setParamFleche()
        elif not self.barre.deplacement and not self.barre.attaque:
            if self.barre.btDep.getContact():
                self.plateau + self.zoneDep
            else:
                self.plateau - self.zoneDep
            if self.barre.btAt.getContact():
                self.plateau + self.zoneAt
            else:
                self.plateau - self.zoneAt
        else:
            if self.barre.choixAction:
                if self.barre.deplacement:
                    self.plateau + self.zoneDep
                elif self.barre.attaque:
                    self.plateau + self.zoneAt
                self.barre.choixAction = False
            if self.barre.deplacement:
                self.fleche.dessine()
                self.dessineMarqueur()
            # Organisation
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
                        if len(case) > 1:
                            if self.vainqueur == 0:
                                recomp.setBateaux(case[0], case[1])
                            else:
                                recomp.setBateaux(case[1], case[0])
                    else:
                        self.barre.abordage = False
                        self.barre.valide = True
                else:
                    if self.play:
                        self.play = False
                    if len(case) > 1:
                        if self.vainqueur == 0:
                            bat = case[0]
                            op = case[1]
                        else:
                            bat = case[1]
                            op = case[0]
                        if bat in self.joueurs[0].bateaux:
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
                                    if op.coule:
                                        self.caseAbordage - op
                                        j1.nbelimination += 1
                            self.barre.abordage = False
                            self.barre.valide = True
                            self.recompAbordage = False
                            recomp.valide = -1
                            self.play = True
                            if j2.compteBateau() == 0:
                                self.switch()
            if self.barre.attaque:
                if self.zoneAt.getContact() and is_mouse_button_pressed(0):
                    self.attaque()
            if self.barre.valide:
                self.barre.deplacement = self.barre.attaque = self.barre.valide = False
                self.passe()
            elif self.barre.annule:
                self.barre.deplacement = self.barre.attaque = self.barre.annule = False
                self.fleche.reset()

    def dessineMarqueur(self) -> None:
        bateau = self.fleche.bateau
        ptBtOrga = 0
        ptBtAbordage = 0
        for i in range(len(self.zoneDep)):
            c = self.zoneDep[i]
            case = self.plateau[c[0]][c[1]]
            if len(case) == 1 and case[0] != bateau:
                if case[0] in self.joueurs[self.actuel].bateaux:
                    draw_texture(miniorga, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                else:
                    draw_texture(miniabordage, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
            elif len(case) == 2 and bateau in case:
                if case[0] in self.joueurs[self.actuel].bateaux:
                    draw_texture(orga, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                    ptBtOrga += 1
                else:
                    draw_texture(abordage, int(case.pos[0]+case.taille*0.02), int(case.pos[1]+case.taille*0.02), WHITE)
                    ptBtAbordage += 1
                    if len(case) == 2:
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
            vainqueur = -1
            self.caseAbordage - bat1
            if bat1 in self.joueurs[0].bateaux:
                self.joueurs[1].nbelimination += 1
                self.joueurs[0] - bat1
                if self.joueurs[0].compteBateau() == 0:
                    self.switch()
            else:
                self.joueurs[0].nbelimination += 1
                self.joueurs[1] - bat1
                if self.joueurs[1].compteBateau() == 0:
                    self.switch()
        if bat2.coule:
            vainqueur = -1
            self.caseAbordage - bat2
            if bat2 in self.joueurs[0].bateaux:
                self.joueurs[1].nbelimination += 1
                self.joueurs[0] - bat2
                if self.joueurs[0].compteBateau() == 0:
                    self.switch()
            else:
                self.joueurs[0].nbelimination += 1
                self.joueurs[1] - bat2
                if self.joueurs[1].compteBateau() == 0:
                    self.switch()
        return vainqueur
    
    def attaque(self) -> None:
        origine = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        victime = None
        i = 0
        fini = False
        while i < len(self.zoneAt) and not fini:
            Case = self.plateau[self.zoneAt[i][0]][self.zoneAt[i][1]]
            if Case.getContact():
                if len(Case) == 1 and Case[0] != origine:
                    Case[0].setNbPV(Case[0].vie-origine.degats)
                    victime = Case[0]
                elif len(Case) > 1:
                    if origine not in Case:
                        j = 0
                        trouve = False
                        while j < len(Case) and not trouve:
                            if Case[j].getContact():
                                Case[j].setNbPV(Case[j].vie-origine.degats)
                                victime = Case[j]
                                trouve = True
                            else:
                                j += 1
                    else:
                        place = Case.contenu.index(origine)
                        Case[len(Case)-1-place].setNbPV(Case[len(Case)-1-place].vie-origine.degats)
                        victime = Case[len(Case)-1-place]
                fini = True
            else:
                i += 1
        if victime != None:
            self.barre.valide = True
            if victime.coule:
                Case - victime
                self.joueurs[self.actuel].nbelimination += 1
                if victime.couleur == self.joueurs[0].couleur:
                    self.joueurs[0] - victime
                    if self.joueurs[0].compteBateau() == 0:
                        self.switch()
                else:
                    self.joueurs[1] - victime
                    if self.joueurs[1].compteBateau() == 0:
                        self.switch()

    def setParamFleche(self) -> None:
        bat = self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]
        if bat.pm > 0:
            ncase = self.trouveCase(bat)
            if not isinstance(ncase, bool):
                case = self.plateau[ncase[0]][ncase[1]]
                self.zoneDep.cases = []
                self.setZonePortee(bat, case, 1)
                self.setZoneAttaque(case, ncase)
                if len(self.zoneDep) == 0:
                    self.barre.actionsPossibles["deplacement"] = False
                else:
                    self.barre.actionsPossibles["deplacement"] = True
                self.barre.actionsPossibles["attaque"] = self.verifAttaquePossible()
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
                self.zoneDep.cases.append(devant)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[devant[0]][devant[1]], progression+1)
            if gauche and not self.plateau[gauche[0]][gauche[1]].estPleine():
                self.zoneDep.cases.append(gauche)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[gauche[0]][gauche[1]], progression+1)
            if droite and not self.plateau[droite[0]][droite[1]].estPleine():
                self.zoneDep.cases.append(droite)
                if progression < bateau.pm:
                    self.setZonePortee(bateau, self.plateau[droite[0]][droite[1]], progression+1)
        else:
            for i in range(len(pointsCardinaux)):
                if voisines[pointsCardinaux[i]] and not voisines[pointsCardinaux[i]] in self.zoneDep.cases:
                    ncase = self.plateau[voisines[pointsCardinaux[i]][0]][voisines[pointsCardinaux[i]][1]]
                    if not ncase.estPleine():
                        casebat = self.trouveCase(bateau)
                        if voisines[pointsCardinaux[i]] != casebat:
                            self.zoneDep.cases.append(voisines[pointsCardinaux[i]])
                            if progression < bateau.pm:
                                self.setZonePortee(bateau, ncase, progression+1)

    def setZoneAttaque(self, centre: Case, equiv: tuple) -> None:
        self.zoneAt.cases = []
        self.zoneAt.cases.append(equiv)
        voisines = self.plateau.getVoisines(centre)
        if not isinstance(voisines['n'], bool):
            haut = self.plateau[voisines['n'][0]][voisines['n'][1]]
            self.zoneAt.cases.append(voisines['n'])
            vois = self.plateau.getVoisines(haut)
            if not isinstance(voisines['o'], bool):
                self.zoneAt.cases.append(vois['o'])
                self.zoneAt.cases.append(voisines['o'])
            if not isinstance(voisines['e'], bool):
                self.zoneAt.cases.append(vois['e'])
                self.zoneAt.cases.append(voisines['e'])
        if not isinstance(voisines['s'], bool):
            bas = self.plateau[voisines['s'][0]][voisines['s'][1]]
            self.zoneAt.cases.append(voisines['s'])
            vois = self.plateau.getVoisines(bas)
            if not isinstance(voisines['o'], bool):
                self.zoneAt.cases.append(vois['o'])
                if voisines['o'] not in self.zoneAt.cases:
                    self.zoneAt.cases.append(voisines['o'])
            if not isinstance(voisines['e'], bool):
                self.zoneAt.cases.append(vois['e'])
                if voisines['e'] not in self.zoneAt.cases:
                    self.zoneAt.cases.append(voisines['e'])

    def verifAttaquePossible(self) -> bool:
        stop = False
        i = 0
        while i < len(self.zoneAt) and not stop:
            c = self.zoneAt.cases[i]
            Case = self.plateau[c[0]][c[1]]
            if len(Case) == 1 and Case[0] != self.joueurs[self.actuel][self.joueurs[self.actuel].actuel]:
                stop = True
            elif len(Case) == 2 and self.joueurs[self.actuel][self.joueurs[self.actuel].actuel] not in Case.contenu:
                stop = True
            else:
                i += 1
        return stop

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