from game.board import Board


def main() -> None:
    board = Board.starting_position()

    board.display()

    print()
    print("Player 1 pieces:", board.piece_count(1))
    print("Player 2 pieces:", board.piece_count(-1))


if __name__ == "__main__":
    main()

    