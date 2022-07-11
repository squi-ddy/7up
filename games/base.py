from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import auto, IntEnum, unique


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


up_matcher = re.compile("up", re.IGNORECASE)
number_matcher = re.compile(r"\d+")
fizz_matcher = re.compile("fizz", re.IGNORECASE)
buzz_matcher = re.compile("buzz", re.IGNORECASE)
