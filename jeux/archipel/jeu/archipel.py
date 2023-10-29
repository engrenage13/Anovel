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
            if case[0] < len(self.contenu["plateau"]) and case[1] < len(self.contenu["plateau"][case[0]]):
                retour = self.contenu["plateau"][case[0]][case[1]]
        return retour
    
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
    
    def check_deplacement_possible(self, bateau: Bateau, destination: tuple[int]) -> bool:
        reponse = False
        depart = bateau.position
        pm = bateau.pm
    
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

    def deplacement(self, bateau: Bateau|int, destination: tuple[int]) -> bool:
        ok = False
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            case_dep = self.contenu["plateau"][bateau.position[0]][bateau.position[1]]
            case_dest = self.trouve_case(destination)
            if type(case_dest) == Case and case_dest.type == TypeCase.MER:
                bateau.position = destination
                case_dep - bateau
                case_dest + bateau
                ok = True
        return ok
    