from systeme.FondMarin import *
from museeNoyee import croixLumineuse, croixSombre
from ui.clickIma import ClickIma
from ui.blocTexte import BlocTexte
from parametres.menu import Menu
from interpreteur.interpreteurMd import InterpreteurMd

class Parametres:
    def __init__(self) -> None:
        """Crée la fenêtre des paramètres.
        """
        self.ouvert = False
        self.largeurLat = int(xf*0.25)
        self.fichierMenu = "parametres/Categories.md"
        self.menu = Menu(self.fichierMenu, (0, int(yf*0.078), self.largeurLat, int(yf-yf*0.128)))
        repMenu = self.menu.checkFichier()
        if repMenu:
            self.page = InterpreteurMd(self.menu.contenu[self.menu.actif][1], 
                                       (self.largeurLat, 0, xf-self.largeurLat, yf))
            self.bug = False
        else:
            self.bug = True
        self.croix = ClickIma([self.ferme], [croixSombre, croixLumineuse])
        self.charge = False
        self.fond = None

    def dessine(self) -> None:
        """Dessine la fenêtre à l'écran.
        """
        if not self.bug and self.page.fichier != self.menu.contenu[self.menu.actif][1]:
            self.page.changeFichier(self.menu.contenu[self.menu.actif][1])
        if not self.charge:
            self.chargeElement()
        if self.fond != None:
            draw_texture(self.fond, 0, 0, WHITE)
        if not self.bug:
            self.dessineMenu()
            self.page.dessine()
            draw_rectangle(0, 0, self.largeurLat, int(yf*0.078), [87, 67, 237, 255])
            draw_text_pro(police1, "Parametres", (int(yf*0.02), int(yf*0.02)), (0, 0), 0, int(yf*0.05), 
                          0, WHITE)
            self.dessineVersion()
        else:
            self.erreur()
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

    def erreur(self) -> None:
        """Définit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.
        """
        taillePolice = int(yf*0.035)
        draw_texture(self.iErreur, int(xf/2-self.iErreur.width/2), int(yf*0.4-self.iErreur.height/2), WHITE)
        titre = BlocTexte("Un probleme est survenu !", police2, taillePolice*1.2, [xf, ''])
        sousTitre = BlocTexte("Chargement interrompue.", police2, taillePolice, [xf, ''])
        message = BlocTexte(f"Le fichier \"{self.fichierMenu}\" est manquant.", police2, taillePolice*0.8, [xf, ''])
        titre.dessine([[int(xf/2), int(yf*0.7)], 'c'])
        sousTitre.dessine([[int(xf/2), int(yf*0.75)], 'c'])
        message.dessine([[int(xf/2), int(yf*0.8)], 'c'], [242, 171, 56, 255])