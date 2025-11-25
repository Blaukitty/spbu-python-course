from random import randint
from typing import Tuple, Optional
from constants import Color

class Ruller:
    def __init__(self, color_cur: Optional[str] = None, number_cur: Optional[int] = None) -> None:
        self.numbers: list[int] = list(range(0, 37))
        self.number_cur: Optional[int] = number_cur
        self.color_cur: Optional[str] = color_cur

    def ruller_spin(self) -> Tuple[int, str]:
        self.number_cur = randint(0, 36)
        self.color_cur = self.ruller_color(self.number_cur)
        return self.number_cur, self.color_cur

    def ruller_color(self, numb: int) -> str:
        if numb == 0:
            return Color.GREEN.value
        elif numb % 2 == 0:
            return Color.RED.value
        else:
            return Color.BLACK.value

    def get_result(self) -> Tuple[Optional[int], Optional[str]]:
        return self.number_cur, self.color_cur
