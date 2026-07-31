import pytest

from bots.random_bot import RandomBot
from evaluation.tournament import TournamentResult, run_tournament


def random_bot_factory(rng):
    return RandomBot(name="Test Random Bot", rng=rng)


def test_tournament_result_calculates_win_rates() -> None:
    result = TournamentResult(10, 6, 4, 800, 2.0)
    assert result.player_one_win_rate == pytest.approx(0.6)
    assert result.player_two_win_rate == pytest.approx(0.4)


def test_tournament_result_calculates_average_turns() -> None:
    assert TournamentResult(10, 6, 4, 800, 2.0).average_turns == pytest.approx(80.0)


def test_tournament_result_calculates_games_per_second() -> None:
    assert TournamentResult(10, 6, 4, 800, 2.0).games_per_second == pytest.approx(5.0)


def test_tournament_rejects_zero_games() -> None:
    with pytest.raises(ValueError):
        run_tournament(0, player_one_factory=random_bot_factory, player_two_factory=random_bot_factory)


def test_tournament_plays_requested_number_of_games() -> None:
    result = run_tournament(3, seed=42, player_one_factory=random_bot_factory, player_two_factory=random_bot_factory)
    assert result.games_played == 3
    assert result.player_one_wins - result.player_two_wins in (-3, -1, 1, 3)
    assert result.total_turns > 0


def test_seeded_tournament_has_reproducible_game_results() -> None:
    first = run_tournament(5, seed=123, player_one_factory=random_bot_factory, player_two_factory=random_bot_factory)
    second = run_tournament(5, seed=123, player_one_factory=random_bot_factory, player_two_factory=random_bot_factory)
    assert (first.player_one_wins, first.player_two_wins, first.total_turns) == (
        second.player_one_wins,
        second.player_two_wins,
        second.total_turns,
    )
