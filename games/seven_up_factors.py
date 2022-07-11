from typing import List

from games import SevenUpHardGame


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
