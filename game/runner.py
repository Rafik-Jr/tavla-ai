from dataclasses import dataclass

from bots.random_bot import RandomBot
from game.game import Game


@dataclass
class GameResult:
    winner: int
    turns_played: int


def play_game(
    game: Game,
    player_one_bot: RandomBot,
    player_two_bot: RandomBot,
    max_turns: int = 10_000,
    verbose: bool = False,
) -> GameResult:
    """
    Play one complete game between two bots.
    """

    turns_played = 0

    while not game.is_over():
        if turns_played >= max_turns:
            raise RuntimeError(
                f"Game exceeded {max_turns} turns"
            )

        dice = game.roll_dice()

        if verbose:
            print(
                f"Turn {turns_played + 1}: "
                f"Player {game.current_player} rolled {dice}"
            )

        bot = (
            player_one_bot
            if game.current_player == 1
            else player_two_bot
        )

        selected_turn = bot.choose_turn(
            game=game,
            dice=dice,
        )

        if verbose:
            print(f"Selected turn: {selected_turn}")

        if selected_turn is None:
            game.pass_turn(dice)
        else:
            game.play_turn(
                dice=dice,
                moves=selected_turn,
            )

        turns_played += 1

    winner = game.winner()

    if winner is None:
        raise RuntimeError("Game ended without a winner")

    return GameResult(
        winner=winner,
        turns_played=turns_played,
    )
