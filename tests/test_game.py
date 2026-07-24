from random import Random

import pytest

from game.board import Board
from game.game import Game
from game.move import Move


def test_game_starts_with_player_one() -> None:
    game = Game()

    assert game.current_player == 1


def test_dice_rolls_are_between_one_and_six() -> None:
    game = Game(rng=Random(123))

    for _ in range(100):
        die_one, die_two = game.roll_dice()

        assert 1 <= die_one <= 6
        assert 1 <= die_two <= 6


def test_seeded_dice_are_reproducible() -> None:
    first_game = Game(rng=Random(123))
    second_game = Game(rng=Random(123))

    first_rolls = [first_game.roll_dice() for _ in range(10)]
    second_rolls = [second_game.roll_dice() for _ in range(10)]

    assert first_rolls == second_rolls


def test_player_one_wins_after_bearing_off_all_pieces() -> None:
    board = Board()
    board.player_one_off = 15

    game = Game(board=board)

    assert game.winner() == 1
    assert game.is_over()


def test_player_two_wins_after_bearing_off_all_pieces() -> None:
    board = Board()
    board.player_two_off = 15

    game = Game(board=board)

    assert game.winner() == -1
    assert game.is_over()


def test_game_without_winner_is_not_over() -> None:
    game = Game()

    assert game.winner() is None
    assert not game.is_over()


def test_play_turn_applies_moves_and_switches_player() -> None:
    board = Board()
    board.points[0] = 1

    game = Game(
        board=board,
        current_player=1,
    )

    turn = (
        Move(start=0, end=2, die_value=2),
        Move(start=2, end=5, die_value=3),
    )

    game.play_turn(
        dice=(2, 3),
        moves=turn,
    )

    assert game.board.points[0] == 0
    assert game.board.points[5] == 1
    assert game.current_player == -1


def test_illegal_turn_is_rejected_without_changing_board() -> None:
    board = Board()
    board.points[0] = 1

    game = Game(
        board=board,
        current_player=1,
    )

    original_points = game.board.points.copy()

    illegal_turn = (
        Move(start=0, end=4, die_value=4),
    )

    with pytest.raises(ValueError):
        game.play_turn(
            dice=(2, 3),
            moves=illegal_turn,
        )

    assert game.board.points == original_points
    assert game.current_player == 1


def test_player_can_pass_when_no_legal_turn_exists() -> None:
    board = Board()
    board.player_one_bar = 1

    for index in range(6):
        board.points[index] = -2

    game = Game(
        board=board,
        current_player=1,
    )

    game.pass_turn(dice=(2, 5))

    assert game.current_player == -1


def test_player_cannot_pass_when_legal_turn_exists() -> None:
    board = Board()
    board.points[0] = 1

    game = Game(
        board=board,
        current_player=1,
    )

    with pytest.raises(ValueError):
        game.pass_turn(dice=(2, 3))

    assert game.current_player == 1


def test_game_rejects_turn_after_game_is_over() -> None:
    board = Board()
    board.player_one_off = 15

    game = Game(board=board)

    with pytest.raises(ValueError):
        game.play_turn(
            dice=(2, 3),
            moves=(),
        )


def test_winning_turn_does_not_switch_player() -> None:
    board = Board()
    board.points[23] = 1
    board.player_one_off = 14

    game = Game(
        board=board,
        current_player=1,
    )

    winning_turn = (
        Move(start=23, end=None, die_value=1),
    )

    game.play_turn(
        dice=(1, 2),
        moves=winning_turn,
    )

    assert game.winner() == 1
    assert game.current_player == 1
