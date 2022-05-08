from pyray import *
from raylib.colors import *

TITRE_F = 'NAVALE'
etatVersion = "alpha"
version = "0.1.14"

init_window(get_monitor_width(0), get_monitor_height(0), TITRE_F)
set_target_fps(60)
toggle_fullscreen()

# Dimensions
xf = get_screen_width()
yf = get_screen_height()
tlatba = int((xf - yf*0.84)/2)
yp = int(yf*0.15)
origyp = int(yf*0.105)
pasApas = int(yf*0.05)
tailleCase = int(yf*0.84/10)

# barre - menu
hbarre = int(yf*0.05)

# polices
police1 = load_font('polices/STENCIL.ttf')
gen_texture_mipmaps([police1.texture])
police2 = load_font('polices/lilita.ttf')
gen_texture_mipmaps([police2.texture])
police3 = get_font_default()