from tkinter import E
from FondMarin import Poli1, Poli2, fond, xf, yf, tlatba, gris, noir, blanc

class Bouton:
    def __init__(self, fonction, texte: str="", couleur: str=gris, etat: bool=True, nom: list=["bt"]) -> None:
        self.nom = nom
        self.texte = texte
        self.couleur = couleur
        self.etat = etat
        self.fonction = fonction
        fond.tag_bind(self.nom[0], '<Button-1>', self.reaction)

    def dessine(self, coord: tuple=(xf/2, yf/2)) -> None:
        t = int((yf*0.02)/3*3)
        xr = tlatba*0.8
        yr = yf*0.1
        p = Poli2
        c = self.couleur
        if t*len(self.texte) >= xr:
            p = Poli1
        if not self.etat:
            c = gris
        fond.create_rectangle(coord[0]-xr/2, coord[1]-yr/2, coord[0]+xr/2, coord[1]+yr/2, fill=c, 
                              outline=noir, width=2, tags=self.nom+[f'fbt{self.nom[0]}'])
        fond.create_text(coord[0], coord[1], text=self.texte, fill=blanc, font=p, tags=self.nom)

    def getEtat(self) -> bool:
        return self.etat

    def setEtat(self, etat: bool) -> None:
        if etat:
            c = self.couleur
        else:
            c = gris
        fond.itemconfigure(f'fbt{self.nom[0]}', fill=c)
        self.etat = etat

    def reaction(self, event) -> None:
        if self.etat:
            self.fonction()