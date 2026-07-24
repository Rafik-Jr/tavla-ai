"""Board module.

Game rules and board behavior will be implemented separately.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field

from game.move import Move


@dataclass
class Board:
    """
    Represents a Tavla board.

    Point indexes are 0 through 23.
    Positive numbers represent Player 1 pieces.
    Negative numbers represent Player 2 pieces.
    """

    points: list[int] = field(default_factory=lambda: [0] * 24)

    player_one_bar: int = 0
    player_two_bar: int = 0

    player_one_off: int = 0
    player_two_off: int = 0

    @classmethod
    def starting_position(cls) -> "Board":
        board = cls()

        # Standard backgammon starting position.
        board.points[0] = 2
        board.points[11] = 5
        board.points[16] = 3
        board.points[18] = 5

        board.points[23] = -2
        board.points[12] = -5
        board.points[7] = -3
        board.points[5] = -5

        return board

    def piece_count(self, player: int) -> int:
        """
        Return the total number of pieces belonging to a player.

        player must be 1 or -1.
        """

        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if player == 1:
            pieces_on_board = sum(
                count for count in self.points if count > 0
            )
            return pieces_on_board + self.player_one_bar + self.player_one_off

        pieces_on_board = sum(
            abs(count) for count in self.points if count < 0
        )
        return pieces_on_board + self.player_two_bar + self.player_two_off

    def bar_entry_index(self, player: int, die_value: int) -> int:
        """
        Return the destination index for entering from the bar.
        """

        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if not 1 <= die_value <= 6:
            raise ValueError("die_value must be between 1 and 6")

        if player == 1:
            return die_value - 1

        return 24 - die_value

    def is_bar_entry_legal(self, player: int, die_value: int) -> bool:
        """
        Check whether a player can enter one piece from the bar.
        """

        if player not in (1, -1):
            return False

        if not 1 <= die_value <= 6:
            return False

        if player == 1 and self.player_one_bar <= 0:
            return False

        if player == -1 and self.player_two_bar <= 0:
            return False

        destination_index = self.bar_entry_index(player, die_value)
        destination = self.points[destination_index]

        if player == 1 and destination < -1:
            return False

        if player == -1 and destination > 1:
            return False

        return True

    def enter_from_bar(self, player: int, die_value: int) -> None:
        """
        Enter one piece from the bar.

        This supports entering onto:
        - an empty point
        - a friendly point
        - one exposed opponent piece
        """

        if not self.is_bar_entry_legal(player, die_value):
            raise ValueError("Illegal bar entry")

        destination_index = self.bar_entry_index(player, die_value)
        destination = self.points[destination_index]

        if player == 1:
            self.player_one_bar -= 1

            if destination == -1:
                self.points[destination_index] = 1
                self.player_two_bar += 1
            else:
                self.points[destination_index] += 1

            return

        self.player_two_bar -= 1

        if destination == 1:
            self.points[destination_index] = -1
            self.player_one_bar += 1
        else:
            self.points[destination_index] -= 1

    def copy(self) -> "Board":
        """Return an independent copy of the board."""

        return Board(
            points=self.points.copy(),
            player_one_bar=self.player_one_bar,
            player_two_bar=self.player_two_bar,
            player_one_off=self.player_one_off,
            player_two_off=self.player_two_off,
        )

    def all_pieces_in_home(self, player: int) -> bool:
        """
        Return whether all of the player's remaining board pieces
        are inside their home board.

        Pieces already borne off are allowed.
        Pieces on the bar prevent bearing off.
        """

        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if player == 1:
            if self.player_one_bar > 0:
                return False

            return all(count <= 0 for count in self.points[:18])

        if self.player_two_bar > 0:
            return False

        return all(count >= 0 for count in self.points[6:])

    def is_bear_off_legal(
        self,
        player: int,
        start: int,
        die_value: int,
    ) -> bool:
        """
        Check whether one piece may be borne off using a die.

        This initially supports:
        - exact bearing off
        - oversized dice when no piece is farther from the exit
        """

        if player not in (1, -1):
            return False

        if not 0 <= start < 24:
            return False

        if not 1 <= die_value <= 6:
            return False

        if not self.all_pieces_in_home(player):
            return False

        start_count = self.points[start]

        if player == 1:
            if start_count <= 0:
                return False

            if start < 18:
                return False

            distance_to_exit = 24 - start

            if die_value == distance_to_exit:
                return True

            if die_value < distance_to_exit:
                return False

            return all(self.points[index] <= 0 for index in range(18, start))

        if start_count >= 0:
            return False

        if start > 5:
            return False

        distance_to_exit = start + 1

        if die_value == distance_to_exit:
            return True

        if die_value < distance_to_exit:
            return False

        return all(self.points[index] >= 0 for index in range(start + 1, 6))

    def bear_off(
        self,
        player: int,
        start: int,
        die_value: int,
    ) -> None:
        """Bear one piece off the board."""

        if not self.is_bear_off_legal(
            player=player,
            start=start,
            die_value=die_value,
        ):
            raise ValueError("Illegal bear off")

        self.points[start] -= player

        if player == 1:
            self.player_one_off += 1
        else:
            self.player_two_off += 1

    def legal_moves_for_die(
        self,
        player: int,
        die_value: int,
    ) -> list[Move]:
        """
        Return every legal move the player can make with one die.

        If the player has a piece on the bar, only bar-entry moves
        are considered.
        """

        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if not 1 <= die_value <= 6:
            raise ValueError("die_value must be between 1 and 6")

        if player == 1 and self.player_one_bar > 0:
            if not self.is_bar_entry_legal(player, die_value):
                return []

            destination = self.bar_entry_index(player, die_value)

            return [
                Move(
                    start=None,
                    end=destination,
                    die_value=die_value,
                )
            ]

        if player == -1 and self.player_two_bar > 0:
            if not self.is_bar_entry_legal(player, die_value):
                return []

            destination = self.bar_entry_index(player, die_value)

            return [
                Move(
                    start=None,
                    end=destination,
                    die_value=die_value,
                )
            ]

        legal_moves: list[Move] = []

        for start in range(24):
            end = start + die_value if player == 1 else start - die_value

            if self.is_simple_move_legal(
                player=player,
                start=start,
                end=end,
                die_value=die_value,
            ):
                legal_moves.append(
                    Move(
                        start=start,
                        end=end,
                        die_value=die_value,
                    )
                )
                continue

            if self.is_bear_off_legal(
                player=player,
                start=start,
                die_value=die_value,
            ):
                legal_moves.append(
                    Move(
                        start=start,
                        end=None,
                        die_value=die_value,
                    )
                )

        return legal_moves

    def apply_move(self, player: int, move: Move) -> None:
        """
        Apply a Move object to the board.
        """

        if move.is_bar_entry:
            self.enter_from_bar(
                player=player,
                die_value=move.die_value,
            )
            return

        if move.is_bear_off:
            if move.start is None:
                raise ValueError("Bear-off move must have a starting point")

            self.bear_off(
                player=player,
                start=move.start,
                die_value=move.die_value,
            )
            return

        if move.start is None or move.end is None:
            raise ValueError("Normal move requires start and end points")

        self.move_piece(
            player=player,
            start=move.start,
            end=move.end,
            die_value=move.die_value,
        )

    def apply_turn(
        self,
        player: int,
        moves: Sequence[Move],
    ) -> None:
        """
        Apply a sequence of moves to the board.

        The caller should pass a sequence returned by legal_turns().
        """

        for move in moves:
            self.apply_move(
                player=player,
                move=move,
            )

    def legal_turns(
        self,
        player: int,
        die_one: int,
        die_two: int,
    ) -> list[tuple[Move, ...]]:
        """
        Generate every legal move sequence for a complete dice roll.

        Rules currently supported:
        - both dice orders are considered
        - doubles provide four moves
        - the maximum possible number of dice must be used
        - when only one die can be used, the higher die must be used
        """

        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if not 1 <= die_one <= 6 or not 1 <= die_two <= 6:
            raise ValueError("dice must be between 1 and 6")

        if die_one == die_two:
            dice_orders = [(die_one, die_one, die_one, die_one)]
        else:
            dice_orders = [(die_one, die_two), (die_two, die_one)]

        generated_turns: set[tuple[Move, ...]] = set()

        for dice_order in dice_orders:
            playable_dice: list[int] = []

            for die_value in dice_order:
                if self.legal_moves_for_die(
                    player=player,
                    die_value=die_value,
                ):
                    playable_dice.append(die_value)
                else:
                    break

            if not playable_dice:
                continue

            turns = self._generate_turns_for_dice_order(
                player=player,
                dice=playable_dice,
            )
            generated_turns.update(turns)

        if not generated_turns:
            return []

        maximum_moves = max(len(turn) for turn in generated_turns)

        legal_turns = [
            turn for turn in generated_turns if len(turn) == maximum_moves
        ]

        if maximum_moves == 0:
            return []

        if maximum_moves == 1 and die_one != die_two:
            higher_die = max(die_one, die_two)

            higher_die_turns = [
                turn for turn in legal_turns if turn[0].die_value == higher_die
            ]

            if higher_die_turns:
                legal_turns = higher_die_turns

        return sorted(
            legal_turns,
            key=lambda turn: tuple(
                (
                    -1 if move.start is None else move.start,
                    24 if move.end is None else move.end,
                    move.die_value,
                )
                for move in turn
            ),
        )

    def _generate_turns_for_dice_order(
        self,
        player: int,
        dice: Sequence[int],
    ) -> list[tuple[Move, ...]]:
        """
        Generate move sequences using one specific dice order.

        The search uses the chosen dice in order and may stop early when
        a die has no legal move from the current board state.
        """

        completed_turns: list[tuple[Move, ...]] = []

        def search(
            board: Board,
            dice_index: int,
            moves_so_far: tuple[Move, ...],
        ) -> None:
            if dice_index >= len(dice):
                completed_turns.append(moves_so_far)
                return

            die_value = dice[dice_index]
            available_moves = board.legal_moves_for_die(
                player=player,
                die_value=die_value,
            )

            if not available_moves:
                completed_turns.append(moves_so_far)
                return

            for move in available_moves:
                next_board = board.copy()
                next_board.apply_move(
                    player=player,
                    move=move,
                )

                search(
                    board=next_board,
                    dice_index=dice_index + 1,
                    moves_so_far=moves_so_far + (move,),
                )

        search(
            board=self.copy(),
            dice_index=0,
            moves_so_far=(),
        )

        return completed_turns

    def is_simple_move_legal(
        self,
        player: int,
        start: int,
        end: int,
        die_value: int,
    ) -> bool:
        """
        Check whether a basic move is legal.

        This currently checks:
        - valid player
        - valid board indexes
        - valid die value
        - player owns a piece at the starting point
        - correct movement direction
        - distance matches the die
        - destination is not blocked

        Captures, bar entry, and bearing off are not handled yet.
        """

        if player not in (1, -1):
            return False

        if player == 1 and self.player_one_bar > 0:
            return False

        if player == -1 and self.player_two_bar > 0:
            return False

        if not 0 <= start < 24:
            return False

        if not 0 <= end < 24:
            return False

        if not 1 <= die_value <= 6:
            return False

        starting_point_count = self.points[start]
        destination_point_count = self.points[end]

        if player == 1 and starting_point_count <= 0:
            return False

        if player == -1 and starting_point_count >= 0:
            return False

        expected_end_index = start + die_value if player == 1 else start - die_value

        if end != expected_end_index:
            return False

        if player == 1 and destination_point_count < -1:
            return False

        if player == -1 and destination_point_count > 1:
            return False

        return True

    def move_piece(
        self,
        player: int,
        start: int,
        end: int,
        die_value: int,
    ) -> None:
        """
        Apply a simple legal move.

        Supports:
        - normal moves
        - capturing one exposed opponent piece

        Does not yet support:
        - entering from the bar
        - bearing off
        - complete dice-turn logic
        """

        if not self.is_simple_move_legal(
            player=player,
            start=start,
            end=end,
            die_value=die_value,
        ):
            raise ValueError("Illegal move")

        destination = self.points[end]

        self.points[start] -= player

        if player == 1 and destination == -1:
            self.points[end] = 1
            self.player_two_bar += 1
            return

        if player == -1 and destination == 1:
            self.points[end] = -1
            self.player_one_bar += 1
            return

        self.points[end] += player

    def display(self) -> None:
        print("Tavla Board")
        print("-" * 50)

        for index, count in enumerate(self.points, start=1):
            print(f"Point {index:2}: {count:3}")

        print("-" * 50)
        print(f"Player 1 bar: {self.player_one_bar}")
        print(f"Player 2 bar: {self.player_two_bar}")
        print(f"Player 1 off: {self.player_one_off}")
        print(f"Player 2 off: {self.player_two_off}")

        