from typing import Protocol

from game.game import Game
from game.move import Move


class Bot(Protocol):
    name: str

    def choose_turn(
        self,
        game: Game,
        dice: tuple[int, int],
    ) -> tuple[Move, ...] | None:
        ...
