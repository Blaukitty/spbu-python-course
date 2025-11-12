from random import randint
from typing import Tuple, List, Optional, Dict

class StrategyType:
    """Constants representing available betting strategies.
    
    Attributes:
        DALAMBER (int): Dalembert strategy identifier
        MARTINGEIL (int): Martingale strategy identifier  
        ALL_CAPITAL (int): All-in strategy identifier
    """
    DALAMBER = 1
    MARTINGEIL = 2  
    ALL_CAPITAL = 3

class Color:
    """Constants representing roulette colors.
    
    Attributes:
        RED (tuple): Red color as (name, value) tuple
        BLACK (tuple): Black color as (name, value) tuple
        GREEN (tuple): Green color as (name, value) tuple
    """
    RED = ('red')
    BLACK = ('black') 
    GREEN = ('green')

class ColorType:
    """Constants representing roulette colors with numeric values.
    
    Attributes:
        RED (tuple): Red color as (name, value) tuple
        BLACK (tuple): Black color as (name, value) tuple
        GREEN (tuple): Green color as (name, value) tuple
    """
    RED = (1)
    BLACK = (2) 
    GREEN = (3)   

class BetType:
    """Constants representing available bet types in roulette.
    
    Attributes:
        SINGLE (str): Bet on a single number
        COLOR (str): Bet on a color
        DOZEN (str): Bet on a dozen (1-12, 13-24, 25-36)
        EVEN_ODD (str): Bet on even or odd numbers
        RANGE (str): Bet on a range of numbers
    """
    SINGLE = "single"
    COLOR = "color" 
    DOZEN = "dozen"
    EVEN_ODD = "even_odd"
    RANGE = "range"

class Ruller:
    """Manages roulette wheel operations and results.
    
    Attributes:
        numbers (List[int]): List of all possible roulette numbers (0-36)
        number_cur (Optional[int]): Current number from last spin
        color_cur (Optional[str]): Current color from last spin
    """
    
    def __init__(self, color_cur: Optional[str] = None, number_cur: Optional[int] = None) -> None:
        """Initialize roulette with numbers and optional current state."""
        self.numbers: List[int] = list(range(0, 37))
        self.number_cur: Optional[int] = number_cur
        self.color_cur: Optional[str] = color_cur

    def ruller_spin(self) -> Tuple[int, str]:
        """Spin the roulette and return result."""
        self.number_cur = randint(0, 36)
        self.color_cur = self.ruller_color(self.number_cur)
        return self.number_cur, self.color_cur

    def ruller_color(self, numb: int) -> str:
        """ Determine color for given number."""
        if numb == 0:
            return Color.GREEN
        elif numb % 2 == 0:
            return Color.RED
        else:
            return Color.BLACK
        
    def get_result(self) -> Tuple[Optional[int], Optional[str]]:
        """Get current roulette result  """
        return self.number_cur, self.color_cur
    
class Bots:
    """Represents AI players with betting strategies and choices.
    
    Attributes:
        diapason (List[int]): Current betting number range
        color_b (Optional[str]): Current chosen color for betting
        indicator (int): Current betting strategy identifier
        ifwin (bool): Win status from previous round
        number1_b (int): First number in betting range
        number2_b (int): Second number in betting range
        selected_dozen (int): Chosen dozen for dozen bets (1, 2, or 3)
        selected_even_odd (str): Chosen parity for even/odd bets ('even' or 'odd')
    """
    
    def __init__(self, number1_b: Optional[int] = None, number2_b: Optional[int] = None) -> None:
        """Initialize bot with optional number range."""
        self.diapason: List[int] = []
        self.color_b: Optional[str] = None
        self.indicator: int = randint(StrategyType.DALAMBER, StrategyType.ALL_CAPITAL)
        self.ifwin: bool = False
        self.number1_b: int = 0
        self.number2_b: int = 0
        self.selected_dozen: int = randint(1, 3)
        self.selected_even_odd: str = 'even' if randint(1, 2) == 1 else 'odd'

    def choice(self) -> Tuple[str, List[int]]:
        """Make betting choice for current round."""
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
        return self.color_b, self.diapason

    def color_choice(self) -> str:
        """Choose color based on current betting range."""
        temp_diapason: List[int] = []
        
        if self.number2_b != 0:
            for number in range(self.number1_b, self.number2_b + 1):
                temp_diapason.append(number)
        else:
            temp_diapason.append(self.number1_b)

        if len(temp_diapason) == 1:
            color_indicator = randint(ColorType.RED, ColorType.BLACK)
        else:
            color_indicator = randint(ColorType.BLACK, ColorType.BLACK)

        if color_indicator == Color.RED:
            return Color.RED
        elif color_indicator == Color.BLACK:
            return Color.BLACK
        else:
            return Color.GREEN

    def get_choice(self) -> List[int]:
        """Get current number range choice."""
        return self.diapason

class Bet777:
    """Manages player bets, money, and bet types.
    
    Attributes:
        money (int): Current money amount
        xbet (int): Current bet amount
        bet_type (str): Type of current bet
    """
    payouts = {
        BetType.SINGLE: 35,
        BetType.COLOR: 2,
        BetType.DOZEN: 3,
        BetType.EVEN_ODD: 2,
        BetType.RANGE: 2
    }
    
    def __init__(self, money: int = 1000, xbet: int = 100, bet_type: Optional[str] = None) -> None:
        """Initialize bet with money and bet amount."""
        self.money: int = money
        self.xbet: int = xbet
        self.bet_type: str = bet_type if bet_type else self._random_bet_type()
    
    def _random_bet_type(self) -> str:
        bet_types = [BetType.SINGLE, BetType.COLOR, BetType.DOZEN, BetType.EVEN_ODD, BetType.RANGE]
        return bet_types[randint(0, len(bet_types) - 1)]

    def capital(self, money: int) -> None:
        """Update money amount."""
        self.money = money

    def bet(self, xbet: int) -> None:
        """Update bet amount."""
        self.xbet = xbet

    def get_payout(self) -> int:
        """Get payout multiplier for current bet type."""
        return self.payouts.get(self.bet_type, 2)

    def get_choice(self) -> Tuple[int, int]:
        """Get current money and bet status."""
        return self.money, self.xbet

class Strategies:
    """Class containing different betting strategies."""
    base_bet: int = 100
    @staticmethod
    def choose_strategy(curva_bet: int, ifwin: bool, money: int, 
                       indicator: Optional[int] = None) -> int:
        """Randomly select and apply a betting strategy using randint.
        
        Args:
            curva_bet: Current bet amount
            ifwin: Win status from previous round
            money: Current money amount
            indicator: Optional strategy indicator (ignored, random selection used)        
        """
        actual_indicator = randint(StrategyType.DALAMBER, StrategyType.ALL_CAPITAL)
        
        if actual_indicator == StrategyType.DALAMBER:
            return Strategies.dalamber(curva_bet, ifwin, money)
        elif actual_indicator == StrategyType.MARTINGEIL:
            return Strategies.martingeil(curva_bet, ifwin, money)
        else:
            return Strategies.all_capital(curva_bet, ifwin, money)
            
    @staticmethod
    def dalamber(curva_bet: int, ifwin: bool, money: int) -> int:
        """D'Alembert betting strategy implementation"""
        if ifwin:
            return max(0, curva_bet - 100)
        else:
            return curva_bet + 100

    @staticmethod
    def all_capital(curva_bet: int, ifwin: bool, money: int) -> int:
        """All-in betting strategy implementation."""
        if ifwin:
            return max(0, money - curva_bet)
        else:
            return money
    
    @staticmethod
    def martingeil(curva_bet: int, ifwin: bool, money: int) -> int:
        
        """Martingale betting strategy - double on loss, reset on win."""
        if ifwin:
            return Strategies.base_bet
        else:
            new_bet = curva_bet * 2
            return min(new_bet, money)

class Game:
    """Main game class managing roulette game between multiple bots.
    
    Attributes:
        bots (List[Bots]): List of all bot players
        bets (List[Bet777]): List of all bet managers
        roulette (Ruller): Roulette wheel instance
        flag (int): Game round counter
        indicator (int): Game strategy indicator
        ifwin (bool): Global win status
        gain (int): Current gain amount
    """
    def __init__(self, num_bots: int = 2) -> None:
        self.bots: List[Bots] = []
        self.bets: List[Bet777] = []
        
        for i in range(num_bots):
            self.add_bot()
        
        self.roulette: Ruller = Ruller()
        self.flag: int = 0
        self.indicator: int = randint(StrategyType.DALAMBER, StrategyType.ALL_CAPITAL)
        self.ifwin: bool = False
        self.gain: int = 0

    def add_bot(self) -> None:
        """Add new bot in the game"""
        new_bot = Bots()
        new_bet = Bet777()
        
        self.bots.append(new_bot)
        self.bets.append(new_bet)
        new_bot.choice()
        print(f"~ Бот{len(self.bots)} добавлен в игру ~")

    def get_bots(self) -> int:
        """Get current bot in the game"""
        print(f"Участвует {len(self.bots)} ботов")
        return len(self.bots)

    def full_money(self) -> int:
        """Calculate total money bet by all players."""
        return sum(bet.xbet for bet in self.bets)

    def apply_strategy(self, bot_index: int) -> int:
        """Apply betting strategy to specified bot."""
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

    def play_round(self, bot_index: int) -> None:
        """Play one complete round for specified bot."""
        print(f"Ход для Бота{bot_index + 1} ---")

        if self.bets[bot_index].money <= 0:
            print(f"  Бот{bot_index + 1} банкрот и не может играть")
            return

        current_new_bet: int = self.apply_strategy(bot_index)
        print(f"Бот{bot_index + 1} сделал ставку: {current_new_bet}")

        current_bot_choice: Tuple[str, List[int]] = self.bots[bot_index].choice()
        print(f"Бот{bot_index + 1} выбрал: цвет {current_bot_choice[0]}, числа {current_bot_choice[1]}")

        roulette_result: Tuple[int, str] = self.roulette.ruller_spin()
        print(f"Рулетка выпала: число {roulette_result[0]}, цвет {roulette_result[1]}")

        self.check_win(bot_index, roulette_result)

    def check_win(self, bot_index: int, roulette_result: Tuple[int, str]) -> None:
        """Check if bot won and update game state."""
        strategies: Dict[int, str] = {1: "Даламбер", 2: "Мартингейл", 3: "Все в игру"}
        current_bot: Bots = self.bots[bot_index]
        current_bet: Bet777 = self.bets[bot_index]
        winning_number, winning_color = roulette_result

        is_win = False
        payout_multiplier = 1

        bot_choice = current_bot.get_choice()
        bot_color = current_bot.color_b

        if current_bet.bet_type == BetType.SINGLE:
            is_win = winning_number in bot_choice
            payout_multiplier = 35
            bet_description = f"число {bot_choice[0]}"

        elif current_bet.bet_type == BetType.COLOR:
            is_win = winning_color == bot_color
            payout_multiplier = 2
            bet_description = f"цвет {bot_color}"

        elif current_bet.bet_type == BetType.DOZEN:
            selected_dozen = getattr(current_bot, 'selected_dozen', randint(1, 3))
            is_win = self._is_in_dozen(winning_number, selected_dozen)
            payout_multiplier = 3
            bet_description = f"дюжина {selected_dozen}"

        elif current_bet.bet_type == BetType.EVEN_ODD:
            selected_even_odd = getattr(current_bot, 'selected_even_odd', 'even' if randint(1, 2) == 1 else 'odd')
            is_win = self._is_even_odd(winning_number, selected_even_odd)
            payout_multiplier = 2
            bet_description = f"{'четные' if selected_even_odd == 'even' else 'нечетные'} числа"

        elif current_bet.bet_type == BetType.RANGE:
            if len(bot_choice) == 1:
                if bot_color == winning_color and winning_number in bot_choice:
                    self.gain = current_bet.xbet * 35
                    self.ifwin = True
                    print(f'  Полное попадание!')
                    print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
                else:
                    self.gain = 0
                    self.ifwin = False
                    print(f'  Было близко...')
                    print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
                
                current_bet.money += self.gain - current_bet.xbet
                current_bot.ifwin = self.ifwin

            else:
                if (winning_number in bot_choice) and (winning_color == bot_color):
                    self.gain = int(current_bet.xbet * 0.75)
                    self.ifwin = True
                    print(f'  Попал в диапазон и угадал с цветом')
                    print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
                elif (winning_number in bot_choice) and (winning_color != bot_color):
                    self.gain = int(current_bet.xbet * 0.5)
                    self.ifwin = False
                    print(f'  Попал в диапазон, но цвет мимо')
                    print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
                else:
                    self.gain = 0
                    self.ifwin = False
                    print(f'  Ни одного попадания!')
                    print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
                
                current_bet.money += self.gain - current_bet.xbet
                current_bot.ifwin = self.ifwin

        self.ifwin = is_win
        self.gain = current_bet.xbet * payout_multiplier if is_win else 0

        if is_win:
            print(f'  Выигрыш! Ставка: {bet_description}')
            print(f'  - Выплата: {payout_multiplier}:1')
            print(f'  - Выигрыш: ${self.gain}')
        else:
            print(f'  Проигрыш! Ставка: {bet_description}')
            print(f'  - Потеря: ${current_bet.xbet}')

        print(f" - была выбрана стратегия {strategies[current_bot.indicator]}, капитал теперь {current_bet.money + self.gain - current_bet.xbet}\n")
        
        current_bet.money += self.gain - current_bet.xbet
        current_bot.ifwin = self.ifwin

    def _is_in_dozen(self, number: int, dozen: int) -> bool:
        """Check if number is in specified dozen."""
        if dozen == 1:
            return 1 <= number <= 12
        elif dozen == 2:
            return 13 <= number <= 24
        elif dozen == 3:
            return 25 <= number <= 36
        return False

    def _is_even_odd(self, number: int, even_odd: str) -> bool:
        """Check if number matches even/odd selection."""
        if even_odd == "even":
            return number % 2 == 0 and number != 0
        elif even_odd == "odd":
            return number % 2 == 1
        return False

    def play_game(self, max_rounds: int = 30) -> None:
        """Run complete game until bankruptcy or max rounds reached."""
        print(f"Начальные деньги:")
        for i, bet in enumerate(self.bets):
            print(f"  Бот{i + 1}: ${bet.money}")

        round_count: int = 0
        active_bots = list(range(len(self.bots)))
    
        while active_bots and round_count < max_rounds:
            self.flag += 1
            round_count += 1
            print(f"\nРаунд {round_count}:")
        
            for bot_index in active_bots[:]:
                if self.bets[bot_index].money > 0:
                    self.play_round(bot_index)
                else:
                    print(f"Бот{bot_index + 1} обанкротился!")
                    active_bots.remove(bot_index)
        
            if not active_bots:
                print("Все боты обанкротились!")
                break

        self.declare_winner()

    def declare_winner(self) -> None:
        """Determine and announce game winner based on final money."""
        print(" ~ Игра окончена ~ ")

        bot_money = [(bet.money, i) for i, bet in enumerate(self.bets)]
        bot_money.sort(reverse=True, key=lambda x: x[0])

        max_money = bot_money[0][0]
        winners = [i for money, i in bot_money if money == max_money]

        if len(winners) == 1:
            print(f"Победитель: Бот{winners[0] + 1} с ${max_money}!")
        else:
            winner_names = ', '.join(f'Бот{i+1}' for i in winners)
            print(f"Ничья между ботами: {winner_names} с ${max_money}")
