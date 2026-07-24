from game.board import Board


def main() -> None:
    board = Board()

    board.player_one_bar = 1
    board.points[2] = -1

    print("Before bar entry:")
    board.display()

    board.enter_from_bar(
        player=1,
        die_value=3,
    )

    print()
    print("After Player 1 enters and captures:")
    board.display()


if __name__ == "__main__":
    main()
