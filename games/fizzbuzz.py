import discord

from .base import CountingGame, ValidationResult, buzz_matcher, fizz_matcher, number_matcher


class FizzBuzzGame(CountingGame):
    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        is_fizz = not number % 3
        is_buzz = not number % 5
        is_number = not is_fizz and not is_buzz

        has_fizz = fizz_matcher.search(to_check) is not None
        has_buzz = buzz_matcher.search(to_check) is not None

        numbers = number_matcher.findall(to_check)
        number_str = str(number)
        has_number = len(numbers) != 0 and all(entered_number == number_str for entered_number in numbers)

        if not any((has_fizz, has_buzz, len(numbers))):
            return ValidationResult.UNRELATED

        return ValidationResult.from_bool((is_fizz, is_buzz, is_number) == (has_fizz, has_buzz, has_number))

    @classmethod
    def get_solution(cls, number: int) -> str:
        is_fizz = not number % 3
        is_buzz = not number % 5

        if not is_fizz and not is_buzz:
            return str(number)

        return ("Fizz" if is_fizz else "") + ("Buzz" if is_buzz else "")

    @classmethod
    def get_title(cls) -> str:
        return "FizzBuzz"

    @classmethod
    def get_embed(cls) -> discord.Embed:
        return discord.Embed(
            title=cls.get_title(),
            description="The classic game of FizzBuzz!\n"
            + "When a number divides `3`, say `Fizz`!\n"
            + "When a number divides `5`, say `Buzz`!\n"
            + "When it divides both, say `FizzBuzz`!\n"
            "Example: `1` -> `1`, `3` -> `Fizz`, `5` -> `Buzz`, "
            + "`15` -> `FizzBuzz`!\n"
            + "Per usual: A person cannot say two numbers in a row!",
        )
