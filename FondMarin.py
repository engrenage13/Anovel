import screeninfo
import tkinter as tk
from tkinter import *
from tkinter.font import Font

TITRE_F = 'NAVALE'
version = "0.1.9"

def trouveEcran(x, y): # Trouve l'écran utilisé
    monitors = screeninfo.get_monitors()
    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]

Fen = tk.Tk()

Fen.rowconfigure(0, weight=1)
Fen.columnconfigure(0, weight=1)

ecran = trouveEcran(Fen.winfo_x(), Fen.winfo_y())

def auRevoir(): # Ferme le jeu.
    Fen.quit()

# Dimensions
xf = ecran.width
yf = ecran.height
tlatba = (xf - yf*0.84)/2
yp = yf*0.15
origyp = yf*0.105
pasApas = yf*0.05
dpd = xf-tlatba

# Polices
Poli1 = Font(family='Stencil', size=int(yf*0.02))
Poli2 = Font(family='Stencil', size=int((yf*0.02)/3*5))
Poli3 = Font(family='Stencil', size=int((yf*0.02)/3*20))
Lili1 = Font(family='Lilita One', size=int(yf*0.015))
Lili2 = Font(family='Lilita One', size=int(yf*0.02))
Lili3 = Font(family='Lilita One', size=int(yf*0.04))

# Couleurs
gris = "#333333"
grisClair = "#555555"
mauve = "#3322AA"
bleuBt = "#0044BB"
bleu1 = '#0066FF'
bleu2 = '#0055EE'
grisBlanc = '#CCCCCC'
blanc = 'white'
vertFluo = "#00FF00"
rouge = 'red'
orange = 'orange'
noir = 'black'

mer = [bleu1, bleu2]

fond = Canvas(Fen, width=xf, height=yf, bg='black', bd=-2)
fond.grid(row=0, column=0, sticky="nswe")