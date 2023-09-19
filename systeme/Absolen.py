from random import randint, choice
from verif import verifSauvegarde

NOM = "ABSOLEN"
VERSION = "1.1.3"

save = False
nbChiffre = 3
code = ""
for i in range(nbChiffre):
    code += str(randint(0, 9))
abandon = False
tentatives = 0
indices = []

print(f">>> Bienvenue sur {NOM} {VERSION} pour ANOVEL\n")

def indice() -> str:
    propositions = [i for i in range(7)]
    for i in range(len(indices)):
        del propositions[propositions.index(indices[i])]
    ind = choice(propositions)
    liste = []
    for i in range(len(code)):
        liste.append(int(code[i]))
    nbPaire = 0
    for i in range(len(liste)):
        if liste[i]%2 == 0:
            nbPaire += 1
    if ind == 0:
        rep = f"La somme de tous mes chiffres vaut : {liste[0]+liste[1]+liste[2]}."
    elif ind == 1:
        rep = f"La somme de mes 2 premiers chiffres vaut : {liste[0]+liste[1]}."
    elif ind == 2:
        rep = f"La somme de mon premier et mon dernier chiffres vaut : {liste[0]+liste[2]}."
    elif ind == 3:
        rep = f"La somme de mes 2 derniers chiffres vaut : {liste[1]+liste[2]}."
    elif ind == 4:
        rep = f"J'ai {nbPaire} chiffre(s) paire(s)."
    elif ind == 5:
        rep = f"J'ai {nbChiffre-nbPaire} chiffre(s) impaire(s)."
    elif ind == 6:
        nb = randint(0, nbChiffre-1)
        if nb == 0:
            position = "premmier"
        elif nb == 1:
            position = "second"
        else:
            position = "dernier"
        rep = f"Mon {position} est {code[nb]}."
    indices.append(ind)
    return rep

def saisieCode() -> bool:
    s = input(f"Code de sécurité ({nbChiffre} chiffres): ")
    if s == "Nacéo":
        print("Toujours cette vieille ruse...")
        rep = True
    elif len(s) == nbChiffre and s == code:
        print("Code Bon !")
        rep = True
    else:
        print("Code Erroné.")
        if tentatives > 0 and tentatives%3 == 0 and len(indices) < nbChiffre:
            i = indice()
            print(f"Petit indice : {i}")
        rep = False
    return rep

travail = input("Nouvelle sauvegarde ? [y] ")
if travail.lower() in ("y", "yes", "oui", "o", ""):
    trouve = saisieCode()
    tentatives = tentatives + 1
    while not trouve and not abandon:
        fin = choice([True]+[False]*9)
        if fin:
            bam = input("\nVeux-tu abandonner ?\n> ")
            if bam.lower() in ("y", "yes", "oui", "o"):
                abandon = True
        elif not abandon:
            trouve = saisieCode()
            tentatives = tentatives + 1
            if trouve:
                save = True

if not abandon and save:
    print(f"Code trouvé en {tentatives} tentatives et avec {len(indices)} indices.")
    verifSauvegarde()
    print("\nSauvegarde effectuée.")
print("\nAu revoir.")