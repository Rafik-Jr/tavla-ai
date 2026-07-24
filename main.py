from game.board import Board


def main() -> None:
    board = Board.starting_position()

    die_value = 3
    legal_moves = board.legal_moves_for_die(
        player=1,
        die_value=die_value,
    )

    print(f"Player 1 legal moves using die {die_value}:")

    for move in legal_moves:
        if move.is_bar_entry:
            print(
                f"Enter from bar onto point {move.end + 1}"
            )
        else:
            print(
                f"Move from point {move.start + 1} "
                f"to point {move.end + 1}"
            )


if __name__ == "__main__":
    main()
