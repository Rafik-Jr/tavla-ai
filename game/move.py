from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """
    Represents one move using one die.

    start=None means the piece enters from the bar.
    end=None means the piece bears off.
    """

    start: int | None
    end: int | None
    die_value: int

    @property
    def is_bar_entry(self) -> bool:
        return self.start is None

    @property
    def is_bear_off(self) -> bool:
        return self.end is None
