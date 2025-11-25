from random import randint
from typing import Tuple, Optional
from constants import BetType, PAYOUTS, INITIAL_MONEY

class Bet777:
    """Represents a betting entity with money management and bet types."""
    
    def __init__(self, money: int = INITIAL_MONEY, xbet: int = 100, 
                 bet_type: Optional[BetType] = None) -> None:
        """
        Initialize a betting entity.
        
        Args:
            money: Initial amount of money
            xbet: Initial bet amount
            bet_type: Type of bet, randomly chosen if None
        """
        self.money: int = money
        self.xbet: int = xbet
        self.bet_type: BetType = bet_type if bet_type else self._random_bet_type()

    def _random_bet_type(self) -> BetType:
        """Randomly select a bet type from available options."""
        bet_types = list(BetType)
        return bet_types[randint(0, len(bet_types) - 1)]

    def capital(self, money: int) -> None:
        """
        Set the capital amount.
        
        Args:
            money: New money amount
        """
        self.money = money

    def bet(self, xbet: int) -> None:
        """
        Set the bet amount.
        
        Args:
            xbet: New bet amount
        """
        self.xbet = xbet

    def get_payout(self) -> int:
        """Get the payout multiplier for the current bet type."""
        return PAYOUTS.get(self.bet_type, 2)

    def get_choice(self) -> Tuple[int, int]:
        """Get current money and bet amount."""
        return self.money, self.xbet

    def is_bankrupt(self) -> bool:
        """Check if the entity has no money left."""
        return self.money <= 0
