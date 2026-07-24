from game.move import Move


def test_move_stores_start_and_end_points() -> None:
    move = Move(start=0, end=4)

    assert move.start == 0
    assert move.end == 4