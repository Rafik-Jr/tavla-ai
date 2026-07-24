from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

from game.board import Board
from game.move import Move


@dataclass
class Game:
    board: Board = field(default_factory=Board.starting_position)
    current_player: int = 1
    rng: Random = field(default_factory=Random)

    def roll_dice(self) -> tuple[int, int]:
        return (
            self.rng.randint(1, 6),
            self.rng.randint(1, 6),
        )

    def winner(self) -> int | None:
        if self.board.player_one_off == 15:
            return 1

        if self.board.player_two_off == 15:
            return -1

        return None

    def is_over(self) -> bool:
        return self.winner() is not None

    def legal_turns(
        self,
        dice: tuple[int, int],
    ) -> list[tuple[Move, ...]]:
        die_one, die_two = dice

        return self.board.legal_turns(
            player=self.current_player,
            die_one=die_one,
            die_two=die_two,
        )

    def play_turn(
        self,
        dice: tuple[int, int],
        moves: tuple[Move, ...],
    ) -> None:
        if self.is_over():
            raise ValueError("Game is already over")

        legal_turns = self.legal_turns(dice)

        candidate_board = self.board.copy()

        try:
            candidate_board.apply_turn(
                player=self.current_player,
                moves=moves,
            )
        except ValueError as exc:
            raise ValueError("Illegal turn") from exc

        if not (
            candidate_board.player_one_off == 15
            or candidate_board.player_two_off == 15
        ) and moves not in legal_turns:
            raise ValueError("Illegal turn")

        self.board = candidate_board

        if not self.is_over():
            self.current_player *= -1

    def pass_turn(self, dice: tuple[int, int]) -> None:
        if self.is_over():
            raise ValueError("Game is already over")

        if self.legal_turns(dice):
            raise ValueError("Cannot pass when a legal turn exists")

        self.current_player *= -1
