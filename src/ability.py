from enum import Enum, auto

class AbilityResult(Enum):
    END_TURN = auto()
    ALLOW_EXTRA_MOVES = auto()
    CONTINUE = auto()