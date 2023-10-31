import json
from pyray import *
from raylib import TEXTURE_FILTER_TRILINEAR
from raylib.colors import *
from ui.bouton.taille import Taille
from ui.bouton.apparence import Apparence

# Configuration système
fichier = open("systeme/config.json")
config_sys = json.loads(fichier.read())
fichier.close()

init_window(get_monitor_width(0), get_monitor_height(0), config_sys["nom"])
set_target_fps(60)
toggle_fullscreen()
set_exit_key(0)

# Dimensions
xf = get_screen_width()
yf = get_screen_height()
tlatba = int((xf - yf*0.84)/2)
yp = int(yf*0.15)
origyp = int(yf*0.105)
pasApas = int(yf*0.05)
tailleCase = int(yf*0.084)

hbarre = int(yf*0.05)

espaceBt = int(xf*0.003)

# polices
police1 = load_font('polices/Roboto-Bold.otf')
gen_texture_mipmaps([police1.texture])
set_texture_filter(police1.texture, TEXTURE_FILTER_TRILINEAR)
police1i = load_font('polices/Roboto-BoldItalic.otf')
gen_texture_mipmaps([police1i.texture])
set_texture_filter(police1i.texture, TEXTURE_FILTER_TRILINEAR)
police2 = load_font('polices/Roboto-Regular.otf')
gen_texture_mipmaps([police2.texture])
set_texture_filter(police2.texture, TEXTURE_FILTER_TRILINEAR)
police2i = load_font('polices/Roboto-Italic.otf')
gen_texture_mipmaps([police2i.texture])
set_texture_filter(police2i.texture, TEXTURE_FILTER_TRILINEAR)
police3 = load_font('polices/Roboto-Light.otf')
gen_texture_mipmaps([police3.texture])
set_texture_filter(police3.texture, TEXTURE_FILTER_TRILINEAR)
police3i = load_font('polices/Roboto-LightItalic.otf')
gen_texture_mipmaps([police3i.texture])
set_texture_filter(police3i.texture, TEXTURE_FILTER_TRILINEAR)

# -- Boutons
# Tailles
TB1o = Taille(int(yf*0.07), True)
TB1n = Taille(int(yf*0.07), False)
TB2o = Taille(int(yf*0.05), True)
TB2n = Taille(int(yf*0.05), False)

# Apparences
PTIBT1 = Apparence([[255, 255, 255, 70], [255, 255, 255, 130]], police2, 1, False)
PTIBT2 = Apparence([[0, 0, 0, 70], [0, 0, 0, 150]], police2, 1, False)
PTIBT3 = Apparence([[225, 225, 225, 255], WHITE], police2, 1, False)
PTIBT4 = Apparence([[0, 0, 0, 225], [0, 0, 0, 255]], police2, 1, False)
BTNOIR = Apparence([[0, 0, 0, 70], [0, 0, 0, 150]], police2, 1, True)
BTV = Apparence([[18, 82, 219, 255]], police2, 1, True)
BTX = Apparence([[207, 35, 41, 255]], police2, 1, True)
BTDANGER = Apparence([[118, 33, 33, 100], [151, 31, 31, 100]], police2, 1, True)
BTANNULE = Apparence([[118, 33, 33, 200], [151, 31, 31, 200]], police2, 1, False)
BTDEV = Apparence([[237, 206, 104, 200], [233, 190, 47, 200]], police2, 1, False)
