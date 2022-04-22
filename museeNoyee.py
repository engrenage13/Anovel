from FondMarin import hbarre, tailleCase, yf
from Image import Ima

# Interface
cruzoff = Ima('images/ui/CroSom.png')
croixSombre = cruzoff.reDim(hbarre*0.9, hbarre*0.9)
croixSombre = cruzoff.createPhotoImage(croixSombre)
cruzon = Ima('images/ui/CroLum.png')
croixLumineuse = cruzon.reDim(hbarre*0.9, hbarre*0.9)
croixLumineuse = cruzon.createPhotoImage(croixLumineuse)

# Marqueurs
croix = Ima('images/bataille/croix.png')
touche = croix.reDim(tailleCase, tailleCase)
touche = croix.createPhotoImage(touche)
loupe = Ima('images/bataille/loupe.png')
rate = loupe.reDim(tailleCase, tailleCase)
rate = loupe.createPhotoImage(rate)

# Environnement
env = Ima('images/envs/mer.png')
dimensions = env.getDimensions()
mer = env.reDim(prop=yf/dimensions[1])
mer = env.createPhotoImage(mer)