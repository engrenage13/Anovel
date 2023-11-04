from systeme.FondMarin import *

# Interface
fum = load_image("images/decors/vapeur.png")
prop = int(yf*0.06)/fum.height
image_resize(fum, int(fum.width*prop), int(fum.height*prop))
vapeurD = load_texture_from_image(fum)
image_flip_horizontal(fum)
vapeurG = load_texture_from_image(fum)
unload_image(fum)

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