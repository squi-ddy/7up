import nextcord

from games import CountUpGame, SevenUpFactorsGame, SevenUpGame, SevenUpHardGame, FizzBuzzGame, ValidationResult

games_to_test = [
    SevenUpGame,
    SevenUpHardGame,
    SevenUpFactorsGame,
    CountUpGame,
    FizzBuzzGame,
]


def test_games_solutions():
    # Test on correct solutions
    for game in games_to_test:
        for i in range(1, 1000):
            assert game.is_valid(game.get_solution(i), i) == ValidationResult.ACCEPT


def test_games_ignore():
    # Test on unrelated message
    message = "I love cream cheese!"
    for game in games_to_test:
        for i in range(1, 1000):
            assert game.is_valid(message, i) == ValidationResult.UNRELATED


def test_games_help():
    # Test game attributes
    for game in games_to_test:
        assert isinstance(game.get_title(), str)
        assert isinstance(game.get_embed(), nextcord.Embed)
        assert game.get_embed().title is not nextcord.Embed.Empty
        assert game.get_embed().description is not nextcord.Embed.Empty
        assert game.get_title() == game.get_embed().title