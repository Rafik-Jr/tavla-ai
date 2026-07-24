from random import Random

from bots.random_bot import RandomBot
from game.board import Board
from game.game import Game
from game.runner import play_game


def test_runner_finishes_near_complete_game() -> None:
    board = Board()

    board.points[23] = 1
    board.player_one_off = 14

    board.points[0] = -1
    board.player_two_off = 14

    game = Game(
        board=board,
        current_player=1,
        rng=Random(42),
    )

    player_one_bot = RandomBot(
        name="Player One Bot",
        rng=Random(1),
    )

    player_two_bot = RandomBot(
        name="Player Two Bot",
        rng=Random(2),
    )

    result = play_game(
        game=game,
        player_one_bot=player_one_bot,
        player_two_bot=player_two_bot,
        max_turns=100,
    )

    assert result.winner in (1, -1)
    assert result.turns_played > 0


def test_runner_reports_player_one_win() -> None:
    board = Board()

    board.points[23] = 1
    board.player_one_off = 14

    board.points[0] = -15

    game = Game(
        board=board,
        current_player=1,
        rng=Random(1),
    )

    player_one_bot = RandomBot(
        name="Player One Bot",
        rng=Random(1),
    )

    player_two_bot = RandomBot(
        name="Player Two Bot",
        rng=Random(2),
    )

    result = play_game(
        game=game,
        player_one_bot=player_one_bot,
        player_two_bot=player_two_bot,
        max_turns=100,
    )

    assert result.winner == 1
