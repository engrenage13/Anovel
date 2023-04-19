def glisse(position: tuple[int], destination: tuple[int], vitesse: int = 1) -> tuple[int]:
    x = position[0]
    y = position[1]
    dx = destination[0]
    dy = destination[1]
    vitx = regleVitesse(x, dx, vitesse)
    vity = regleVitesse(y, dy, vitesse)
    if x < dx:
        x += vitx
    elif x > dx:
        x -= vitx
    if y < dy:
        y += vity
    elif y > dy:
        y -= vity
    return (x, y)

def regleVitesse(position: int, destination: int, vitesse: int) -> int:
    vit = vitesse
    if position < destination:
        if destination-position < vitesse:
            vit = destination-position
    elif position > destination:
        if position-destination < vitesse:
            vit = position-destination
    else:
        vit = 0
    return vit