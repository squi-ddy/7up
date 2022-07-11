from .base import CountingGame, ValidationResult, up_matcher, number_matcher


class SevenUpGame(CountingGame):
    @classmethod
    def check_is_up(cls, number: int) -> bool:
        is_up = not number % 7
        while not is_up and number >= 1:
            is_up = number % 10 == 7
            number //= 10

        return is_up

    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        is_up: bool = cls.check_is_up(number)
        is_number = not is_up

        has_up = up_matcher.search(to_check) is not None
        numbers = number_matcher.findall(to_check)
        number_str = str(number)
        has_number = len(numbers) != 0 and all(entered_number == number_str for entered_number in numbers)

        if not has_up and not has_number:
            # unrelated message
            return ValidationResult.UNRELATED

        return ValidationResult.from_bool((is_up, is_number) == (has_up, has_number))

    @classmethod
    def get_solution(cls, number: int) -> str:
        return "Up" if cls.check_is_up(number) else str(number)
