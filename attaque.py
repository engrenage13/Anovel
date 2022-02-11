from FondMarin import *
from objets.Bateau import *
from finPartie import ecranFin

def localiseCurseur(plateau: list) -> object:
    # Renvoie le tag de la case sur laquelle est le curseur, ou None, sinon.
    a = fond.winfo_pointerxy()
    b = False
    i = 0
    while i < len(plateau) and not b:
        j = 0
        while j < len(plateau[i]) and not b:
            c = fond.coords(plateau[i][j])
            if a[0] >= c[0] and a[0] <= c[2] and a[1] >= c[1] and a[1] <= c[3]:
                b = True
            else:
                j = j + 1
        if not b:
            i = i + 1
    if b:
        sortie = plateau[i][j]
    else:
        sortie = None
    return sortie

def attaque(joueur: object, position: float) -> None:
    # boucle pour laisser le viseur en place tant que le joueur n'a pas tirer.
    fond.delete('pointeur')
    a = localiseCurseur(joueur.cTire)
    d = fond.find_withtag('ecranFin')
    if a != None and len(d) == 0:
        b = fond.coords(a)
        fond.create_rectangle(b[0], b[1], b[2], b[3], fill='', outline='white', width=4, tag='pointeur')
        fond.create_oval(b[0]+(b[2]-b[0])*0.2, b[1]+(b[3]-b[1])*0.2, b[2]-(b[2]-b[0])*0.2, b[3]-(b[3]-b[1])*0.2, 
                         fill='', outline=grisClair, width=3, tag='pointeur')
        if getEtatCase(a):
            case = a[0:len(a)-2]
            col = blanc
        else:
            case = "X"
            col = orange
        fond.create_line(b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])*0.1, b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])*0.35, 
                         width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[2]-(b[2]-b[0])*0.1, b[1]+(b[3]-b[1])/2, b[2]-(b[2]-b[0])*0.35, b[1]+(b[3]-b[1])/2, 
                         width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[0]+(b[2]-b[0])/2, b[3]-(b[3]-b[1])*0.1, b[0]+(b[2]-b[0])/2, b[3]-(b[3]-b[1])*0.35, 
                         width=2, fill=grisClair, tag='pointeur')
        fond.create_line(b[0]+(b[2]-b[0])*0.1, b[1]+(b[3]-b[1])/2, b[0]+(b[2]-b[0])*0.35, b[1]+(b[3]-b[1])/2, 
                         width=2, fill=grisClair, tag='pointeur')
        fond.create_text(b[0]+(b[2]-b[0])/2, b[1]+(b[3]-b[1])/2, text=case, font=Lili1, fill=col, 
                         tags=('pointeur', 'affiTgVis'))
    c = fond.coords(joueur.cTire[0][0])
    if int(c[1]) == int(position) and len(d) == 0:
        fond.after(50, attaque, joueur, c[1])
    else:
        fond.delete('pointeur')

def marquerCase(idCase: str, idplateau: str, joueurCible: object) -> None: # Marque les cases touchées.
    tag = idCase+idplateau
    c = grisBlanc
    if estToucheBateau(joueurCible, idCase):
        c = 'red'
    fond.itemconfigure(tag, fill=c)

def getEtatCase(idCase: str, idPlateau: str="") -> bool: # Renvoie l'état de la case (touché ou non).
    tag = idCase+idPlateau
    c = fond.itemcget(tag, 'fill')
    rep = True
    if c == 'red' or c == grisBlanc:
        rep = False
    return rep

def monter(pas: float): # Fait descendre les plateaux.
    for i in range(len(joueurs)):
        fond.move(('cTire'+str(i+1)), 0, pas)
    a = fond.coords(joueurs[0].cTire[0][0])
    if int(a[1]) != int(origyp):
        fond.after(30, monter, pas)
    else:
        fond.itemconfigure('titre', text=joueurs[0].nom)
        connect()
        attaque(joueurs[0], a[1])

def descendre(pas: float): # Fait monter les plateaux.
    for i in range(len(joueurs)):
        fond.move(('cTire'+str(i+1)), 0, -pas)
    a = fond.coords(joueurs[1].cTire[0][0])
    if int(a[1]) != int(origyp):
        fond.after(30, descendre, pas)
    else:
        fond.itemconfigure('titre', text=joueurs[1].nom)
        connect()
        attaque(joueurs[1], a[1])

def monterOuQuitter(): # Vérifie si le joueur qui joue à gagner...
    if aPerduJoueur(joueurs[0]):
        ecranFin(joueurs[1].nom)
    else:
        monter(pasApas)

def descendreOuQuitter(): # Vérifie si le joueur qui joue à gagner...
    if aPerduJoueur(joueurs[1]):
        ecranFin(joueurs[0].nom)
    else:
        descendre(pasApas)

def deconnect():
    fond.tag_unbind('pointeur', '<Button-1>')
    fond.tag_unbind('cTire2', '<Button-1>')
    fond.tag_unbind('cTire1', '<Button-1>')

def connect():
    fond.tag_bind('cTire1', '<Button-1>', aj2)
    fond.tag_bind('cTire2', '<Button-1>', aj1)
    fond.tag_bind('pointeur', '<Button-1>', cliqueCurseur)

def cliqueCurseur(event): # Réagit à un clique sur le pointeur/viseur.
    t = fond.itemcget('affiTgVis', 'text')
    if t != "X":
        deconnect()
        p1 = getEtatCase(fond.itemcget('affiTgVis', 'text'), 'c1')
        p2 = getEtatCase(fond.itemcget('affiTgVis', 'text'), 'c2')
        if p1 or p2:
            c = fond.coords(joueurs[0].cTire[0][0])
            if int(c[1]) == int(origyp):
                marquerCase(fond.itemcget('affiTgVis', 'text'), 'c1', joueurs[1])
                fond.after(1000, descendreOuQuitter)
            else:
                marquerCase(fond.itemcget('affiTgVis', 'text'), 'c2', joueurs[0])
                fond.after(1000, monterOuQuitter)

def aj1(event): # Affiche le plateau d'attaque du premier joueur.
    t = fond.itemcget('affiTgVis', 'text')
    if t != "X":
        deconnect()
        p = getEtatCase(fond.itemcget('affiTgVis', 'text'), 'c2')
        if p:
            marquerCase(fond.itemcget('affiTgVis', 'text'), 'c2', joueurs[0])
            fond.after(1000, monterOuQuitter)

def aj2(event): # Affiche le plateau d'attaque du second joueur.
    t = fond.itemcget('affiTgVis', 'text')
    if t != "X":
        deconnect()
        p = getEtatCase(fond.itemcget('affiTgVis', 'text'), 'c1')
        if p:
            marquerCase(fond.itemcget('affiTgVis', 'text'), 'c1', joueurs[1])
            fond.after(1000, descendreOuQuitter)

fond.tag_bind('cTire1', '<Button-1>', aj2)
fond.tag_bind('cTire2', '<Button-1>', aj1)
fond.tag_bind('pointeur', '<Button-1>', cliqueCurseur)