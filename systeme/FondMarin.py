from pyray import *
from raylib import TEXTURE_FILTER_TRILINEAR
from raylib.colors import *

TITRE_F = 'ANOVEL'
etatVersion = "alpha"
version = "0.2"

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
tailleCase = int(yf*0.084)

# barre - menu
hbarre = int(yf*0.05)

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