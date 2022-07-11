from .base import CountingGame, ValidationResult, number_matcher


class CountUpGame(CountingGame):
    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        # Check if this string satisfies constraints for this number.
        # Rules:
        #   The only number that can appear is the target number.
        numbers = number_matcher.findall(to_check)

        if len(numbers) == 0:
            return ValidationResult.UNRELATED

        number_str = str(number)

        has_number = all(entered_number == number_str for entered_number in numbers)

        return ValidationResult.from_bool(has_number)

    @classmethod
    def get_solution(cls, number: int) -> str:
        return str(number)
