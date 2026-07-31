from dataclasses import dataclass
from random import Random

from game.board import Board
from game.game import Game
from game.move import Move


@dataclass
class HeuristicBot:
    name: str = "Heuristic Bot"
    rng: Random | None = None

    def choose_turn(
        self,
        game: Game,
        dice: tuple[int, int],
    ) -> tuple[Move, ...] | None:
        legal_turns = game.legal_turns(dice)
        if not legal_turns:
            return None

        scored_turns = [
            (self._score_turn(game.board, game.current_player, turn), turn)
            for turn in legal_turns
        ]
        highest_score = max(score for score, _ in scored_turns)
        best_turns = [
            turn for score, turn in scored_turns if score == highest_score
        ]

        if self.rng is not None:
            return self.rng.choice(best_turns)
        return best_turns[0]

    def _score_turn(
        self,
        board: Board,
        player: int,
        turn: tuple[Move, ...],
    ) -> float:
        before_opponent_bar = self._opponent_bar(board, player)
        before_own_off = self._own_off(board, player)
        after = board.copy()
        after.apply_turn(player=player, moves=turn)

        score = 0.0
        score += (self._opponent_bar(after, player) - before_opponent_bar) * 25.0
        score += (self._own_off(after, player) - before_own_off) * 40.0
        score += (self._pip_count(board, player) - self._pip_count(after, player)) * 1.0
        score += (self._made_points(after, player) - self._made_points(board, player)) * 6.0
        score += (self._blots(board, player) - self._blots(after, player)) * 4.0
        score += (self._home_board_pieces(after, player) - self._home_board_pieces(board, player)) * 2.0
        return score

    @staticmethod
    def _own_off(board: Board, player: int) -> int:
        return board.player_one_off if player == 1 else board.player_two_off

    @staticmethod
    def _opponent_bar(board: Board, player: int) -> int:
        return board.player_two_bar if player == 1 else board.player_one_bar

    @staticmethod
    def _pip_count(board: Board, player: int) -> int:
        total = 0
        for index, count in enumerate(board.points):
            if player == 1 and count > 0:
                total += count * (24 - index)
            elif player == -1 and count < 0:
                total += abs(count) * (index + 1)
        return total + (board.player_one_bar if player == 1 else board.player_two_bar) * 25

    @staticmethod
    def _made_points(board: Board, player: int) -> int:
        if player == 1:
            return sum(count >= 2 for count in board.points)
        return sum(count <= -2 for count in board.points)

    @staticmethod
    def _blots(board: Board, player: int) -> int:
        target = 1 if player == 1 else -1
        return sum(count == target for count in board.points)

    @staticmethod
    def _home_board_pieces(board: Board, player: int) -> int:
        if player == 1:
            return sum(count for count in board.points[18:24] if count > 0)
        return sum(abs(count) for count in board.points[:6] if count < 0)
