from random import randint
from typing import Tuple, List, Dict
from task4.roulette import Ruller
from task4.bot import Bots
from task4.bet import Bet777
from task4.strategies import Strategies
from task4.constants import BetType, StrategyType

class Game:
    """Main game class that manages the roulette game with multiple bots."""
    
    def __init__(self, num_bots: int = 2) -> None:
        """Initialize the game with specified number of bots."""
        self.bots: List[Bots] = []
        self.bets: List[Bet777] = []

        for i in range(num_bots):
            self.add_bot()

        self.roulette: Ruller = Ruller()
        self.flag: int = 0
        self.indicator: int = StrategyType(randint(1, 3))
        self.ifwin: bool = False
        self.gain: int = 0

    def add_bot(self) -> None:
        """Add a new bot to the game."""
        new_bot = Bots()
        new_bet = Bet777()

        self.bots.append(new_bot)
        self.bets.append(new_bet)
        new_bot.choice()
        print(f"~ Bot{len(self.bots)} added to the game ~")

    def remove_bankrupt_bots(self) -> None:
        """Remove bankrupt bots from the game."""
        indices_to_remove = []
        
        for i in range(len(self.bots) - 1, -1, -1):
            if self.bets[i].is_bankrupt():
                indices_to_remove.append(i)
        
        for index in indices_to_remove:
            bot_number = index + 1
            print(f"~ Bot{bot_number} bankrupt and removed from the game ~")
            del self.bots[index]
            del self.bets[index]

    def full_money(self) -> int:
        """Calculate total money in all bets."""
        return sum(bet.xbet for bet in self.bets)

    def apply_strategy(self, bot_index: int) -> int:
        """Apply betting strategy for a specific bot."""
        current_bot_bet: Bet777 = self.bets[bot_index]
        current_bot: Bots = self.bots[bot_index]

        new_bet_value: int = Strategies.choose_strategy(
            curva_bet=current_bot_bet.xbet, 
            ifwin=current_bot.ifwin, 
            money=current_bot_bet.money, 
            indicator=current_bot.indicator
        )

        new_bet_value = min(new_bet_value, current_bot_bet.money)
        current_bot_bet.bet(new_bet_value)
        return new_bet_value

    def play_round(self) -> None:
        """Play one round of the game."""
        print(f"\nRound {self.flag + 1}:")
        
        self.remove_bankrupt_bots()
        
        if not self.bots:
            print("All bots are bankrupt! Game over.")
            return

        roulette_result = self.roulette.ruller_spin()
        print(f"Roulette result: number {roulette_result[0]}, color {roulette_result[1]}")
        print(f"Bots remaining in game: {len(self.bots)}")

        for bot_index in range(len(self.bots)):
            if self.bets[bot_index].is_bankrupt():
                continue

            print(f"Bot{bot_index + 1} turn ---")
            current_new_bet = self.apply_strategy(bot_index)
            print(f"Bot{bot_index + 1} placed bet: {current_new_bet}")

            current_bot_choice = self.bots[bot_index].choice()
            print(f"Bot{bot_index + 1} chose: color {current_bot_choice[0]}, numbers {current_bot_choice[1]}, bet type: {current_bot_choice[2].value}")

            self.check_win(bot_index, roulette_result)

    def check_win(self, bot_index: int, roulette_result: Tuple[int, str]) -> None:
        """Check if bot won and update money accordingly."""
        strategies: Dict[int, str] = {1: "D'Alembert", 2: "Martingale", 3: "All-in"}
        current_bot: Bots = self.bots[bot_index]
        current_bet: Bet777 = self.bets[bot_index]
        winning_number, winning_color = roulette_result

        is_win = False
        payout_multiplier = 1
        bet_description = ""

        bot_bet_type = current_bot.bet_type

        if bot_bet_type == BetType.SINGLE:
            is_win = winning_number in current_bot.diapason
            payout_multiplier = 35
            bet_description = f"number {current_bot.diapason}"

        elif bot_bet_type == BetType.COLOR:
            is_win = winning_color == current_bot.color_b
            payout_multiplier = 2
            bet_description = f"color {current_bot.color_b}"

        elif bot_bet_type == BetType.DOZEN:
            is_win = self._is_in_dozen(winning_number, current_bot.selected_dozen)
            payout_multiplier = 3
            bet_description = f"dozen {current_bot.selected_dozen}"

        elif bot_bet_type == BetType.EVEN_ODD:
            is_win = self._is_even_odd(winning_number, current_bot.selected_even_odd)
            payout_multiplier = 2
            bet_description = f"{'even' if current_bot.selected_even_odd == 'even' else 'odd'} numbers"

        elif bot_bet_type == BetType.RANGE:
            if len(current_bot.diapason) == 1:
                if current_bot.color_b == winning_color and winning_number in current_bot.diapason:
                    is_win = True
                    payout_multiplier = 35
                    bet_description = f"number {current_bot.diapason[0]}"
                else:
                    is_win = False
                    bet_description = f"number {current_bot.diapason[0]}"
            else:
                if winning_number in current_bot.diapason:
                    if current_bot.color_b == winning_color:
                        is_win = True
                        payout_multiplier = 2
                        bet_description = f"range {current_bot.diapason} with color"
                    else:
                        is_win = True
                        payout_multiplier = 1
                        bet_description = f"range {current_bot.diapason}"
                else:
                    is_win = False
                    bet_description = f"range {current_bot.diapason}"

        self.ifwin = is_win
        self.gain = current_bet.xbet * payout_multiplier if is_win else 0

        if is_win:
            current_bet.money += self.gain
            print(f'  Win! Bet: {bet_description}')
            print(f'  - Payout: {payout_multiplier}:1')
            print(f'  - Winnings: ${self.gain}')
        else:
            current_bet.money -= current_bet.xbet
            print(f'  Loss! Bet: {bet_description}')
            print(f'  - Loss: ${current_bet.xbet}')

        print(f" - strategy: {strategies[current_bot.indicator]}, capital now: {current_bet.money}\n")
        current_bot.ifwin = is_win

    def _is_in_dozen(self, number: int, dozen: int) -> bool:
        """Check if number belongs to specified dozen."""
        if dozen == 1:
            return 1 <= number <= 12
        elif dozen == 2:
            return 13 <= number <= 24
        elif dozen == 3:
            return 25 <= number <= 36
        return False

    def _is_even_odd(self, number: int, even_odd: str) -> bool:
        """Check if number is even or odd."""
        if number == 0:
            return False
        if even_odd == "even":
            return number % 2 == 0
        elif even_odd == "odd":
            return number % 2 == 1
        return False

    def play_game(self, max_rounds: int = 30) -> None:
        """Main game loop."""
        print(f"\nStarting money:")
        for i, bet in enumerate(self.bets):
            print(f"  Bot{i + 1}: ${bet.money}")

        round_count: int = 0

        while self.bots and round_count < max_rounds:
            self.flag += 1
            round_count += 1

            self.play_round()

            if not self.bots:
                print("All bots are bankrupt!")
                break

        self.declare_winner()

    def declare_winner(self) -> None:
        """Declare the winner of the game."""
        print(" ~ Game Over ~ ")

        if not self.bots:
            print("No winners - all bots are bankrupt!")
            return

        bot_money = [(bet.money, i) for i, bet in enumerate(self.bets)]
        bot_money.sort(reverse=True, key=lambda x: x[0])

        max_money = bot_money[0][0]
        winners = [i for money, i in bot_money if money == max_money]

        if len(winners) == 1:
            print(f"Winner: Bot{winners[0] + 1} with ${max_money}!")
        else:
            winner_names = ', '.join(f'Bot{i+1}' for i in winners)
            print(f"Tie between bots: {winner_names} with ${max_money}")
