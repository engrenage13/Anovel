class Bougeable:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.pos = (x, y)

    def deplace(self, x: int, y: int) -> None:
        self.setPos(self.pos[0]+x, self.pos[1]+y)

    def setPos(self, x: int, y: int) -> None:
        self.pos = (x, y)