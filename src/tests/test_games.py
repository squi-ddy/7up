import nextcord

from games import (
    CountUpGame,
    FizzBuzzGame,
    SevenUpFactorsGame,
    SevenUpGame,
    SevenUpHardGame,
    ValidationResult,
)

games_to_test = [
    SevenUpGame,
    SevenUpHardGame,
    SevenUpFactorsGame,
    CountUpGame,
    FizzBuzzGame,
]

messages = [
    "I love cream cheese!",
    "<@832964372803354655>",
    "<:drewimo:993167758500048916>",
    "<#995972091759300629>",
    ":1:",
    "This is a discussion about `7`",
    "`1524`",
    "꧕",
]


def test_games_solutions():
    # Test on correct solutions
    for game in games_to_test:
        for i in range(1, 1000):
            assert game.is_valid(game.get_solution(i), i) == ValidationResult.ACCEPT


def test_games_ignore():
    # Test on unrelated message
    for game in games_to_test:
        for i in range(1, 1000):
            for message in messages:
                assert game.is_valid(message, i) == ValidationResult.UNRELATED


def test_games_help():
    # Test game attributes
    for game in games_to_test:
        assert isinstance(game.get_title(), str)
        assert isinstance(game.get_embed(), nextcord.Embed)
        assert game.get_embed().title is not nextcord.Embed.Empty
        assert game.get_embed().description is not nextcord.Embed.Empty
        assert game.get_title() == game.get_embed().title
