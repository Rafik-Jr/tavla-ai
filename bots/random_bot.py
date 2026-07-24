from dataclasses import dataclass, field
from random import Random

from game.game import Game
from game.move import Move


@dataclass
class RandomBot:
    name: str
    rng: Random = field(default_factory=Random)

    def choose_turn(
        self,
        game: Game,
        dice: tuple[int, int],
    ) -> tuple[Move, ...] | None:
        """
        Choose one legal turn randomly.

        Return None when no legal turn exists.
        """

        legal_turns = game.legal_turns(dice)

        if not legal_turns:
            return None

        return self.rng.choice(legal_turns)
