from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import IntEnum, auto, unique
from typing import TYPE_CHECKING

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


up_matcher = re.compile("up", re.IGNORECASE)
number_matcher = re.compile(r"\d+", re.ASCII)
fizz_matcher = re.compile("foo", re.IGNORECASE)
buzz_matcher = re.compile("bar", re.IGNORECASE)
