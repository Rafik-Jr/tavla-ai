from random import Random

from bots.random_bot import RandomBot
from game.game import Game
from game.runner import play_game


def player_name(player: int) -> str:
    return "Player 1" if player == 1 else "Player 2"


def main() -> None:
    game = Game(
        rng=Random(42),
    )

    player_one_bot = RandomBot(
        name="Random Bot A",
        rng=Random(100),
    )

    player_two_bot = RandomBot(
        name="Random Bot B",
        rng=Random(200),
    )

    result = play_game(
        game=game,
        player_one_bot=player_one_bot,
        player_two_bot=player_two_bot,
        verbose=True,
    )

    print("Game finished")
    print(f"Winner: {player_name(result.winner)}")
    print(f"Turns played: {result.turns_played}")


if __name__ == "__main__":
    main()
