from systeme.FondMarin import *

def viseur() -> tuple:
    X = get_mouse_x()
    Y = get_mouse_y()
    return (X, Y)

def check_obstacle(trajectoire: Rectangle, obstacles: list) -> int:
    obs = False
    i = 0