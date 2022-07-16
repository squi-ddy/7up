from typing import Any, Optional


def int_or_null(value: Any) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None
