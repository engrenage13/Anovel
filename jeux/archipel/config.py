import json

fichier = open("jeux/archipel/config.json")
config = json.loads(fichier.read())

fichier = open("jeux/archipel/data/joueurs.json")
joueurs = json.loads(fichier.read())

fichier = open("jeux/archipel/data/bateaux.json")
bateaux = json.loads(fichier.read())