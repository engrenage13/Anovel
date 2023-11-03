from jeux.archipel.jeu.jeu import Jeu, Phases, Etats
from jeux.archipel.jeu.plateau.plateau import Plateau, TypeCase, Case
from jeux.archipel.jeu.bateau import Bateau
from jeux.archipel.config import bateaux as libat, joueurs as lijo
from jeux.archipel.jeu.joueur import Joueur

class Archipel(Jeu):
    def __init__(self, plateau: tuple[int, float]) -> None:
        self.contenu = {
            "plateau": Plateau(plateau[0], int(plateau[0]*plateau[0]*plateau[1])),
            "bateaux": {
                "set1": self.charge_set_bateaux(),
                "set2": self.charge_set_bateaux(),
            }
        }
        # Variables
        self.manche = 1
        self.manche_max = 20
        self.joueur_actuel = 0
        self.phase = Phases.MISE_EN_PLACE
        self.etat = Etats.EN_ATTENTE

    # Utilitaires

    def trouve_bateau(self, bateau: int) -> Bateau|bool:
        retour = False
        if bateau < len(self.joueurs[self.joueur_actuel]):
            retour = self.joueurs[self.joueur_actuel][bateau]
        return retour
    
    def trouve_joueur(self, bateau: Bateau) -> Joueur|bool:
        retour = False
        if type(bateau) == Bateau:
            i = 0
            while not retour and i < len(self.joueurs):
                if bateau in self.joueurs[i]:
                    retour = self.joueurs[i]
                else:
                    i += 1
        return retour
    
    def trouve_liste_bateaux_et_joueur(self, bateaux: list[Bateau|int]) -> list[tuple[Bateau, Joueur]]|bool:
        retour = False
        liste = []
        i = 0
        ok = True
        while ok and i < len(bateaux):
            bateau = bateaux[i]
            if type(bateau) == int:
                bateau = self.trouve_bateau(bateau)
            if type(bateau) == Bateau:
                joueur = self.trouve_joueur(bateau)
                if type(joueur) == Joueur:
                    liste.append([bateau, joueur])
                else:
                    ok = False
            else:
                ok = False
        if ok and len(liste) == len(bateaux):
            retour = liste
        return retour
    
    def trouve_case(self, case: tuple[int]) -> Case|bool:
        retour = False
        if type(case) == tuple[int] and len(case) >= 2:
            if self.contenu["plateau"].check_case_existe(case):
                retour = self.contenu["plateau"][case[0]][case[1]]
        return retour
    
    def trouve_cases_atteignables(self, bateau: Bateau|int) -> list[tuple[int]]:
        cases_atteignables = []
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            plateau = self.contenu["plateau"]
            cases_adjacentes = [bateau.position]
            pm = 0
            while len(cases_adjacentes > 0):
                cases = []
                for i in range(len(cases_adjacentes)):
                    depart = cases_adjacentes[i]
                    cn = (depart[0], depart[1]-1)
                    ce = (depart[0]+1, depart[1])
                    cs = (depart[0], depart[1]+1)
                    co = (depart[0]-1, depart[1])
                    directions = [ce, cs, co, cn]
                    for j in range(len(directions)):
                        if plateau.check_case_existe(directions[j]):
                            tuile = plateau[directions[j][0]][directions[j][1]]
                            if not tuile.check_case_pleine():
                                cases_atteignables.append(directions[j])
                                if pm < bateau.get_pm():
                                    cases.append(directions[j])
                pm += 1
                cases_adjacentes = cases
        return cases_atteignables
    
    # /utilitaires
    # Vérificateurs

    def check_fin_mise_en_place(self) -> bool:
        fin = True
        i = 0
        while fin and i < len(self.joueurs):
            fin = self.joueurs[i].check_fin_mise_en_place()
            i += 1
        if fin:
            self.etat = Etats.EN_ATTENTE
        return fin
    
    def check_fin_partie(self) -> bool:
        fin = True
        i = 0
        while fin and i < len(self.joueurs):
            fin = self.joueurs[i].check_defaite()
            i += 1
        if fin:
            self.phase = Phases.FIN
        return fin
    
    # /vérificateurs

    def charge_set_bateaux(self) -> list[Bateau]:
        contenuSet = ["gafteur" for i in range(3)] + ["ferpasseur"]
        liste = []
        for i in range(len(contenuSet)):
            ibat = libat[contenuSet[i]]
            liste.append(Bateau(ibat["nom"], ibat["vie"], ibat["marins"], ibat["pm"], ibat["degats"]))
        return liste
    
    def mise_en_place(self) -> None:
        for i in range(len(lijo)):
            joueur = lijo[i]
            self.joueurs.append(Joueur(joueur["nom"], self.contenu["bateaux"][i]))
        self.contenu["plateau"].mise_en_place()
    
    def place_bateau(self, joueur: Joueur|int, bateau: Bateau|int, case: tuple[int]) -> bool:
        ok = False
        ok_joueur = True if type(joueur) == Joueur else False
        if type(joueur) == int:
            joueur = self.joueurs[self.joueurs.index(joueur)]
            ok_joueur = True
        if ok_joueur:
            if type(bateau) == int:
                bateau = self.trouve_bateau(bateau)
            if type(bateau) == Bateau:
                case_plateau = self.trouve_case(case)
                if type(case_plateau) == Case and case_plateau.type == TypeCase.MER:
                    bateau.position = case
                    case_plateau + bateau
                    bateau.est_en_jeu = True
                    ok = True
        return ok
    
    def passe_au_joueur_suivant(self) -> None:
        if not self.check_fin_partie():
            if self.joueur_actuel < len(self.joueurs):
                self.joueur_actuel += 1
            else:
                self.joueur_actuel = 0
                if self.phase == Phases.PARTIE:
                    if self.manche < self.manche_max:
                        self.manche += 1
                    else:
                        self.phase = Phases.FIN
                elif self.phase == Phases.MISE_EN_PLACE:
                    self.phase = Phases.PARTIE

    def fait_mal(self, victime: Bateau, proprietaire: Joueur, degats: int) -> bool:
        coule = False
        if victime in proprietaire.bateaux:
            coule = victime - degats
            if coule:
                proprietaire - victime
        return coule

    def deplacement(self, bateau: Bateau|int, destination: tuple[int], direction: int = None) -> bool:
        ok = False
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            case_dep = self.contenu["plateau"][bateau.position[0]][bateau.position[1]]
            case_dest = self.trouve_case(destination)
            if type(case_dest) == Case and case_dest.type == TypeCase.MER:
                deplacements_possibles = self.trouve_cases_atteignables(bateau)
                if destination in deplacements_possibles:
                    bateau.position = destination
                    case_dep - bateau
                    if type(direction) == int:
                        bateau.direction = direction%4
                    case_dest + bateau
                    ok = True
        return ok
    
    def organisation(self, bateaux: tuple[Bateau], nouvel_agencement: tuple[int]) -> bool:
        ok = False
        if len(bateaux) == len(nouvel_agencement):
            total_actuel = 0
            nouveau_total = 0
            for i in range(len(bateaux)):
                total_actuel += bateaux[i].get_marins()
                nouveau_total += nouvel_agencement[i]
            if total_actuel == nouveau_total:
                for i in range(len(bateaux)):
                    if bateaux[i].marins < nouvel_agencement[i]:
                        bateaux[i].marins + (nouvel_agencement[i]-bateaux[i].marins)
                    elif bateaux[i].marins > nouvel_agencement[i]:
                        bateaux[i].marins + (bateaux[i].marins-nouvel_agencement[i])
                ok = True
        return ok
    
    def abordage(self, bateaux: tuple[Bateau|int]) -> list|bool:
        ok = False
        bats = self.trouve_liste_bateaux_et_joueur(bateaux)
        if type(bats) == list and len(bats) >= 2:
            if bats[0][1] != bats[1][1] and bats[0][0].position == bats[1][0].position:
                # Conditions réspéctées, l'abordage a lieu
                gagnant = None
                recompenses = []
                if bats[0][0].get_marins() == bats[1][0].get_marins():
                    # Egalité
                    self.fait_mal(bats[0][0], bats[0][1], 1)
                    self.fait_mal(bats[1][0], bats[1][1], 1)
                    vainqueur = False
                else:
                    # Cas contraire, il y a un vainqueur
                    vainqueur = True
                    if bats[0][0].get_marins() > bats[1][0].get_marins():
                        gagnant = bats[0]
                        perdant = bats[1]
                        coule = self.fait_mal(bats[1][0], bats[1][1], 1)
                    else:
                        gagnant = bats[1]
                        perdant = bats[0]
                        coule = self.fait_mal(bats[0][0], bats[0][1], 1)
                    if not coule:
                        if perdant[0].get_marins() > 0:
                            recompenses.append(0)
                            if gagnant[0].get_marins() - perdant[0].get_marins() >= 5:
                                recompenses.append(1)
                        else:
                            recompenses.append(2)
                        if gagnant[0].get_marins() - perdant[0].get_marins() - 1 > 0:
                            recompenses.append(3)
                ok = [vainqueur, gagnant, recompenses]
        return ok
