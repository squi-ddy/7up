import re
import sys

__all__ = ["whitespace"]

s = "".join(chr(c) for c in range(sys.maxunicode + 1))
whitespace = "".join(re.findall(r"\s", s))
