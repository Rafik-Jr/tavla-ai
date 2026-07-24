"""Tests for the board module."""


def test_board_module_imports() -> None:
    from game import board

    assert board is not None


import pytest

from game.board import Board


def test_empty_board_has_24_points() -> None:
    board = Board()

    assert len(board.points) == 24
    assert board.points == [0] * 24


def test_starting_position_has_15_pieces_per_player() -> None:
    board = Board.starting_position()

    assert board.piece_count(1) == 15
    assert board.piece_count(-1) == 15


def test_player_one_can_move_forward_using_die() -> None:
    board = Board.starting_position()

    board.move_piece(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )

    assert board.points[0] == 1
    assert board.points[3] == 1
    assert board.piece_count(1) == 15


def test_invalid_player_is_rejected() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=2,
        start=0,
        end=3,
        die_value=3,
    )


def test_indexes_out_of_range_are_rejected() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=-1,
        end=3,
        die_value=3,
    )

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=24,
        die_value=3,
    )


def test_player_two_can_move_forward_using_die() -> None:
    board = Board.starting_position()

    board.move_piece(
        player=-1,
        start=23,
        end=20,
        die_value=3,
    )

    assert board.points[23] == -1
    assert board.points[20] == -1
    assert board.piece_count(-1) == 15


def test_player_one_can_capture_player_two_piece() -> None:
    board = Board()
    board.points[0] = 1
    board.points[3] = -1

    board.move_piece(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )

    assert board.points[0] == 0
    assert board.points[3] == 1
    assert board.player_two_bar == 1
    assert board.piece_count(1) == 1
    assert board.piece_count(-1) == 1


def test_player_two_can_capture_player_one_piece() -> None:
    board = Board()
    board.points[23] = -1
    board.points[20] = 1

    board.move_piece(
        player=-1,
        start=23,
        end=20,
        die_value=3,
    )

    assert board.points[23] == 0
    assert board.points[20] == -1
    assert board.player_one_bar == 1
    assert board.piece_count(1) == 1
    assert board.piece_count(-1) == 1


def test_player_one_cannot_move_backward() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=11,
        end=8,
        die_value=3,
    )


def test_player_two_cannot_move_backward() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=-1,
        start=12,
        end=15,
        die_value=3,
    )


def test_move_distance_must_match_die() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=4,
        die_value=3,
    )


def test_cannot_move_from_empty_point() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=1,
        end=4,
        die_value=3,
    )


def test_cannot_move_opponents_piece() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=23,
        end=20,
        die_value=3,
    )


def test_cannot_move_to_blocked_point() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=5,
        die_value=5,
    )


def test_point_with_one_opponent_piece_is_not_blocked() -> None:
    board = Board()
    board.points[0] = 1
    board.points[3] = -1

    assert board.is_simple_move_legal(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )


def test_player_one_cannot_land_on_two_opponent_pieces() -> None:
    board = Board()
    board.points[0] = 1
    board.points[3] = -2

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )


def test_player_two_cannot_land_on_two_opponent_pieces() -> None:
    board = Board()
    board.points[23] = -1
    board.points[20] = 2

    assert not board.is_simple_move_legal(
        player=-1,
        start=23,
        end=20,
        die_value=3,
    )


def test_invalid_die_value_is_rejected() -> None:
    board = Board.starting_position()

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=0,
        die_value=0,
    )

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=7,
        die_value=7,
    )


def test_illegal_move_does_not_change_board() -> None:
    board = Board.starting_position()
    original_points = board.points.copy()

    with pytest.raises(ValueError):
        board.move_piece(
            player=1,
            start=0,
            end=4,
            die_value=3,
        )

    assert board.points == original_points


def test_invalid_die_value_does_not_change_board() -> None:
    board = Board.starting_position()
    original_points = board.points.copy()

    with pytest.raises(ValueError):
        board.move_piece(
            player=1,
            start=0,
            end=1,
            die_value=0,
        )

    assert board.points == original_points


def test_piece_count_rejects_invalid_player() -> None:
    board = Board()

    with pytest.raises(ValueError):
        board.piece_count(2)