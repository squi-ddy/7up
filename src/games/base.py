from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum, auto, unique
from typing import TYPE_CHECKING

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


up_matcher = regex.compile("up", regex.IGNORECASE)
number_matcher = regex.compile(r"(?<=[a-z !?.,\-^*]|^)(?P<number>[0-9]+)(?=[a-z !?.,\-^*]|$)", regex.IGNORECASE)
fizz_matcher = regex.compile("fizz", regex.IGNORECASE)
buzz_matcher = regex.compile("buzz", regex.IGNORECASE)
