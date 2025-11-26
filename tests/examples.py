"""
Example of gameplay
"""

if __name__ == "__main__":
    game = Game(num_bots=2)
    game.add_bot()
    game.play_game(max_rounds=1000)
