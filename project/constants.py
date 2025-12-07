from enum import Enum


class StrategyType(Enum):
    DALAMBER = 1
    MARTINGEIL = 2
    ALL_CAPITAL = 3


class Color(Enum):
    RED = "red"
    BLACK = "black"
    GREEN = "green"


class BetType(Enum):
    SINGLE = "single"
    COLOR = "color"
    DOZEN = "dozen"
    EVEN_ODD = "even_odd"
    RANGE = "range"


PAYOUTS = {
    BetType.SINGLE: 35,
    BetType.COLOR: 2,
    BetType.DOZEN: 3,
    BetType.EVEN_ODD: 2,
    BetType.RANGE: 2,
}

BASE_BET = 100
INITIAL_MONEY = 1000
