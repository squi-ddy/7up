import itertools
from typing import Type

import nextcord
import pytest

from games import (
    CountingGame,
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

ignore_messages = [
    "I love cream cheese!",
    "<@832964372803354655>",
    "<:drewimo:993167758500048916>",
    "<#995972091759300629>",
    ":1:",
    "This is a discussion about `7`",
    "`1524`",
    "꧕",
    "`fizz`",
    "`buzz`",
    "`up`",
    "`77 fizz buzz up`",
]


@pytest.mark.parametrize("game", games_to_test)
def test_games_solutions(game):
    # Test on correct solutions
    for i in range(1, 1000):
        assert game.is_valid(game.get_solution(i), i) == ValidationResult.ACCEPT


@pytest.mark.parametrize("game, to_ignore", itertools.product(games_to_test, ignore_messages))
def test_games_ignore(game: Type[CountingGame], to_ignore: str):
    # Test on unrelated message
    for i in range(1, 1000):
        assert game.is_valid(to_ignore, i) == ValidationResult.UNRELATED


def test_games_help():
    # Test game attributes
    for game in games_to_test:
        assert isinstance(game.get_title(), str)
        assert isinstance(game.get_embed(), nextcord.Embed)
        assert game.get_embed().title is not nextcord.Embed.Empty
        assert game.get_embed().description is not nextcord.Embed.Empty
        assert game.get_title() == game.get_embed().title
