from game.move import Move


def test_move_stores_regular_move_information() -> None:
    move = Move(
        start=0,
        end=4,
        die_value=4,
    )

    assert move.start == 0
    assert move.end == 4
    assert move.die_value == 4
    assert not move.is_bar_entry
    assert not move.is_bear_off


def test_move_can_represent_bar_entry() -> None:
    move = Move(
        start=None,
        end=2,
        die_value=3,
    )

    assert move.is_bar_entry
    assert not move.is_bear_off


def test_move_can_represent_bearing_off() -> None:
    move = Move(
        start=21,
        end=None,
        die_value=3,
    )

    assert not move.is_bar_entry
    assert move.is_bear_off