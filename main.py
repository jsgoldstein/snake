import curses

from game import Game


def play(stdscr):
    stdscr.clear()

    game = Game(stdscr)

    while True:
        try:
            game.play()
        except Game.AteYourself:
            message = "Oh no! You ate youself.\n\n"
        except Game.OutOfBounds:
            message = "Oopsies. You went out of bounds.\n\n"
        finally:
            stdscr.clear()
            stdscr.addstr(0, 0, message)
            stdscr.addstr(5, 0, "Continue? (y/n).\n")
            stdscr.refresh()

        stdscr.timeout(10000)
        play_again = stdscr.getch()
        if chr(play_again) != 'y':
            break
        game.reset()


if __name__ == "__main__":
    curses.wrapper(play)
