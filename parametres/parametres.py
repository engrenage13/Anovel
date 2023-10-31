import platform
from systeme.FondMarin import *
from systeme.set import trouveParam, sauvegarde, setParam
from systeme.verif import verifSauvegarde
from ui.PosiJauge import PosiJauge
from ui.interrupteur import Interrupteur
from ui.bouton.bouton import Bouton
from ui.bouton.grille import Grille
from parametres.menu import Menu
from reve.Reve import Reve
from reve.OZ import NOMREVE, VERSIONREVE
from random import choice

class Parametres:
    def __init__(self) -> None:
        """Crée la fenêtre des paramètres.
        """
        self.largeurLat = int(xf*0.25)
        self.fichierMenu = "parametres/Categories.md"
        self.htBanniere = int(yf*0.078)
        self.menu = Menu(self.fichierMenu, (0, self.htBanniere, self.largeurLat, int(yf*0.92)))
        print(self.menu.actif)
        self.page = Reve(self.menu.contenu[self.menu.actif][1], 
                         (self.largeurLat, espaceBt+TB2n.hauteur, xf-self.largeurLat, yf-espaceBt+TB2n.hauteur))
        self.grOpt = Grille(int(xf*0.15), [False])
        self.grOpt.ajouteElement(Bouton(TB2o, BTDANGER, "REINITIALISER", '', [self.reset]), 0, 0)
        self.grOpt.ajouteElement(Bouton(TB2n, PTIBT1, "FERMER", 'images/ui/CroSom.png', [self.portailBoreal]), 1, 0)
        self.charge = False
        self.fond = None
        # Paramètres
        self.lset = []
        self.copieValeur = []
        # Between the worlds
        self.play = False
        self.message = ""
        self.lu = True

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        if self.page.fichier != self.menu.contenu[self.menu.actif][1]:
            self.page.changeFichier(self.menu.contenu[self.menu.actif][1])
            self.copieValeur = []
            sauvegarde()
            verifSauvegarde()
        if not self.charge:
            self.chargeElement()
        if self.fond != None:
            draw_texture(self.fond, 0, 0, WHITE)
        self.dessineMenu()
        self.page.dessine()
        self.lset = self.page.liSetWidge
        self.InitialiseWidget()
        draw_rectangle(self.largeurLat, 0, xf-self.largeurLat, espaceBt+TB2n.hauteur, [0, 0, 0, 170])
        draw_rectangle_gradient_ex((0, 0, self.largeurLat, self.htBanniere), 
                                [51, 7, 144, 255], [145, 104, 235, 255], BLACK, BLACK)
        draw_text_pro(police1i, "PARAMETRES", (int(yf*0.02), int(yf*0.02)), (0, 0), 0, int(yf*0.06), 0, WHITE)
        self.dessineVersion()
        self.setValeurWidgets()
        self.grOpt.dessine(int(xf-self.grOpt.largeur), 0)

    def dessineMenu(self) -> None:
        """Permet de dessiner le menu latérale.
        """
        draw_rectangle(0, 0, self.largeurLat, yf, [20, 20, 30, 150])
        self.menu.dessine()

    def dessineVersion(self) -> None:
        """Dessine la partie indiquant la version du jeu.
        """
        taille = int(yf*0.03)
        draw_rectangle_gradient_ex((0, yf-int(yf*0.08), self.largeurLat, int(yf*0.08)), 
                                    [87, 25, 243, 255], [24, 87, 197, 255], [58, 117, 219, 255], BLACK)
        tt1 = measure_text_ex(police1, config_sys['type_version'].upper(), taille, 0)
        draw_rectangle_rounded((int(xf*0.005), int(yf*0.93), int(xf*0.01+tt1.x), int(yf*0.01+tt1.y)), 
                                0.3, 30, ORANGE)
        draw_text_pro(police1, config_sys['type_version'].upper(), (int(xf*0.01), int(yf*0.935)), (0, 0), 0, taille, 0, 
                      WHITE)
        draw_text_pro(police1, config_sys['version'], (int(xf*0.02+tt1.x), int(yf*0.935)), (0, 0), 0, taille, 0, WHITE)
        tt2 = measure_text_ex(police1, config_sys['version'], int(taille*1.1), 0)
        vSys = f"Python {platform.python_version()} - {platform.system()} {platform.release()}"
        draw_text_pro(police2, vSys.upper(), (int(xf*0.025+tt1.x+tt2.x), int(yf*0.935+tt1.y*0.1)), 
                      (0, 0), 0, int(taille*0.7), 0, LIGHTGRAY)
        texte = f"Parametres genere par {NOMREVE} {VERSIONREVE}".upper()
        tv = measure_text_ex(police3i, texte, int(taille*0.6), 0)
        draw_text_pro(police3i, texte, (int(xf*0.005), int(yf-tv.y*1.2)), (0, 0), 0, int(taille*0.6), 0, GRAY)

    def chargeElement(self) -> None:
        """Permet de charger certains éléments nécessaire au fonctionnement de la fenêtre lors de son démarrage.
        """
        tableau = load_image(f"images/backgrounds/{choice(['boussole', 'machinerie'])}.png")
        ratio = yf/tableau.height
        image_resize(tableau, int(tableau.width*ratio), int(tableau.height*ratio))
        self.fond = load_texture_from_image(tableau)
        unload_image(tableau)
        self.charge = True

    def InitialiseWidget(self) -> None:
        """Permet de rétablir les valeurs actuelles des paramètres sur les widgets.
        """
        valeur = "?"
        cpval = "?"
        for i in range(len(self.lset)):
            balise = self.lset[i]
            valeur = trouveParam(balise[0])
            trouve = False
            settatitude = False
            j = 0
            while j < len(self.copieValeur) and not trouve:
                if self.copieValeur[j][0] == balise[0]:
                    trouve = True
                    cpval = self.copieValeur[j][1]
                else:
                    j = j + 1
            if not trouve:
                self.copieValeur.append([balise[0], valeur])
                settatitude = True
            else:
                if valeur != cpval:
                    self.copieValeur[j][1] = valeur
                    settatitude = True
            if settatitude:
                if type(balise[1]) == PosiJauge:
                    balise[1].setPosCurseur(valeur)
                elif type(balise[1]) == Interrupteur:
                    if balise[1].getValeur() != int(valeur):
                        balise[1].switch()

    def setValeurWidgets(self) -> None:
        """Permet d'enregister les valeurs des widgets dans le fichier de sauvegarde.
        """
        for i in range(len(self.lset)):
            balise = self.lset[i]
            if not balise[1].getLu():
                setParam(balise[0], balise[1].getValeur())
                balise[1].marqueCommeLu()

    def reset(self) -> None:
        """Réinitialise les paramètres du jeu.
        """
        sauvegarde(True)

    # Between the worlds
    def portailBoreal(self) -> None:
        """Ferme les paramètres.
        """
        self.message = 'PRECEDENT'
        self.lu = False
        sauvegarde()
        verifSauvegarde()