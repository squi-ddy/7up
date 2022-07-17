import random
import string

import pytest

from games.util import process_ignores

performance_tests = ["> ||" + "***__`foobar`__***" * 200 + "||", "|" * 2000, "||***__" + "a" * 2000 + "__***||"]

random_characters = string.printable

random_lengths = [10, 100, 1000, 2000]


@pytest.mark.parametrize("test_in", performance_tests, ids=[i + 1 for i in range(len(performance_tests))])
def test_ignore_performance(test_in, benchmark):
    benchmark(process_ignores, test_in)


@pytest.mark.parametrize("length", random_lengths)
def test_ignore_random(length, benchmark):
    @benchmark
    def random_markdown_parse():
        to_parse = "".join(random.choice(random_characters) for _ in range(length))

        process_ignores(to_parse)
