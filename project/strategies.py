from random import randint
from typing import Optional
from .constants import StrategyType, BASE_BET

class Strategies:
    base_bet: int = BASE_BET

    @staticmethod
    def choose_strategy(curva_bet: int, ifwin: bool, money: int,
                       indicator: Optional[int] = None) -> int:
        actual_indicator = StrategyType(randint(1, 3))

        if actual_indicator == StrategyType.DALAMBER:
            return Strategies.dalamber(curva_bet, ifwin, money)
        elif actual_indicator == StrategyType.MARTINGEIL:
            return Strategies.martingeil(curva_bet, ifwin, money)
        else:
            return Strategies.all_capital(curva_bet, ifwin, money)

    @staticmethod
    def dalamber(curva_bet: int, ifwin: bool, money: int) -> int:
        if ifwin:
            return max(BASE_BET, curva_bet - 100)
        else:
            return min(curva_bet + 100, money)

    @staticmethod
    def all_capital(curva_bet: int, ifwin: bool, money: int) -> int:
        return money

    @staticmethod
    def martingeil(curva_bet: int, ifwin: bool, money: int) -> int:
        if ifwin:
            return Strategies.base_bet
        else:
            new_bet = curva_bet * 2
            return min(new_bet, money)
