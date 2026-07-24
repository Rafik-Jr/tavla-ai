from game.board import Board


def main() -> None:
    board = Board.starting_position()

    print("Before move:")
    board.display()

    board.move_piece(player=1, start=0, end=1)

    print()
    print("After Player 1 moves from point 1 to point 2:")
    board.display()


if __name__ == "__main__":
    main()
