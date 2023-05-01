from systeme.FondMarin import *

# Interface
pointe = load_image('jeux/BN/images/ui/viseur.png')
image_resize(pointe, int(tailleCase*0.96), int(tailleCase*0.96))
viseur = load_texture_from_image(pointe)
unload_image(pointe)

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