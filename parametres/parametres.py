from systeme.FondMarin import *
from systeme.set import trouveParam, sauvegarde, setParam
from museeNoyee import croixLumineuse, croixSombre
from ui.PosiJauge import PosiJauge
from ui.clickIma import ClickIma
from ui.blocTexte import BlocTexte
from ui.scrollBarre import ScrollBarre
from parametres.menu import Menu
from reve.Reve import Reve
from reve.erreurs import affichErreur
from reve.dimensions import getDimsErreur, mesureTailleErreurs

class Parametres:
    def __init__(self) -> None:
        """Crée la fenêtre des paramètres.
        """
        self.ouvert = False
        self.largeurLat = int(xf*0.25)
        self.fichierMenu = "parametres/Categories.md"
        self.menu = Menu(self.fichierMenu, (0, int(yf*0.078), self.largeurLat, int(yf-yf*0.128)))
        repMenu = self.menu.checkFichier()
        if len(repMenu) == 0:
            self.page = Reve(self.menu.contenu[self.menu.actif][1], (self.largeurLat, 0, xf-self.largeurLat, yf))
            self.bug = False
        else:
            self.bug = True
            self.erreurs = repMenu
            self.scroll = ScrollBarre([0, int(yf*0.08), xf, yf], int(yf*0.9), [[1, 8, 38], [12, 37, 131]])
            self.oyc = self.scroll.getPos()
            self.setHt = False
        self.croix = ClickIma([self.ferme], [croixSombre, croixLumineuse])
        self.charge = False
        self.fond = None
        # Paramètres
        self.lset = []
        self.copieValeur = []

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        if not self.bug and self.page.fichier != self.menu.contenu[self.menu.actif][1]:
            self.page.changeFichier(self.menu.contenu[self.menu.actif][1])
            self.copieValeur = []
            sauvegarde()
        if not self.charge:
            self.chargeElement()
        if self.fond != None:
            draw_texture(self.fond, 0, 0, WHITE)
        if not self.bug:
            self.dessineMenu()
            self.page.dessine()
            self.lset = self.page.liSetWidge
            self.InitialiseWidget()
            draw_rectangle(0, 0, self.largeurLat, int(yf*0.078), [87, 67, 237, 255])
            draw_text_pro(police1, "Parametres", (int(yf*0.02), int(yf*0.02)), (0, 0), 0, int(yf*0.05), 
                          0, WHITE)
            self.dessineVersion()
            self.setValeurWidgets()
        else:
            self.dessinErreur()
            if self.scroll.htContenu > yf:
                self.scroll.dessine()
                self.oyc = self.scroll.getPos()
            if not self.setHt:
                self.scroll.setHtContenu(self.dessinErreur()+mesureTailleErreurs(self.erreurs, int(yf*0.05)))
                self.setHt = True
        self.croix.dessine((xf-hbarre, int(hbarre*0.05)))

    def dessineMenu(self) -> None:
        """Permet de dessiner le menu latérale.
        """
        draw_rectangle(0, 0, self.largeurLat, yf, [20, 20, 30, 150])
        self.menu.dessine()

    def dessineVersion(self) -> None:
        """Dessine la partie indiquant la version du jeu.
        """
        draw_rectangle(0, yf-int(yf*0.05), self.largeurLat, int(yf*0.05), [10, 10, 10, 255])
        texte = f"{etatVersion.upper()} - {version}"
        taille = int(yf*0.03)
        tv = measure_text_ex(police2, texte, taille, 0)
        draw_text_pro(police2, texte, (int(xf*0.01), int(yf-tv.y*1.2)), (0, 0), 0, taille, 0, WHITE)

    def chargeElement(self) -> None:
        """Permet de charger certains éléments nécessaire au fonctionnement de la fenêtre lors de son démarrage.
        """
        if not self.bug:
            tableau = load_image('images/backgrounds/machinerie.png')
            ratio = yf/tableau.height
        else:
            tableau = load_image('images/ui/erreur.png')
            ratio = yf/2/tableau.height
        image_resize(tableau, int(tableau.width*ratio), int(tableau.height*ratio))
        if not self.bug:
            self.fond = load_texture_from_image(tableau)
        else:
            self.iErreur = load_texture_from_image(tableau)
        unload_image(tableau)
        self.charge = True

    def ouvre(self) -> None:
        """Permet d'ouvrir la fenêtre (fictivement).
        """
        self.ouvert = True
    
    def ferme(self) -> None:
        """Permet de fermer la fenêtre (fictivement).
        """
        self.ouvert = False
        sauvegarde()

    def dessinErreur(self) -> int:
        """Definit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.
        """
        taillePolice = int(yf*0.035)
        y = self.oyc-int(yf*0.08)
        draw_texture(self.iErreur, int(xf/2-self.iErreur.width/2), y, WHITE)
        y += int(self.iErreur.height*1.1)
        titre = BlocTexte("Un probleme est survenu !", police2, taillePolice*1.2, [xf, ''])
        sousTitre = BlocTexte("Chargement interrompue.", police2, taillePolice, [xf, ''])
        titre.dessine([[int(xf/2), y], 'c'])
        y += int(yf*0.05)
        sousTitre.dessine([[int(xf/2), y], 'c'])
        y += int(yf*0.05)
        ph = y
        for i in range(len(self.erreurs)):
            affichErreur(self.erreurs[i], [0, xf], y, int(yf*0.05))
            y += getDimsErreur(self.erreurs[i], int(yf*0.05))[1] + int(yf*0.05)
        return ph

    def InitialiseWidget(self) -> None:
        """Permet de rétablir les valeurs actuelles des paramètres sur les widgets.
        """
        valeur = "?"
        cpval = "?"
        for i in range(len(self.lset)):
            balise = self.lset[i]
            valeur = trouveParam(balise[0])
            trouve = False
            j = 0
            while j < len(self.copieValeur) and not trouve:
                if self.copieValeur[j][0] == balise[0]:
                    trouve = True
                    cpval = self.copieValeur[j][1]
                else:
                    j = j + 1
            if not trouve:
                self.copieValeur.append([balise[0], valeur])
                if type(balise[1]) == PosiJauge:
                    balise[1].setPosCurseur(valeur)
            else:
                if valeur != cpval:
                    self.copieValeur[j][1] = valeur
                    if type(balise[1]) == PosiJauge:
                        balise[1].setPosCurseur(valeur)

    def setValeurWidgets(self) -> None:
        """Permet d'enregister les valeurs des widgets dans le fichier de sauvegarde.
        """
        for i in range(len(self.lset)):
            balise = self.lset[i]
            if not balise[1].getLu():
                setParam(balise[0], balise[1].getValeur())
                balise[1].marqueCommeLu()