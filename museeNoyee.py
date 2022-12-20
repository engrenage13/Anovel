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
paraoff = load_image('images/ui/RouSom.png')
image_resize(paraoff, int(hbarre*0.9), int(hbarre*0.9))
rouageSombre = load_texture_from_image(paraoff)
unload_image(paraoff)
paraon = load_image('images/ui/RouLum.png')
image_resize(paraon, int(hbarre*0.9), int(hbarre*0.9))
rouageLumineux = load_texture_from_image(paraon)
unload_image(paraon)
fum = load_image("images/decors/vapeur.png")
prop = int(yf*0.06)/fum.height
image_resize(fum, int(fum.width*prop), int(fum.height*prop))
vapeurD = load_texture_from_image(fum)
image_flip_horizontal(fum)
vapeurG = load_texture_from_image(fum)
unload_image(fum)

# Erreurs
poiscaille = load_image('images/decors/arretedor.png')
prop = int(yf*0.17)/poiscaille.height
image_resize(poiscaille, int(poiscaille.width*prop), int(poiscaille.height*prop))
cadreCodeErreur = load_texture_from_image(poiscaille)
unload_image(poiscaille)
demon = load_image('images/decors/cauchemar.png')
prop = int(yf*0.12)/demon.height
image_resize(demon, int(demon.width*prop), int(demon.height*prop))
cauchemar = load_texture_from_image(demon)
unload_image(demon)