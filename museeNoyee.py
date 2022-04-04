from FondMarin import hbarre
from Image import Ima

cruzoff = Ima('images/CroSom.png')
croixSombre = cruzoff.reDim(hbarre*0.9, hbarre*0.9)
croixSombre = cruzoff.createPhotoImage(croixSombre)
cruzon = Ima('images/CroLum.png')
croixLumineuse = cruzon.reDim(hbarre*0.9, hbarre*0.9)
croixLumineuse = cruzon.createPhotoImage(croixLumineuse)