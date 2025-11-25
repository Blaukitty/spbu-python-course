from random import randint
from typing import Tuple, List, Optional
from .constants import Color, BetType, StrategyType

class Bots:
    def __init__(self, number1_b: Optional[int] = None, number2_b: Optional[int] = None) -> None:
        self.diapason: List[int] = []
        self.color_b: Optional[str] = None
        self.indicator: int = randint(StrategyType.DALAMBER.value, StrategyType.ALL_CAPITAL.value)
        self.bet_type: BetType = BetType.SINGLE
        self.ifwin: bool = False
        self.number1_b: int = 0
        self.number2_b: int = 0
        self.selected_dozen: int = randint(1, 3)
        self.selected_even_odd: str = 'even' if randint(1, 2) == 1 else 'odd'

    def choice(self) -> Tuple[str, List[int], BetType]:
        self.number1_b = randint(0, 30)
        self.number2_b = randint(0, 36)
        self.diapason = []

        if self.number2_b < self.number1_b:
            self.diapason.append(self.number1_b)
        elif self.number2_b != 0:
            for number in range(self.number1_b, self.number2_b + 1):
                self.diapason.append(number)
        else:
            self.diapason.append(self.number1_b)

        self.color_b = self.color_choice()
        bet_types = list(BetType)
        self.bet_type = bet_types[randint(0, len(bet_types) - 1)]

        return self.color_b, self.diapason, self.bet_type

    def color_choice(self) -> str:
        if 0 in self.diapason:
            color_indicator = randint(1, 3)
        else:
            color_indicator = randint(1, 2)

        if color_indicator == 1:
            if len(self.diapason) == 1 and self.diapason[0] != 0:
                if self.diapason[0] % 2 == 0:
                    return Color.RED.value
                else:
                    return Color.BLACK.value
            else:
                return Color.RED.value
        elif color_indicator == 2:
            if len(self.diapason) == 1 and self.diapason[0] != 0:
                if self.diapason[0] % 2 == 1:
                    return Color.BLACK.value
                else:
                    return Color.RED.value
            else:
                return Color.BLACK.value
        else:
            return Color.GREEN.value

    def get_choice(self) -> List[int]:
        return self.diapason
