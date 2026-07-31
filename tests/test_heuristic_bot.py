from random import Random

from bots.heuristic_bot import HeuristicBot
from game.board import Board
from game.game import Game


def test_heuristic_bot_returns_a_legal_turn() -> None:
    game = Game(board=Board.starting_position(), current_player=1)
    bot = HeuristicBot()
    turn = bot.choose_turn(game, (1, 2))
    assert turn in game.legal_turns((1, 2))


def test_heuristic_bot_does_not_mutate_game_board() -> None:
    game = Game(board=Board.starting_position(), current_player=1)
    before = game.board.copy()
    HeuristicBot(rng=Random(42)).choose_turn(game, (1, 2))
    assert game.board == before


def test_heuristic_bot_returns_none_when_no_turn_is_legal() -> None:
    board = Board()
    board.points[0] = 1
    board.points[1] = -2
    game = Game(board=board, current_player=1)
    assert HeuristicBot().choose_turn(game, (1, 1)) is None
