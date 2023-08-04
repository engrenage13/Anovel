def glisse(position: tuple[int], destination: tuple[int], vitesse: int = 1) -> tuple[int]:
    """Permet d'effectuer un déplacement d'un élément vers sa destination.

    Args:
        position (tuple[int]): La position initiale de l'émément
        destination (tuple[int]): L'endroit où il veut aller
        vitesse (int, optional): Sa vitesse de déplacement en pixel/déplacement. Defaults to 1.

    Returns:
        tuple[int]: La nouvelle position de l'élément.
    """
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
    """Limite la valeur du déplacement si la distance est insuffisante.

    Args:
        Args:
        position (tuple[int]): La position initiale de l'émément
        destination (tuple[int]): L'endroit où il veut aller
        vitesse (int, optional): Sa vitesse de déplacement en pixel/déplacement.

    Returns:
        int: Le nouveau déplacement calculé.
    """
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