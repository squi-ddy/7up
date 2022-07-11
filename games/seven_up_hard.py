from .base import CountingGame, ValidationResult, up_matcher, number_matcher


class SevenUpHardGame(CountingGame):
    @classmethod
    def check_number_up(cls, number: int) -> int:
        number_up: int = number % 7 == 0
        while number >= 1:
            number_up += number % 10 == 7
            number //= 10

        return number_up

    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        number_up: int = cls.check_number_up(number)
        is_number = not number_up

        number_up_in_str = len(up_matcher.findall(to_check))
        numbers = number_matcher.findall(to_check)
        number_str = str(number)
        has_number = len(numbers) != 0 and all(entered_number == number_str for entered_number in numbers)

        if not has_number and not number_up_in_str:
            # unrelated message
            return ValidationResult.UNRELATED

        return ValidationResult.from_bool((number_up, is_number) == (number_up_in_str, has_number))

    @classmethod
    def get_solution(cls, number: int) -> str:
        return "Up " * no_up if (no_up := cls.check_number_up(number)) else str(number)
