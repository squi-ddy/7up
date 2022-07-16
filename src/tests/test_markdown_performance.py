import random
import string

import pytest

from util import parse_markdown

performance_tests = ["> ||" + "***__`foobar`__***" * 200 + "||", "|" * 2000, "||***__" + "a" * 2000 + "__***||"]

random_characters = string.printable

random_lengths = [10, 100, 1000, 2000]


@pytest.mark.parametrize("test_in", performance_tests, ids=[i + 1 for i in range(len(performance_tests))])
def test_markdown_performance(test_in, benchmark):
    benchmark(parse_markdown, test_in)


@pytest.mark.parametrize("length", random_lengths)
def test_markdown_random(length, benchmark):
    @benchmark
    def random_markdown_parse():
        to_parse = "".join(random.choice(random_characters) for _ in range(length))

        parse_markdown(to_parse)
