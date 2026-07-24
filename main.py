from random import Random

from game.game import Game


def player_name(player: int) -> str:
    return "Player 1" if player == 1 else "Player 2"


def main() -> None:
    game = Game(rng=Random(42))

    dice = game.roll_dice()
    turns = game.legal_turns(dice)

    print(f"{player_name(game.current_player)} rolled {dice}")

    if not turns:
        print("No legal turns.")
        game.pass_turn(dice)
        return

    print(f"Found {len(turns)} legal turns.")

    selected_turn = turns[0]

    for move in selected_turn:
        if move.is_bar_entry:
            print(
                f"Enter from bar to point {move.end + 1} "
                f"using {move.die_value}"
            )
        elif move.is_bear_off:
            print(
                f"Bear off from point {move.start + 1} "
                f"using {move.die_value}"
            )
        else:
            print(
                f"Move point {move.start + 1} "
                f"to point {move.end + 1} "
                f"using {move.die_value}"
            )

    game.play_turn(
        dice=dice,
        moves=selected_turn,
    )

    print(f"Next player: {player_name(game.current_player)}")


if __name__ == "__main__":
    main()
