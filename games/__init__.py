from typing import List

from .base import CountingGame
from .count_up import CountUpGame
from .seven_up import SevenUpGame
from .seven_up_hard import SevenUpHardGame
from .seven_up_factors import SevenUpFactorsGame
from .fizzbuzz import FizzBuzzGame


class GameSelector:
    games: List[CountingGame] = [CountUpGame, SevenUpGame, FizzBuzzGame, SevenUpHardGame, SevenUpFactorsGame]

    @classmethod
    def get_game_by_id(cls, game_id: int) -> CountingGame:
        return cls.games[game_id]

    @classmethod
    def get_id_by_game(cls, game: CountingGame) -> int:
        return cls.games.index(game)
