import json

fichier = open("jeux/Jeu_1/config.json")
config = json.loads(fichier.read())

fichier = open("jeux/Jeu_1/data/joueurs.json")
joueurs = json.loads(fichier.read())

fichier = open("jeux/Jeu_1/data/bateaux.json")
bateaux = json.loads(fichier.read())