from random import Random

from bots.random_bot import RandomBot
from game.board import Board
from game.game import Game


def test_random_bot_returns_legal_turn() -> None:
    board = Board()
    board.points[0] = 1

    game = Game(
        board=board,
        current_player=1,
    )

    bot = RandomBot(
        name="Test Bot",
        rng=Random(123),
    )

    dice = (2, 3)

    selected_turn = bot.choose_turn(
        game=game,
        dice=dice,
    )

    assert selected_turn is not None
    assert selected_turn in game.legal_turns(dice)


def test_random_bot_returns_none_when_no_turn_exists() -> None:
    board = Board()
    board.player_one_bar = 1

    for index in range(6):
        board.points[index] = -2

    game = Game(
        board=board,
        current_player=1,
    )

    bot = RandomBot(
        name="Test Bot",
        rng=Random(123),
    )

    selected_turn = bot.choose_turn(
        game=game,
        dice=(2, 5),
    )

    assert selected_turn is None


def test_seeded_random_bot_is_reproducible() -> None:
    first_game = Game()
    second_game = Game()

    first_bot = RandomBot(
        name="First",
        rng=Random(123),
    )

    second_bot = RandomBot(
        name="Second",
        rng=Random(123),
    )

    first_choice = first_bot.choose_turn(
        game=first_game,
        dice=(2, 3),
    )

    second_choice = second_bot.choose_turn(
        game=second_game,
        dice=(2, 3),
    )

    assert first_choice == second_choice
