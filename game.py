import curses
import enum
import random
from typing import Optional, Self, Tuple

from coordinate import Coordinate
from snake import Snake


class Animation(enum.StrEnum):
    BLANK = '-'
    SNAKE_HEAD = 'H'
    SNAKE_BODY = 'S'
    FRUIT = 'F'


class Game:
    x_range = 15
    y_range = 15
    directions = enum.Enum(
        'Directions',
        {'UP': curses.KEY_UP, 'DOWN': curses.KEY_DOWN, 'RIGHT': curses.KEY_RIGHT, 'LEFT': curses.KEY_LEFT}
    )

    class AteYourself(Exception):
        pass

    class OutOfBounds(Exception):
        pass

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr

        self.grid = []
        for _ in range(self.y_range):
            self.grid.append([Animation.BLANK.value for i in range(self.x_range)])

        self.fruit = self.generate_fruit()

        head = Coordinate(self.x_range // 2, self.y_range // 2)
        self.snake = Snake(head, self.directions)

        self.animate_board()

    def get_user_input(self, timeout: int) -> Optional[str]:
        self.stdscr.timeout(timeout)
        user_input = self.stdscr.getch()
        return user_input if user_input in [i.value for i in self.directions] else None

    def print_board(self) -> str:
        self.stdscr.clear()
        board = ''
        for i in self.grid:
            board = f'{board}\n{i}'

        self.stdscr.addstr(0, 0, board)
        self.stdscr.refresh()

    def update_grid(self, location: Coordinate, symbol: str) -> None:
        # Yes. I am aware this is backwards...
        self.grid[location.y][location.x] = symbol

    def play(self) -> None:
        user_input = curses.KEY_RIGHT
        while True:
            user_input = self.get_user_input(150) or user_input
            direction = self.directions(user_input)

            self.move(direction)
            self.print_board()

    def move(self, direction: enum.Enum) -> None:
        next_movement = self.snake.get_next_movement(direction)

        if self.out_of_bounds(next_movement):
            raise self.OutOfBounds()

        if self.snake.ate_self(next_movement):
            raise self.AteYourself()

        ate_fruit = False
        if next_movement == self.fruit:
            ate_fruit = True

        empty_space = self.snake.move(next_movement, ate_fruit)

        if ate_fruit:
            self.fruit = self.generate_fruit()

        self.animate_board(empty_space)

    def out_of_bounds(self, next_move: Coordinate) -> bool:
        if next_move.x < 0:
            return True
        elif next_move.x >= self.x_range:
            return True
        elif next_move.y < 0:
            return True
        elif next_move.y >= self.y_range:
            return True

        return False

    def animate_board(self, removed: Optional[Coordinate] = None) -> None:
        if removed:
            self.update_grid(removed, Animation.BLANK.value)

        for segment in self.snake.body:
            self.update_grid(segment, Animation.SNAKE_BODY.value)
        self.update_grid(self.snake.head, Animation.SNAKE_HEAD.value)

        self.update_grid(self.fruit, Animation.FRUIT.value)

    def generate_fruit(self) -> Coordinate:
        open_spaces = []
        for y, _ in enumerate(self.grid):
            for x, _ in enumerate(self.grid[y]):
                # Sigh. More backwardsness....
                if self.grid[y][x] == '-':
                    open_spaces.append(Coordinate(x, y))

        return random.choice(open_spaces)

    def reset(self) -> None:
        self.fruit = None

        for y, _ in enumerate(self.grid):
            for x, _ in enumerate(self.grid[y]):
                self.update_grid(Coordinate(x, y), Animation.BLANK.value)

        self.fruit = self.generate_fruit()

        head = Coordinate(self.x_range // 2, self.y_range // 2)
        self.snake.reset(head)

        self.animate_board()
