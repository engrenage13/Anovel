from genericpath import exists
from os import listdir, remove

blacklist = (".git", ".gitignore", ".vscode", "__pycache__")
nomFichier = "sauvegarde.txt"

def estDossier(test: str) -> bool:
    if not "." in test:
        rep = True
    else:
        rep = False
    return rep

def fichierAPasScan(fichier: str) -> bool:
    fic = fichier.split(".")
    if fic[len(fic)-1] in ("py", "png", "otf") or fichier.lower() in ("readme.md", nomFichier.lower()):
        rep = True
    else:
        rep = False
    return rep

def fichierExiste() -> bool:
    if exists(f"systeme/{nomFichier}"):
        rep = True
    else:
        rep = False
    return rep

def genereListe(adresse: str) -> list:
    inili = listdir(adresse)
    i = 0
    while i < len(inili):
        if inili[i] in blacklist:
            del inili[i]
        elif estDossier(inili[i]):
            inili += genereListe(adresse+"/"+inili[i])
            del inili[i]
        elif fichierAPasScan(inili[i]):
            del inili[i]
        else:
            inili[i] = adresse+"/"+inili[i]
            i = i + 1
    return inili

def lecture(liste: list) -> str:
    rep = ""
    for i in range(len(liste)):
        rep += liste[i] + "\n"
        fichier = open(liste[i], 'r')
        rep += fichier.read()
        if i < len(liste)-1:
            rep += f"\n{'/'*30}\n"
    return rep

def trouveFichier(url: str) -> str:
    rep = ""
    contenu = lecture([f"systeme/{nomFichier}"])
    sauvegarde = contenu.split(f"\n{'/'*30}\n")
    i = 0
    trouve = False
    while i < len(sauvegarde) and not trouve:
        fichier = sauvegarde[i].split("\n")
        if i == 0:
            del fichier[0]
        titre = fichier[0]
        if titre == url:
            del fichier[0]
            rep = "\n".join(fichier)
            trouve = True
        else:
            i = i + 1
    return rep

def identique(url: str, fichier: str) -> bool:
    ref = open(url, 'r')
    if fichier == ref.read():
        rep = True
    else:
        rep = False
    ref.close()
    return rep

def verifSauvegarde() -> None:
    contenu = lecture(genereListe("./"))
    fichier = open(f"systeme/{nomFichier}", "w")
    fichier.write(contenu)
    fichier.close()

def scan() -> None:
    liste = genereListe("./")
    for i in range(len(liste)):
        data = trouveFichier(liste[i])
        if data != "":
            if not identique(liste[i], data):
                fichier = open(liste[i], "w")
                fichier.write(data)
                fichier.close()
        else:
            remove(liste[i])