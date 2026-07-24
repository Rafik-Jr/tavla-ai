from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """
    Represents one move using one die.

    start=None means the piece enters from the bar.
    """

    start: int | None
    end: int
    die_value: int

    @property
    def is_bar_entry(self) -> bool:
        return self.start is None
