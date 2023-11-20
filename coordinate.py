from typing import Self

class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y
