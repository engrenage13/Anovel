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
            pm = 0
            fin = False
            cases_adajencentes = [(bateau.position, bateau.direction)]
            while not fin and pm < bateau.get_pm():
                cases = []
                for i in range(len(cases_adajencentes)):
                    if pm > 0 and cases_adajencentes[i][0] not in cases_atteignables:
                        cases_atteignables.append(cases_adajencentes[i][0])
                    depart = cases_adajencentes[i][0]
                    direction = cases_adajencentes[i][1]
                    choix = [direction, (direction+1)%4, (direction+3)%4]
                    for j in range(len(choix)):
                        if direction == 0:
                            c = (depart[0]+1, depart[1])
                        elif direction == 1:
                            c = (depart[0], depart[1]+1)
                        elif direction == 2:
                            c = (depart[0]-1, depart[1])
                        elif direction == 3:
                            c = (depart[0], depart[1]-1)
                        if plateau.check_case_existe(c):
                            cases.append((c, choix[j]))
                cases_adajencentes = cases
                pm += 1
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
    
    def abordage(self, bateaux: tuple[Bateau|int]) -> bool:
        pass
