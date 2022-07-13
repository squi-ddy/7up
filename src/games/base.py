from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum, auto, unique
from typing import TYPE_CHECKING, Any

import regex

if TYPE_CHECKING:
    from nextcord import Embed


# noinspection PyArgumentList
@unique
class ValidationResult(IntEnum):
    ACCEPT = auto()
    REJECT = auto()
    UNRELATED = auto()

    @classmethod
    def from_bool(cls, value: bool) -> ValidationResult:
        return ValidationResult.ACCEPT if value else ValidationResult.REJECT


class CountingGame(ABC):
    @classmethod
    @abstractmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        pass

    @classmethod
    @abstractmethod
    def get_solution(cls, number: int) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_title(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_embed(cls) -> Embed:
        pass


def get_matcher(to_match: str) -> regex.Pattern[Any]:
    return regex.compile(
        rf"(?<!^[^`]*(`[^`]*`[^`]*)*`[^`]*){to_match}", regex.IGNORECASE
    )  # kinda flawed but good enough


up_matcher = get_matcher("up")
number_matcher = get_matcher(r"(?<=[a-z !?.,\-^*(]|^)(?P<number>[0-9]+)(?=[a-z !?.,\-^*)]|$)")
fizz_matcher = get_matcher("fizz")
buzz_matcher = get_matcher("buzz")
