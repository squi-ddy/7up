from games import CountUpGame, SevenUpGame, SevenUpHardGame, SevenUpFactorsGame
from games.base import ValidationResult
from games.fizzbuzz import FizzBuzzGame

games_to_test = [SevenUpGame, SevenUpHardGame, SevenUpFactorsGame, CountUpGame, FizzBuzzGame]

# Test on correct solutions
for game in games_to_test:
    for i in range(1, 100000):
        if game.is_valid(solution := game.get_solution(i), i) != ValidationResult.ACCEPT:
            print(f"Game {game} failed with input {i}, generated solution was {solution}")

# Test on unrelated messages
message = "psodiwuend"
for game in games_to_test:
    for i in range(1, 100000):
        if game.is_valid(message, i) != ValidationResult.UNRELATED:
            print(f"Game {game} did not ignore messages correctly with input {i}")

