from typing import List, Type

from .base import CountingGame
from .count_up import CountUpGame
from .fizzbuzz import FizzBuzzGame
from .seven_up import SevenUpGame
from .seven_up_factors import SevenUpFactorsGame
from .seven_up_hard import SevenUpHardGame


class GameSelector:
    games: List[Type[CountingGame]] = [
        CountUpGame,
        SevenUpGame,
        FizzBuzzGame,
        SevenUpHardGame,
        SevenUpFactorsGame,
    ]

    @classmethod
    def get_game_by_id(cls, game_id: int) -> Type[CountingGame]:
        return cls.games[game_id]

    @classmethod
    def get_game_by_name(cls, game_name: str) -> Type[CountingGame]:
        for game in cls.games:
            if game.get_title() == game_name:
                return game

        raise ValueError

    @classmethod
    def get_id_by_game(cls, game: Type[CountingGame]) -> int:
        return cls.games.index(game)
