from genericpath import exists
from os import listdir, remove

blacklist = (".git", ".gitignore", ".vscode", "__pycache__")
nomFichier = "sauvegarde.txt"
fichierQuiFautPasToucher = ("py", "png", "otf", "ico", "json")

def estDossier(test: str) -> bool:
    """Vérifie si l'élément passé en paramètre est un dossier.

    Args:
        test (str): Le chemin de l'élément testé.

    Returns:
        bool: True si c'est un dossier.
    """
    if not "." in test:
        rep = True
    else:
        rep = False
    return rep

def fichierAPasScan(fichier: str) -> bool:
    """Vérifie si le fichier ne doit pas être scanné.

    Args:
        fichier (str): Le fichier testé.

    Returns:
        bool: True s'il ne doit pas être scanné.
    """
    fic = fichier.split(".")
    if fic[len(fic)-1] in fichierQuiFautPasToucher or fichier.lower() in ("readme.md", nomFichier.lower()):
        rep = True
    else:
        rep = False
    return rep

def fichierExiste() -> bool:
    """Vérifie le fichier système existe.

    Returns:
        bool: True s'il existe.
    """
    if exists(f"systeme/{nomFichier}"):
        rep = True
    else:
        rep = False
    return rep

def genereListe(adresse: str) -> list:
    """Genere la liste des sauvegardes de fichier.

    Args:
        adresse (str): L'adresse du fichier a sauvegarder.

    Returns:
        list: Liste des adresses.
    """
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
    """Lis les sauvegardes.

    Args:
        liste (list): Sauvegardes à lire.

    Returns:
        str: La sauvegarde lue.
    """
    rep = ""
    for i in range(len(liste)):
        rep += liste[i] + "\n"
        fichier = open(liste[i], 'r')
        rep += fichier.read()
        if i < len(liste)-1:
            rep += f"\n{'/'*30}\n"
    return rep

def trouveFichier(url: str) -> str:
    """Trouve un fichier particulier.

    Args:
        url (str): Le chemin du fichier recherché.

    Returns:
        str: Le contenu du fichier trouvé.
    """
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
    """Compare deux fichiers pour juger s'ils sont identiques.

    Args:
        url (str): Chemin du fichier à trouver.
        fichier (str): Fichier avec lequel il est comparé.

    Returns:
        bool: True s'ils sont identiques.
    """
    ref = open(url, 'r')
    if fichier == ref.read():
        rep = True
    else:
        rep = False
    ref.close()
    return rep

def verifSauvegarde() -> None:
    """Vérifie qu'il y a bien une sauvegarde.
    """
    contenu = lecture(genereListe("./"))
    fichier = open(f"systeme/{nomFichier}", "w")
    fichier.write(contenu)
    fichier.close()

def scan() -> None:
    """Vérifie l'ensemble des fichiers sauvegardés pour voir s'ils sont conformes à leurs sauvegardes.
    """
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