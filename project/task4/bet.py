from random import randint
from typing import Tuple, List
from constants import BetType, PAYOUTS, INITIAL_MONEY

class Bet777:
    def __init__(self, money: int = INITIAL_MONEY, xbet: int = 100, 
                 bet_type: BetType = None) -> None:
        self.money: int = money
        self.xbet: int = xbet
        self.bet_type: BetType = bet_type if bet_type else self._random_bet_type()

    def _random_bet_type(self) -> BetType:
        bet_types = list(BetType)
        return bet_types[randint(0, len(bet_types) - 1)]

    def capital(self, money: int) -> None:
        self.money = money

    def bet(self, xbet: int) -> None:
        self.xbet = xbet

    def get_payout(self) -> int:
        return PAYOUTS.get(self.bet_type, 2)

    def get_choice(self) -> Tuple[int, int]:
        return self.money, self.xbet

    def is_bankrupt(self) -> bool:
        return self.money <= 0
