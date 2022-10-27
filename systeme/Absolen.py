from random import randint, choice
from verif import sauvegarde

save = False
code = ""
for i in range(3):
    code += str(randint(0, 9))
abandon = False
tentatives = 0
indices = []

print(">>> Bienvenue sur ABSOLEN pour ANOVEL")

def indice() -> str:
    propositions = [i for i in range(7)]
    for i in range(len(indices)):
        del propositions[propositions.index(indices[i][0])]
    ind = choice(propositions)
    nbPaire = 0
    for i in range(len(code)):
        if int(code[i])%2 == 0:
            nbPaire += 1
    if ind == 0:
        rep = f"La somme de tous mes chiffres vaut : {int(code[0])+int(code[1])+int(code[2])}."
    elif ind == 1:
        rep = f"La somme de mes 2 premiers chiffres vaut : {int(code[0])+int(code[1])}."
    elif ind == 2:
        rep = f"La somme de mes 2 derniers chiffres vaut : {int(code[1])+int(code[2])}."
    elif ind == 3:
        rep = f"La somme de mon premier et de mon dernier chiffre vaut : {int(code[0])+int(code[2])}."
    elif ind == 4:
        rep = f"J'ai {nbPaire} chiffres paires."
    elif ind == 5:
        rep = f"J'ai {3-nbPaire} chiffres impaires."
    elif ind == 6:
        nb = randint(0, 2)
        if nb == 0:
            position = "premmier"
        elif nb == 1:
            position = "second"
        else:
            position = "dernier"
        rep = f"Mon {position} est {code[nb]}."
    indices.append([ind])
    return rep

def saisieCode() -> bool:
    s = input("Code de sécurité (3 chiffres): ")
    if s == "Nacéo":
        print("Toujours cette vieille ruse...")
        rep = True
    elif len(s) == 3 and s == code:
        print("Code Bon !")
        rep = True
    else:
        print("Code Erroné.")
        if tentatives > 0 and tentatives%3 == 0 and len(indices) < 3:
            i = indice()
            print(f"Petit indice : {i}")
            indices[len(indices)-1].append(i)
        rep = False
    return rep

travail = input("Nouvelle sauvegarde ? [y] ")
if travail.lower() in ("y", "yes", "oui", "o", ""):
    trouve = saisieCode()
    tentatives = tentatives + 1
    while not trouve and not abandon:
        abandon = input("Annuler ? [n] ")
        if abandon.lower() in ("n", "no", "non", ""):
            trouve = saisieCode()
            tentatives = tentatives + 1
            if trouve:
                save = True
        else:
            abandon = True

if not abandon and save:
    print(f"Code trouvé en {tentatives} tentatives et avec {len(indices)} indices.")
    sauvegarde()
    print("Sauvegarde effectuée.")
print("Au revoir.")