from typing import List

import discord

from .seven_up_hard import SevenUpHardGame


# Exactly the same as SevenUpHard, except with a modified check_number_up
class SevenUpFactorsGame(SevenUpHardGame):
    @classmethod
    def factorise(cls, number: int) -> List[int]:
        factors: List[int] = []
        i: int = 1
        while i * i <= number:
            if not number % i:
                factors.append(i)
                if i != number // i:
                    factors.append(number // i)
            i += 1

        return factors

    @classmethod
    def check_number_up(cls, number: int) -> int:
        number_up = 0
        for factor in cls.factorise(number):
            while factor >= 1:
                number_up += factor % 10 == 7
                factor //= 10

        return number_up

    @classmethod
    def get_title(cls) -> str:
        return "Seven Up (Factors Mode)"

    @classmethod
    def get_embed(cls) -> discord.Embed:
        return discord.Embed(
            title=cls.get_title(),
            description="An extreme, math-nerd version of 7up!\n"
            + "To determine what to say, first, factorise the number.\n"
            + "Check how many times the number `7` appears in this factor list.\n"
            + "That translates to how many times you should say `Up`!\n"
            + "Example: `1` -> `1`, `7` -> `Up`, `14` -> `Up`, "
            + "`49` -> `Up`, `77` -> `Up Up Up`\n"
            + "Per usual: A person cannot say two numbers in a row!",
        )
