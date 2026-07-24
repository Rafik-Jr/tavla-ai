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


def test_starting_position_has_no_pieces_on_bar() -> None:
    board = Board.starting_position()

    assert board.player_one_bar == 0
    assert board.player_two_bar == 0


def test_starting_position_has_no_borne_off_pieces() -> None:
    board = Board.starting_position()

    assert board.player_one_off == 0
    assert board.player_two_off == 0


def test_piece_count_rejects_invalid_player() -> None:
    board = Board()

    with pytest.raises(ValueError):
        board.piece_count(2)


def test_player_one_can_move_to_empty_point() -> None:
    board = Board.starting_position()

    board.move_piece(player=1, start=0, end=1)

    assert board.points[0] == 1
    assert board.points[1] == 1
    assert board.piece_count(1) == 15


def test_player_two_can_move_to_empty_point() -> None:
    board = Board.starting_position()

    board.move_piece(player=-1, start=23, end=22)

    assert board.points[23] == -1
    assert board.points[22] == -1
    assert board.piece_count(-1) == 15


def test_cannot_move_from_empty_point() -> None:
    board = Board.starting_position()

    with pytest.raises(ValueError):
        board.move_piece(player=1, start=1, end=2)


def test_cannot_move_opponents_piece() -> None:
    board = Board.starting_position()

    with pytest.raises(ValueError):
        board.move_piece(player=1, start=23, end=22)


def test_cannot_move_to_point_with_opponent_pieces() -> None:
    board = Board.starting_position()

    with pytest.raises(ValueError):
        board.move_piece(player=1, start=0, end=5)


def test_move_rejects_invalid_board_indexes() -> None:
    board = Board.starting_position()

    with pytest.raises(ValueError):
        board.move_piece(player=1, start=-1, end=1)

    with pytest.raises(ValueError):
        board.move_piece(player=1, start=0, end=24)