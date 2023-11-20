import enum
from typing import Optional, Self

from coordinate import Coordinate


class Snake:
    def __init__(self, coord: Coordinate, directions: enum.Enum) -> None:
        self.body = [coord, ]
        self.head = self.body[0]

        self.directions = directions

    def __repr__(self) -> str:
        return f'{self.body}'

    def move(self, new_location: Coordinate, ate_fruit: bool) -> Optional[Coordinate]:
        self.body.append(new_location)

        old_head = None if ate_fruit else self.body.pop(0)

        self.head = self.body[-1]
        return old_head

    def ate_self(self, new_location: Coordinate) -> bool:
        return new_location in self.body

    def get_next_movement(self, direction: enum.Enum) -> Self:
        match direction:
            case self.directions.UP:
                return Coordinate(self.head.x, self.head.y - 1)
            case self.directions.DOWN:
                return Coordinate(self.head.x, self.head.y + 1)
            case self.directions.RIGHT:
                return Coordinate(self.head.x + 1, self.head.y)
            case self.directions.LEFT:
                return Coordinate(self.head.x - 1, self.head.y)

    def reset(self, coord: Coordinate) -> None:
        self.body = [coord, ]
        self.head = self.body[0]
