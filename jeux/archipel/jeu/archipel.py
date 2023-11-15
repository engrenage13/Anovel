from jeux.archipel.jeu.jeu import Jeu, Phases, Etats
from jeux.archipel.jeu.plateau.plateau import Plateau, TypeCase, Case
from jeux.archipel.jeu.bateau import Bateau
from jeux.archipel.config import bateaux as libat, joueurs as lijo
from jeux.archipel.jeu.joueur import Joueur
from jeux.archipel.jeu.actions import vole_marin, vole_bateau, inflige_dommage

recompenses = [("Voler 1 marin", vole_marin), 
               ("Voler le bateau et son equipage", vole_bateau),
               ("Voler le bateau", vole_bateau),
               ("Infliger ? dommages", inflige_dommage)]

class Archipel(Jeu):
    def __init__(self, plateau: tuple[int, float]) -> None:
        """Initialise le jeu, ses constantes, ses variables et son état initial.

        Args:
            plateau (tuple[int, float]): (Nombre de cases sur la longueur, Pourcentage maximal d'ile)
        """
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
        """Retourne le bateau du joueur actif situé à l'indice passé en paramètre.

        Args:
            bateau (int): L'indice du bateau recherché.

        Returns:
            Bateau|bool: Le bateau situé à l'indice ou False si l'indice n'est pas trouvé.
        """
        retour = False
        if bateau < len(self.joueurs[self.joueur_actuel]):
            retour = self.joueurs[self.joueur_actuel][bateau]
        return retour
    
    def trouve_joueur(self, bateau: Bateau) -> Joueur|bool:
        """Renvoie le propriétaire d'un bateau.

        Args:
            bateau (Bateau): Le bateau sur lequel on investigue.

        Returns:
            Joueur|bool: Le propriétaire du bateau s'il en a un ou False dans le cas contraire.
        """
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
        """Retourne une liste composée de tuple (Bateau, Propriétaire du bateau).

        Args:
            bateaux (list[Bateau | int]): Liste des bateaux recherchés (recherche sur le joueur actif).

        Returns:
            list[tuple[Bateau, Joueur]]|bool: Liste de tuples (Bateau, Joueur) ou False si la liste est vide ou les bateaux n'existent pas.
        """
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
        """Renvoie une case du plateau grâçe à ses coordonnées.

        Args:
            case (tuple[int]): Tuple composé de deux int (x, y).

        Returns:
            Case|bool: La case correspondante aux coordonnées ou False si elle n'existe pas.
        """
        retour = False
        if type(case) == tuple[int] and len(case) >= 2:
            if self.contenu["plateau"].check_case_existe(case):
                retour = self.contenu["plateau"][case[0]][case[1]]
        return retour
    
    def trouve_cases_atteignables(self, bateau: Bateau|int) -> list[tuple[int]]:
        """Renvoie la liste des cases que le bateau passé en paramètre peut atteindre en 1 déplacement.

        Args:
            bateau (Bateau | int): Le bateau pour lequel on cherche l'info.

        Returns:
            list[tuple[int]]: Liste des coordonnées (tuple[x, y]) des cases atteignables.
        """
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
    
    def trouve_cases_a_portee(self, bateau: Bateau|int) -> list[tuple[int]]:
        """Renvoie les cases à porté de tir pour le bateau passé en paramètre.

        Args:
            bateau (Bateau | int): Le bateau pour lequel on cherche l'info.

        Returns:
            list[tuple[int]]: Liste des coordonnées (tuple[x, y]) des cases atteignables.
        """
        a_portee = []
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            plateau = self.contenu["plateau"]
            for i in range(bateau.portee+1):
                depart = bateau.position
                cases_possibles = [(depart[0], depart[1]-i), (depart[0]+i, depart[1]), (depart[0], depart[1]+i), (depart[0]-i, depart[1])]
                for j in range(len(cases_possibles)):
                    if plateau.check_case_existe(cases_possibles[j]):
                        if (cases_possibles[j]) not in a_portee: a_portee.append(cases_possibles[j])
        return a_portee
    
    def trouve_bateaux_dans_secteur(self, secteur: list[tuple[int]]) -> list[Bateau]:
        """Renvoie les bateaux présents dans un ensemble de cases (secteur).

        Args:
            secteur (list[tuple[int]]): Liste de coordonnées de cases (tuple[x, y]).

        Returns:
            list[Bateau]: Renvoie les bateaux trouvés sous forme d'une liste (peut être vide).
        """
        bateaux = []
        plateau = self.contenu["plateau"]
        for i in range(len(secteur)):
            tuile = plateau[secteur[i][0]][secteur[i][1]]
            if not tuile.type == TypeCase.ILE and tuile.contenu > 0:
                for j in range(len(tuile)):
                    bateaux.append(tuile[j])
        return bateaux
    
    # /utilitaires
    # Vérificateurs

    def check_fin_mise_en_place(self) -> bool:
        """Vérifie si tous les joueurs sont en place.

        Returns:
            bool: True si tous les joueurs sont parés à jouer, sinon, False.
        """
        fin = True
        i = 0
        while fin and i < len(self.joueurs):
            fin = self.joueurs[i].check_fin_mise_en_place()
            i += 1
        if fin:
            self.etat = Etats.EN_ATTENTE
        return fin
    
    def check_fin_partie(self) -> bool:
        """Vérifie si la partie est terminée.

        Returns:
            bool: True si la partie est terminée, sinon, False.
        """
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
        """Charge le set initial de bateaux d'un joueur.

        Returns:
            list[Bateau]: Les bateaux du set dans une liste.
        """
        contenuSet = ["gafteur" for i in range(3)] + ["ferpasseur"]
        liste = []
        for i in range(len(contenuSet)):
            ibat = libat[contenuSet[i]]
            liste.append(Bateau(ibat["nom"], ibat["vie"], ibat["marins"], ibat["pm"], ibat["degats"], ibat["portee"]))
        return liste
    
    def mise_en_place(self) -> None:
        """Effectue la mise en place du plateau et crée les joueurs.
        """
        for i in range(len(lijo)):
            joueur = lijo[i]
            self.joueurs.append(Joueur(joueur["nom"], self.contenu["bateaux"][i]))
        self.contenu["plateau"].mise_en_place()
    
    def place_bateau(self, joueur: Joueur|int, bateau: Bateau|int, case: tuple[int]) -> bool:
        """Permet de placer le bateau du joueur (passés en paramètre) sur la case ciblée.

        Args:
            joueur (Joueur | int): Le propriétaire du bateau.
            bateau (Bateau | int): Le bateau à placer.
            case (tuple[int]): La case sur laquelle on veut positionner le bateau.

        Returns:
            bool: True si le bateau a pu être placé, False dans le cas contraire.
        """
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
        """Automatise le passage au joueur suivant peut importe la phase du jeu.
        """
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

    def check_actions_possible(self, bateau: Bateau|int) -> list[tuple]:
        """Vérifie les actions réalisables pour le bateau passé en paramètres.

        Args:
            bateau (Bateau | int): Le bateau testé.

        Returns:
            list[tuple]: Liste des actions possibles sous la forme de tuples (nom, fonction).
        """
        actions = []
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            if len(self.trouve_cases_atteignables(bateau)) > 0:
                actions.append(("Deplacement", self.deplacement))
            if len(self.trouve_bateaux_dans_secteur(self.trouve_cases_a_portee(bateau))) > 0:
                actions.append(("Attaque", self.attaque))
        return actions

    def check_actions_possible_via_position(self, bateau: Bateau|int) -> list[tuple]:
        """Renvoie les actions que le bateau en paramètre peut faire, via sa position.

        Args:
            bateau (Bateau | int): Le bateau testé.

        Returns:
            list[tuple]: Liste des actions possibles sous la forme de tuples (nom, fonction).
        """
        actions = []
        if type(bateau) == int:
            bateau = self.trouve_bateau(bateau)
        if type(bateau) == Bateau:
            joueur = self.trouve_joueur(bateau)
            plateau = self.contenu["plateau"]
            tuile = plateau[bateau.position[0]][bateau.position[1]]
            voisin = tuile.get_autre_bateau(bateau)
            if type(voisin) == Bateau:
                proprio = self.trouve_joueur(voisin)
                if joueur == proprio:
                    actions.append(("Organisation", self.organisation))
                else:
                    actions.append(("Abordage", self.abordage))
        return actions

    def deplacement(self, bateau: Bateau|int, destination: tuple[int], direction: int = None) -> bool:
        """Permet de déplacer le bateau passé en paramètre vers la destination souhaitée.

        Args:
            bateau (Bateau | int): Le bateau à déplacer.
            destination (tuple[int]): Les coordonnées de la case sur laquelle le bateau doit être déplacé.
            direction (int, optional): La direction souhaité pour le bateau. None par défaut pour conserver la direction actuelle.

        Returns:
            bool: True si le déplacement a été fait, False dans le cas contraire.
        """
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
        """Permet de réaliser une organisation entre deux bateaux.

        Args:
            bateaux (tuple[Bateau]): Tuple comprenant les deux bateaux de l'organisation.
            nouvel_agencement (tuple[int]): Tuple contenant le nouveau nombre de marins pour chacun des deux bateaux.

        Returns:
            bool: True si l'organisation a pu être faite, sinon, False.
        """
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
        """Permet de réaliser un abordage en deux bateaux.

        Args:
            bateaux (tuple[Bateau | int]): Les deux bateaux qui prennent part à l'abordage.

        Returns:
            list|bool: [Bateau gagnant, joueur gagnant, liste des récompenses possibles pour le gagnant] ([False, None, []] si égalité) ou False s'il y a un problème.
        """
        ok = False
        bats = self.trouve_liste_bateaux_et_joueur(bateaux)
        if type(bats) == list and len(bats) >= 2:
            if bats[0][1] != bats[1][1] and bats[0][0].position == bats[1][0].position:
                # Conditions réspéctées, l'abordage a lieu
                gagnant = None
                recompenses = []
                if bats[0][0].get_marins() == bats[1][0].get_marins():
                    # Egalité
                    inflige_dommage(bats[0][0], bats[0][1], 1)
                    inflige_dommage(bats[1][0], bats[1][1], 1)
                    vainqueur = False
                else:
                    # Cas contraire, il y a un vainqueur
                    vainqueur = True
                    if bats[0][0].get_marins() > bats[1][0].get_marins():
                        gagnant = bats[0]
                        perdant = bats[1]
                        coule = inflige_dommage(bats[1][0], bats[1][1], 1)
                    else:
                        gagnant = bats[1]
                        perdant = bats[0]
                        coule = inflige_dommage(bats[0][0], bats[0][1], 1)
                    if not coule:
                        if perdant[0].get_marins() > 0:
                            recompenses.append(0)
                            if gagnant[0].get_marins() - perdant[0].get_marins() >= 5:
                                recompenses.append(1)
                        else:
                            recompenses.append(2)
                        if gagnant[0].get_marins() - perdant[0].get_marins() - 1 > 0:
                            recompenses.append((3, gagnant[0].get_marins() - perdant[0].get_marins() - 1))
                ok = [vainqueur, gagnant, recompenses]
        return ok
    
    def attaque(self, attaquant: Bateau|int, victime: Bateau|int) -> int:
        """Permet de réaliser une attaque entre deux bateaux.

        Args:
            attaquant (Bateau | int): Le bateau qui attaque.
            victime (Bateau | int): Le bateau attaqué.

        Returns:
            int: -1 si l'attaque n'a pas pu ce faire. Dans le cas contraire, 0 si la victime n'a pas coulée et 1 si elle a coulée.
        """
        ok = -1
        bats = self.trouve_liste_bateaux_et_joueur([attaquant, victime])
        if type(bats) == list and len(bats) == 2:
            if bats[1][0] in self.trouve_bateaux_dans_secteur(self.trouve_cases_a_portee(bats[0][0])):
                coule = inflige_dommage(bats[1][0], bats[1][1], bats[0][0].degats)
                if coule:
                    ok = 1
                else:
                    ok = 0
        return ok
    
    def defini_vainqueur(self) -> Joueur:
        """Désigne le joueur ayant remporté la victoire.

        Returns:
            Joueur: Le vainqueur.
        """
        vainqueur = None
        if self.joueurs[0].check_defaite() and self.joueurs[1].check_defaite():
            if self.joueurs[0].nb_elimination > self.joueurs[1].nb_elimination:
                vainqueur = vainqueur = self.joueurs[0]
            elif self.joueurs[1].nb_elimination > self.joueurs[0].nb_elimination:
                vainqueur = vainqueur = self.joueurs[1]
        else:
            if self.joueurs[0].check_defaite():
                vainqueur = self.joueurs[1]
            elif self.joueurs[1].check_defaite():
                vainqueur = self.joueurs[0]
        return vainqueur