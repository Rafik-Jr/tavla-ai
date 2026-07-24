from game.board import Board


def main() -> None:
    board = Board()

    board.points[0] = 1
    board.points[3] = -1

    print("Before capture:")
    board.display()

    board.move_piece(
        player=1,
        start=0,
        end=3,
        die_value=3,
    )

    print()
    print("After Player 1 captures Player 2:")
    board.display()


if __name__ == "__main__":
    main()
