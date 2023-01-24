from systeme.FondMarin import *

# Interface
pointe = load_image('jeux/BN/images/ui/viseur.png')
image_resize(pointe, int(tailleCase*0.96), int(tailleCase*0.96))
viseur = load_texture_from_image(pointe)
unload_image(pointe)

# Décors
deco1 = load_image('jeux/BN/images/ui/coraux.png')
ratio = int(xf*0.16)/deco1.width
image_resize(deco1, int(deco1.width*ratio), int(deco1.height*ratio))
corail1 = load_texture_from_image(deco1)
image_flip_vertical(deco1)
corail2 = load_texture_from_image(deco1)
unload_image(deco1)
deco2 = load_image('images/decors/poissons.png')
ratio = int(tailleCase*1.2)/deco2.height
image_resize(deco2, int(deco2.width*ratio), int(deco2.height*ratio))
poisson = load_texture_from_image(deco2)
unload_image(deco2)

# Marqueurs
marqueX = load_image('jeux/BN/images/ui/croix.png')
image_resize(marqueX, tailleCase, tailleCase)
croix = load_texture_from_image(marqueX)
unload_image(marqueX)
marqueO = load_image('jeux/BN/images/ui/rond.png')
image_resize(marqueO, tailleCase, tailleCase)
rond = load_texture_from_image(marqueO)
unload_image(marqueO)

# Environnement
env = load_image('jeux/BN/images/envs/mer.png')
reduc = yf/env.height
image_resize(env, int(env.width*reduc), int(env.height*reduc))
mer = load_texture_from_image(env)
unload_image(env)