from systeme.FondMarin import *
#from Image import Ima

# Interface
cruzoff = load_image('images/ui/CroSom.png')
image_resize(cruzoff, int(hbarre*0.9), int(hbarre*0.9))
croixSombre = load_texture_from_image(cruzoff)
cruzon = load_image('images/ui/CroLum.png')
image_resize(cruzon, int(hbarre*0.9), int(hbarre*0.9))
croixLumineuse = load_texture_from_image(cruzon)
#pointe = Ima('images/bataille/viseur.png')
#viseur = pointe.reDim(tailleCase*0.96, tailleCase*0.96)
#viseur = pointe.createPhotoImage(viseur)

# Marqueurs
#croix = Ima('images/bataille/croix.png')
#touche = croix.reDim(tailleCase, tailleCase)
#touche = croix.createPhotoImage(touche)
#loupe = Ima('images/bataille/loupe.png')
#rate = loupe.reDim(tailleCase, tailleCase)
#rate = loupe.createPhotoImage(rate)

# Environnement
env = load_image('images/envs/mer.png')
reduc = yf/env.height
image_resize(env, int(env.width*reduc), int(env.height*reduc))
mer = load_texture_from_image(env)