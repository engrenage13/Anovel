from systeme.FondMarin import *

# Interface
cruzoff = load_image('images/ui/CroSom.png')
image_resize(cruzoff, int(hbarre*0.9), int(hbarre*0.9))
croixSombre = load_texture_from_image(cruzoff)
unload_image(cruzoff)
cruzon = load_image('images/ui/CroLum.png')
image_resize(cruzon, int(hbarre*0.9), int(hbarre*0.9))
croixLumineuse = load_texture_from_image(cruzon)
unload_image(cruzon)
pointe = load_image('images/bataille/viseur.png')
image_resize(pointe, int(tailleCase*0.96), int(tailleCase*0.96))
viseur = load_texture_from_image(pointe)
unload_image(pointe)
fum = load_image("images/decors/vapeur.png")
prop = int(yf*0.06)/fum.height
image_resize(fum, int(fum.width*prop), int(fum.height*prop))
vapeurD = load_texture_from_image(fum)
image_flip_horizontal(fum)
vapeurG = load_texture_from_image(fum)
unload_image(fum)

# Marqueurs
marqueX = load_image('images/bataille/croix.png')
image_resize(marqueX, tailleCase, tailleCase)
croix = load_texture_from_image(marqueX)
unload_image(marqueX)
marqueO = load_image('images/bataille/rond.png')
image_resize(marqueO, tailleCase, tailleCase)
rond = load_texture_from_image(marqueO)
unload_image(marqueO)

# Environnement
env = load_image('images/envs/mer.png')
reduc = yf/env.height
image_resize(env, int(env.width*reduc), int(env.height*reduc))
mer = load_texture_from_image(env)
unload_image(env)