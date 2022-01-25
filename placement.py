import tkinter as tk
from tkinter import *
from FondMarin import *
from attaque import *

liBat1 = []
liBat2 = []

# jeu ////////////////////////////////////////////////////////////////

def checkEtat(event): # Vérifie l'état du bouton de validation, quand on clique dessus.
    a = fond.itemcget('btV', 'fill')
    b = 0
    i = 0
    if a != gris:
        while i < len(joueurs) and b < 2:
            if not joueurs[i].pret:
                b = b + 1
                if b == 1:
                    joueurs[i].pret = True
            i = i + 1
        if b < 2:
            verrouillage()
        else:
            suivant()

def suivant(): # Permet au joueur suivant d'installer son plateau.
    fond.itemconfigure('btV', fill=gris)
    fond.itemconfigure('base1', state='hidden')
    fond.itemconfigure('set1', state='hidden')
    fond.itemconfigure('base2', state='normal')
    fond.itemconfigure('set2', state='normal')
    fond.delete('nSet1')
    fond.itemconfigure('nSet2', state='normal')
    fond.itemconfigure('titre', text=(f"{liBat2[0].proprio.nom} - Installation"))
    for i in range(len(liBat1)):
        fond.tag_unbind(liBat1[i].tag, '<Button-1>')
        fond.tag_unbind(liBat1[i].tag, '<Button-3>')

def verrouillage(): # Passe du mode positionnement à la partie.
    fond.delete('valid')
    fond.delete('nomBat')
    fond.itemconfigure('base2', state='hidden')
    fond.itemconfigure('set2', state='hidden')
    for i in range(len(liBat2)):
        fond.tag_unbind(liBat2[i].tag, '<Button-1>')
        fond.tag_unbind(liBat2[i].tag, '<Button-3>')
    for j in range(len(joueurs)):
        a = 'cTire' + str(joueurs[j].id)
        fond.itemconfigure(a, state='normal')
        fond.move(a, 0, yf*j)
    fond.itemconfigure('titre', text=(joueurs[0].nom))
    fond.move('titre', -xf*0.055, 0)
    a = fond.coords(joueurs[0].cTire[0][0])
    attaque(joueurs[0], a[1])

def vigile(liste: list): # Remet les bateaux rejetés du plateau, correctement en place dans le panneau latéral.
    a = False
    c = fond.coords('pg')
    for i in range(len(liste)):
        b = fond.coords(liste[i].tag)
        if int(b[0]) <= int(c[2]*0.05):
            a = True
    if a:
        placeLat(liste)
    else:
        fond.after(1000, vigile, liste)

def placeLat(liste: list): # Place les bateaux sur le panneau latéral de gauche.
    a = fond.coords('pg')
    for i in range(len(liste)):
        b = fond.coords(liste[i].tag)
        d = fond.coords(liste[i].tagPlus)
        c = int(a[3]*0.05)
        if int(b[1]) == c:
            fond.move(liste[i].tag, 0, yp*(i+1))
        if int(d[1]) == int(c*0.4):
            fond.move(liste[i].tagPlus, 0, yp*(i+1))
        fin()
    fond.delete('Pharos')

def resetBat(bateau: object): # Supprime le modèle "grande taille" du bateau pour recréer le modèle "petite taille."
    c = fond.coords('pg')
    x = c[2]*0.05
    y = c[3]*0.05
    a = fond.coords(bateau.tag)
    fond.delete(bateau.tag)
    fond.create_rectangle(a[0], a[1], a[0]+(c[2]*0.12)*bateau.taille, a[1]+(c[3]*0.05), fill="#444444", 
                          tags=('bateau', bateau.tag, ('set'+str(bateau.proprio.id))))
    reposeBat(bateau, (x, y))

def reposeBat(bateau: object, coo: tuple): # Remet le bateau en place dans le panneau latéral de gauche.
    a = fond.coords(bateau.tag)
    b = int(a[0])-int(coo[0])
    d = int(a[1])-int(coo[1])
    fond.move(bateau.tag, -b, -d)
    if int(b) != 0:
        fond.after(50, reposeBat, bateau, coo)
    else:
        bateau.pos = None
        vigile(bateau.proprio.SetBateaux)

def glisseListe(souris: tuple, milieu: tuple, bateau: object): # Corrige les éventuels problèmes de vitesse
    # rencontrés lors de la localisation des bateaux.
    if bateau.orient == 'h':
        if souris[0] < milieu[0]:
            bateau.sens = -1
        else:
            bateau.sens = 0
    else:
        if souris[1] < milieu[1]:
            bateau.sens = -2
        else:
            bateau.sens = 0

def positionneBien(bateau: object, coo: tuple): 
    # Fait en sorte que le bateau appelé soit bien positionné sur le plateau.
    a = fond.coords(bateau.tag)
    b = coo[0] - a[0]
    c = coo[1] - a[1]
    fond.move(bateau.tag, int(b), int(c))
    if int(b) != 0:
        fond.after(50, positionneBien, bateau, coo)
    else:
        fond.delete('Pharos')
        fin()

def fin(): # Place le bouton dans les états "veille" et "actif", en fonction de la position des bateaux.
    d = True
    i = 0
    while d and i < len(liBat1):
        if liBat1[i].pos == None:
            d = False
        elif type(liBat1[i].pos) == list:
            if None in liBat1[i].pos:
                d = False
                liBat1[i].pos = None
        i = i + 1
    if d:
        fond.itemconfigure('btV', fill=bleuBt)
    else:
        fond.itemconfigure('btV', fill=gris)

def localCase(coo: tuple, bateau: object): # Trouve les cases individuellement.
    b = None
    for i in range(len(bateau.proprio.base)):
        for j in range(len(bateau.proprio.base[i])):
            a = fond.coords(bateau.proprio.base[i][j])
            if coo[0] >= a[0] and coo[0] <= a[2] and coo[1] >= a[1] and coo[1] <= a[3]:
                b = bateau.proprio.base[i][j]
    return b

def iNon(val): # Check si la valeur passée en paramètre est nulle ou non...
    a = True
    if val == None:
        a = False
    return a

def trouveCase(case: str, bateau: object): # Cherche la position sur le plateau de la case passée en paramètre.
    y = 0
    a = False
    while y < len(bateau.proprio.base) and not a:
        x = 0
        while x < len(bateau.proprio.base[y]) and not a:
            if bateau.proprio.base[y][x] == case:
                a = True
            x = x + 1
        y = y + 1
    return [x-1, y-1]

def rempliListe(coo: list, position: list, bout: str, bateau: object): # Remplis la liste de position du bateau.
    if bout == 'av':
        mul = 1
    elif bout == 'ar':
        mul = -1
    for i in range(bateau.taille):
        if bateau.orient == 'h':
            a = coo[0]+(i)*mul+bateau.sens
            if a >= 0 and a <= 9:
                position.append(bateau.proprio.base[coo[1]][a])
            else:
                position.append(None)
        else:
            a = coo[1]+(i)*mul+bateau.sens
            if a >= 0 and a <= 9:
                position.append(bateau.proprio.base[a][coo[0]])
            else:
                position.append(None)
    if bout == 'ar':
        position.reverse()

def blocVert(bateau: object): # Désélectionne tout les bateaux à part celui qui vient d'être sélectionné.
    for i in range(len(liBat1)):
        if bateau != liBat1[i].nom:
            if liBat1[i].defil:
                liBat1[i].immobile()

# Brillant //////////////////////////////////////////////////////////////

def brillePlacement(bateau: object, liste: list):
    # Mets en évidence les cases où le bateau sélectionné se trouvera une fois relaché.
    fond.delete('Pharos')
    c = 'white'
    if None in bateau.pos:
        c = 'red'
    else:
        for j in range(len(liste)):
            if liste[j] != bateau and liste[j].pos != None:
                if not voisin(liste[j], bateau.pos):
                    c = 'red'
    for i in range(len(bateau.pos)):
        if bateau.pos[i] != None:
            a = fond.coords(bateau.pos[i])
            b = 'Pharo' + str(i+1)
            fond.create_rectangle(a[0], a[1], a[2], a[3], fill='', outline=c, width=4, tags=(b, 'Pharos'))
            fond.tag_raise(bateau.tag, 'Pharos')

def voisin(bateau: object, rep: list):
    # Vérifie si le bateau sélectionné n'empiète pas sur un autre bateau déjà placé.
    a = True
    i = 0
    while i < len(rep) and a:
        if rep[i] in bateau.pos:
            a = False
        i = i + 1
    return a

fond.tag_bind('valid', '<Button-1>', checkEtat)