from systeme.FondMarin import *

DISTANCEPOINTS = int(yf*0.01)
TAILLECASE = int(xf*0.13)
TAILLEPETITECASE = int(xf*0.035)
EAUX = [[48, 201, 201, 255], [48, 140, 201, 255], [29, 79, 171, 255]]

def definiRect(centre: tuple|list, dest: tuple|list) -> list:
    rect = []
    if centre[0] <= dest[0]:
        rect.append(centre[0])
        if centre[1] <= dest[1]:
            rect += [centre[1], dest[0], dest[1]]
        else:
            rect += [dest[1], dest[0], centre[1]]
    else:
        rect.append(dest[0])
        if centre[1] <= dest[1]:
            rect += [centre[1], centre[0], dest[1]]
        else:
            rect += [dest[1], centre[0], centre[1]]
    return rect

def getCote(centre: tuple|list, rectangle: list) -> int:
    if centre[0] == rectangle[0]:
        if centre[1] == rectangle[1]:
            return 1
        else:
            return 4
    else:
        if centre[1] == rectangle[1]:
            return 2
        else:
            return 3

def definiSpectre(pos: tuple|list, objet) -> list:
    return [int(pos[0]-objet.image.width), int(pos[1]-objet.image.height), objet.image.width, objet.image.height]

def deplacePoint(point: tuple|list, destination: tuple|list, sens: int) -> tuple:
    pt = [point[0], point[1]]
    if sens == 1:
        if pt[0] < destination[0]:
            pt[0] += DISTANCEPOINTS
        if pt[1] < destination[1]:
            pt[1] += DISTANCEPOINTS
    elif sens == 2:
        if pt[0] > destination[0]:
            pt[0] -= DISTANCEPOINTS
        if pt[1] < destination[1]:
            pt[1] += DISTANCEPOINTS
    elif sens == 3:
        if pt[0] > destination[0]:
            pt[0] -= DISTANCEPOINTS
        if pt[1] > destination[1]:
            pt[1] -= DISTANCEPOINTS
    else:
        if pt[0] < destination[0]:
            pt[0] += DISTANCEPOINTS
        if pt[1] > destination[1]:
            pt[1] -= DISTANCEPOINTS
    return (pt[0], pt[1])

def checkContactObstacle(rectangle: list, obstacles: list, actuel) -> bool:
    rep = False
    i = 0
    while i < len(obstacles) and not rep:
        spectre = definiSpectre(obstacles[i].pos, obstacles[i])
        if check_collision_recs(rectangle, spectre) and obstacles[i] != actuel:
            rep = True
        else:
            i += 1
    return rep

def modifDestination(destination: list, objet, obstacles: list) -> tuple:
    ok = True
    pos = objet.pos
    precedent = pos
    coin = getCote(objet.pos, definiRect(objet.pos, destination))
    while ok:
        if checkContactObstacle(definiSpectre(pos, objet), obstacles, objet):
            ok = False
        else:
            precedent = pos[:]
            pos = deplacePoint(pos, destination, coin)
            if pos == precedent:
                ok = False
    return precedent