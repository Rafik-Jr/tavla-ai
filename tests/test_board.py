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