from random import randint, choice
from FondMarin import fond, xf, yf, gris, mer

def plusDeTuile() -> None:
    fond.delete('tuile')

def quadriDeco(couleurs: list = [gris]+mer, tagVerif: str = 'accueil') -> None:
    chance = [0]*2 + [1]*1
    fait = choice(chance)
    if fait:
        indi = randint(1, 10)
        a = 'tuile' + str(indi)
        fond.delete(a)
        t = randint(int(yf/40), int(yf/20))
        x = randint(0, xf-t)
        y = randint(0, yf-t)
        fond.create_rectangle(x, y, x+t, y+t, fill=choice(couleurs), tags=(a, 'tuile'))
        fond.tag_lower('tuile', 'plafDec')
    b = fond.find_withtag(tagVerif)
    if len(b) > 0:
        tmp = randint(50, 100)
        fond.after(tmp, quadriDeco, couleurs, tagVerif)
    else:
        plusDeTuile()