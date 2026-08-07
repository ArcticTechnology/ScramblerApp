from .scrambler import ScramblerAppHome
from .utils.base import Scrambler


def main():
    scrambler = Scrambler()

    app = ScramblerAppHome(scrambler)
    app.cmdloop()


if __name__ == '__main__':
    raise SystemExit(main())
