from dataclasses import dataclass
from random import Random
from time import perf_counter

from bots.random_bot import RandomBot
from game.game import Game
from game.runner import play_game


@dataclass(frozen=True)
class TournamentResult:
    games_played: int
    player_one_wins: int
    player_two_wins: int
    total_turns: int
    elapsed_seconds: float

    @property
    def player_one_win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.player_one_wins / self.games_played

    @property
    def player_two_win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.player_two_wins / self.games_played

    @property
    def average_turns(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.total_turns / self.games_played

    @property
    def games_per_second(self) -> float:
        if self.elapsed_seconds <= 0:
            return 0.0
        return self.games_played / self.elapsed_seconds


def run_tournament(number_of_games: int, seed: int = 42) -> TournamentResult:
    """Run a reproducible tournament between two random bots."""
    if number_of_games <= 0:
        raise ValueError("number_of_games must be greater than zero")

    master_rng = Random(seed)
    player_one_wins = 0
    player_two_wins = 0
    total_turns = 0
    start_time = perf_counter()

    for _ in range(number_of_games):
        game = Game(rng=Random(master_rng.randrange(1_000_000_000)))
        player_one_bot = RandomBot("Random Bot A", Random(master_rng.randrange(1_000_000_000)))
        player_two_bot = RandomBot("Random Bot B", Random(master_rng.randrange(1_000_000_000)))
        result = play_game(game, player_one_bot, player_two_bot)
        total_turns += result.turns_played
        if result.winner == 1:
            player_one_wins += 1
        else:
            player_two_wins += 1

    return TournamentResult(
        games_played=number_of_games,
        player_one_wins=player_one_wins,
        player_two_wins=player_two_wins,
        total_turns=total_turns,
        elapsed_seconds=perf_counter() - start_time,
    )


def print_tournament_result(result: TournamentResult) -> None:
    print("Tournament complete")
    print("-" * 40)
    print(f"Games played: {result.games_played}")
    print(f"Player 1 wins: {result.player_one_wins}")
    print(f"Player 2 wins: {result.player_two_wins}")
    print(f"Player 1 win rate: {result.player_one_win_rate:.1%}")
    print(f"Player 2 win rate: {result.player_two_win_rate:.1%}")
    print(f"Average turns: {result.average_turns:.1f}")
    print(f"Elapsed time: {result.elapsed_seconds:.2f} seconds")
    print(f"Games per second: {result.games_per_second:.2f}")
