from ui.scrollBarre import ScrollBarre
from reve.decodeuses import texte, widget, cadre, checkFinCadre
from reve.dimensions import mesureTaille
from reve.dessin import *

class Reve:
    def __init__(self, fichier: str, dims: tuple) -> None:
        """Crée une instance de "REVE", un interpréteur markdown.

        Args:
            fichier (str): L'url du fichier qui doit être interprété.
            dims (tuple): La position et les dimensions de la zone dans laquelle doit s'afficher le contenu du fichier.
        """
        # Fichier
        self.fichier = fichier
        self.decode = False
        # Zone
        self.origine = (dims[0], dims[1])
        self.largeur = dims[2]
        self.hauteur = dims[3]
        self.hauteurTotale = self.hauteur
        self.espace = int(yf*0.03)
        self.evaluation = False
        # Elements
        self.contenu = []
        self.lContenu = int(self.largeur*0.95)
        self.pasx = int(xf*0.0125)
        self.pasy = int(yf*0.05)
        # Widgets
        self.liSetWidge = []
        self.attenteParam = False
        # Scroll
        self.scrollBarre = ScrollBarre([self.origine[0], self.origine[1], self.largeur, self.hauteur], 
                                        self.hauteurTotale, [[1, 8, 38], [12, 37, 131]])
        self.oyc = self.scrollBarre.getPos()

    def dessine(self) -> None:
        """Dessine le contenu du fichier à l'écran.
        """
        if not self.decode:
            self.startDecode()
        if not self.evaluation:
            self.setHauteurContenu()
        x = self.origine[0]+self.pasx
        ph = self.oyc
        for i in range(len(self.contenu)):
            element = self.contenu[i]
            if type(element) == list and type(element[0]) == list:
                ph += dessineCadre(element, x, ph, self.espace)[1] + self.espace
            elif type(element) == BlocTexte:
                ph += dessineTexte(element, x, ph)[1] + int(self.espace/2)
            elif type(element) == Interrupteur:
                ph += dessineInterrupteur(element, x, ph)[1] + int(self.espace/2)
            elif type(element) == PosiJauge:
                ph += dessinePosiJauge(element, x, ph, self.lContenu)[1] + self.espace
            elif type(element) == str:
                ph += self.espace
        if self.hauteurTotale > self.hauteur:
            self.scrollBarre.dessine()
            self.oyc = self.scrollBarre.getPos()

    def startDecode(self) -> None:
        """Permet de vérifier si le fichier a été décodé.
        """
        if not self.decode:
            self.decodeur()
            self.decode = True

    def decodeur(self) -> None:
        """Permet de décoder le texte du fichier traiter.
        """
        fic = load_file_text(self.fichier)
        fil = fic.split("\n")
        cadres = []
        while len(fil) > 0:
            if ">" in fil[0]:
                eleType = fil[0].split(">")
                if eleType[0] == "*":
                    self.liSetWidge.append([eleType[1]])
                    self.attenteParam = True
                else:
                    rep = widget(fil[0])
                    if rep != None:
                        if len(cadres) == 0:
                            self.ajouteContenu(rep)
                        else:
                            cadres[len(cadres)-1].append(rep)
                        if self.attenteParam:
                            self.liSetWidge[len(self.liSetWidge)-1].append(rep)
                            self.attenteParam = False
                        if checkFinCadre(fil[0]):
                            self.finCadre(cadres)
            elif "[" in fil[0]:
                rep = cadre(fil[0])
                prop = self.pasx/self.lContenu
                largeur = int(self.lContenu*(1-prop*2*(len(cadres))))
                cadres.append([[largeur]+rep])
            elif fil[0] == "]":
                self.finCadre(cadres)
            elif fil[0] != "":
                prop = self.pasx/self.lContenu
                rep = texte(fil[0], int(self.lContenu*(1-prop*2*(len(cadres)))))
                if len(cadres) == 0:
                    self.ajouteContenu(rep)
                else:
                    cadres[len(cadres)-1].append(rep)
            else:
                if len(cadres) == 0:
                    self.ajouteContenu("\n")
                else:
                    cadres[len(cadres)-1].append("\n")
            del fil[0]

    def finCadre(self, cadres: list) -> list:
        if len(cadres) > 0:
            cad = cadres[len(cadres)-1]
            del cadres[len(cadres)-1]
            if len(cadres) > 0:
                cadres[len(cadres)-1].append(cad)
            else:
                self.ajouteContenu(cad)
        return cadres

    def changeFichier(self, fichier: str) -> None:
        """Permet de changer le fichier qu'utilise l'interpréteur.

        Args:
            fichier (str): Nouveau fichier utilisé par l'interpréteur.
        """
        self.fichier = fichier
        self.decode = False
        self.evaluation = False
        self.liSetWidge = []
        self.oyc = int(self.origine[1] + yf*0.02)
        self.contenu.clear()

    def setHauteurContenu(self) -> None:
        """Modifie la taille théorique de la totalité du contenu de la fenêtre.
        """
        self.hauteurTotale = mesureTaille(self.contenu, self.espace)
        if self.hauteurTotale > self.hauteur:
            self.scrollBarre.setHtContenu(self.hauteurTotale)
        self.evaluation = True

    def ajouteContenu(self, contenu: list) -> None:
        """Permet d'ajouter du contenu dans la fenêtre.

        Args:
            contenu (list): Le contenu qu'on ajoute.
        """
        self.contenu.append(contenu)
        self.evaluation = False