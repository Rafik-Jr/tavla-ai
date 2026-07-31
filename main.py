from random import Random

from bots.heuristic_bot import HeuristicBot
from bots.random_bot import RandomBot
from evaluation.tournament import print_tournament_result, run_tournament


def main() -> None:
    result = run_tournament(
        number_of_games=100,
        seed=42,
        player_one_factory=lambda rng: HeuristicBot(rng=rng),
        player_two_factory=lambda rng: RandomBot(
            name="Random Bot",
            rng=rng,
        ),
    )
    print_tournament_result(result)


if __name__ == "__main__":
    main()
