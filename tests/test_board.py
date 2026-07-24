"""Tests for the board module."""
import game.board
import game


def test_board_module_imports() -> None:
    from game import board

    assert board is not None


import pytest

from game.board import Board
from game.move import Move


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


def test_board_copy_is_independent() -> None:
    board = Board()
    board.points[0] = 1

    copied_board = board.copy()
    copied_board.points[0] = 0
    copied_board.points[3] = 1

    assert board.points[0] == 1
    assert board.points[3] == 0


def test_generate_player_one_legal_moves_for_die() -> None:
    board = Board()
    board.points[0] = 1
    board.points[4] = 2

    moves = board.legal_moves_for_die(
        player=1,
        die_value=3,
    )

    assert moves == [
        Move(start=0, end=3, die_value=3),
        Move(start=4, end=7, die_value=3),
    ]


def test_generate_player_two_legal_moves_for_die() -> None:
    board = Board()
    board.points[23] = -1
    board.points[19] = -2

    moves = board.legal_moves_for_die(
        player=-1,
        die_value=3,
    )

    assert moves == [
        Move(start=19, end=16, die_value=3),
        Move(start=23, end=20, die_value=3),
    ]


def test_blocked_moves_are_not_generated() -> None:
    board = Board()
    board.points[0] = 1
    board.points[3] = -2

    moves = board.legal_moves_for_die(
        player=1,
        die_value=3,
    )

    assert moves == []


def test_capture_move_is_generated() -> None:
    board = Board()
    board.points[0] = 1
    board.points[3] = -1

    moves = board.legal_moves_for_die(
        player=1,
        die_value=3,
    )

    assert moves == [
        Move(start=0, end=3, die_value=3),
    ]


def test_only_bar_entry_is_generated_when_piece_is_on_bar() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[10] = 2

    moves = board.legal_moves_for_die(
        player=1,
        die_value=3,
    )

    assert moves == [
        Move(start=None, end=2, die_value=3),
    ]


def test_no_move_generated_when_bar_entry_is_blocked() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[2] = -2
    board.points[10] = 2

    moves = board.legal_moves_for_die(
        player=1,
        die_value=3,
    )

    assert moves == []


def test_apply_move_applies_regular_move() -> None:
    board = Board()
    board.points[0] = 1

    move = Move(
        start=0,
        end=3,
        die_value=3,
    )

    board.apply_move(
        player=1,
        move=move,
    )

    assert board.points[0] == 0
    assert board.points[3] == 1


def test_apply_move_applies_bar_entry() -> None:
    board = Board()
    board.player_one_bar = 1

    move = Move(
        start=None,
        end=2,
        die_value=3,
    )

    board.apply_move(
        player=1,
        move=move,
    )

    assert board.player_one_bar == 0
    assert board.points[2] == 1


def test_legal_turn_uses_both_dice() -> None:
    board = Board()
    board.points[0] = 1

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=3,
    )

    assert (
        Move(start=0, end=2, die_value=2),
        Move(start=2, end=5, die_value=3),
    ) in turns

    assert (
        Move(start=0, end=3, die_value=3),
        Move(start=3, end=5, die_value=2),
    ) in turns

    assert all(len(turn) == 2 for turn in turns)


def test_legal_turn_considers_different_pieces() -> None:
    board = Board()
    board.points[0] = 1
    board.points[5] = 1

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=3,
    )

    assert (
        Move(start=0, end=2, die_value=2),
        Move(start=5, end=8, die_value=3),
    ) in turns


def test_blocked_die_can_be_skipped() -> None:
    board = Board()
    board.points[0] = 1
    board.points[2] = -2

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=3,
    )

    assert turns == [
        (
            Move(start=0, end=3, die_value=3),
        ),
    ]


def test_only_available_die_is_used() -> None:
    board = Board()
    board.points[0] = 1
    board.points[2] = -2

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=3,
    )

    assert turns == [
        (
            Move(start=0, end=3, die_value=3),
        ),
    ]


def test_doubles_can_generate_four_moves() -> None:
    board = Board()
    board.points[0] = 1

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=2,
    )

    assert (
        Move(start=0, end=2, die_value=2),
        Move(start=2, end=4, die_value=2),
        Move(start=4, end=6, die_value=2),
        Move(start=6, end=8, die_value=2),
    ) in turns

    assert all(len(turn) == 4 for turn in turns)


def test_bar_piece_must_enter_before_other_moves() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[10] = 1

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=3,
    )

    assert all(turn[0].is_bar_entry for turn in turns)


def test_no_legal_turn_returns_empty_list() -> None:
    board = Board()
    board.player_one_bar = 1

    for index in range(6):
        board.points[index] = -2

    turns = board.legal_turns(
        player=1,
        die_one=2,
        die_two=5,
    )

    assert turns == []


def test_apply_turn_applies_all_moves() -> None:
    board = Board()
    board.points[0] = 1

    turn = (
        Move(start=0, end=2, die_value=2),
        Move(start=2, end=5, die_value=3),
    )

    board.apply_turn(
        player=1,
        moves=turn,
    )

    assert board.points[0] == 0
    assert board.points[5] == 1


def test_player_one_bar_entry_index() -> None:
    board = Board()

    assert board.bar_entry_index(player=1, die_value=1) == 0
    assert board.bar_entry_index(player=1, die_value=6) == 5


def test_player_two_bar_entry_index() -> None:
    board = Board()

    assert board.bar_entry_index(player=-1, die_value=1) == 23
    assert board.bar_entry_index(player=-1, die_value=6) == 18


def test_player_one_can_enter_from_bar() -> None:
    board = Board()
    board.player_one_bar = 1

    board.enter_from_bar(player=1, die_value=3)

    assert board.player_one_bar == 0
    assert board.points[2] == 1
    assert board.piece_count(1) == 1


def test_player_two_can_enter_from_bar() -> None:
    board = Board()
    board.player_two_bar = 1

    board.enter_from_bar(player=-1, die_value=3)

    assert board.player_two_bar == 0
    assert board.points[21] == -1
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


def test_player_one_cannot_enter_on_blocked_point() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[2] = -2

    assert not board.is_bar_entry_legal(
        player=1,
        die_value=3,
    )


def test_player_two_cannot_enter_on_blocked_point() -> None:
    board = Board()
    board.player_two_bar = 1
    board.points[21] = 2

    assert not board.is_bar_entry_legal(
        player=-1,
        die_value=3,
    )


def test_player_one_bar_entry_can_capture() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[2] = -1

    board.enter_from_bar(player=1, die_value=3)

    assert board.player_one_bar == 0
    assert board.points[2] == 1
    assert board.player_two_bar == 1


def test_player_two_bar_entry_can_capture() -> None:
    board = Board()
    board.player_two_bar = 1
    board.points[21] = 1

    board.enter_from_bar(player=-1, die_value=3)

    assert board.player_two_bar == 0
    assert board.points[21] == -1
    assert board.player_one_bar == 1


def test_player_cannot_make_normal_move_with_piece_on_bar() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[0] = 1

    assert not board.is_simple_move_legal(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )


def test_illegal_bar_entry_does_not_change_board() -> None:
    board = Board()
    board.player_one_bar = 1
    board.points[2] = -2

    original_points = board.points.copy()
    original_bar = board.player_one_bar

    with pytest.raises(ValueError):
        board.enter_from_bar(
            player=1,
            die_value=3,
        )

    assert board.points == original_points
    assert board.player_one_bar == original_bar


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