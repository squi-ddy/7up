import pytest

from util import MarkdownNode, parse_markdown


def has_node_type(ast, target_node):
    return any(node_type & target_node for node_type, content in ast)


test_cases = [
    ("*foo `bar* baz`", [MarkdownNode.ITALIC], [MarkdownNode.CODE_BLOCK]),
    ("`*foo*`", [MarkdownNode.CODE_BLOCK], [MarkdownNode.ITALIC]),
    (
        "> ||***__`foobar`__***||",
        [
            MarkdownNode.ITALIC,
            MarkdownNode.BOLD,
            MarkdownNode.CODE_BLOCK,
            MarkdownNode.SPOILER,
            MarkdownNode.UNDERLINE,
            MarkdownNode.BLOCKQUOTE,
        ],
        [],
    ),
    ("*\n>>> foo*\nbar\nbaz", [MarkdownNode.BLOCKQUOTE], [MarkdownNode.ITALIC]),
    ("*\n\n*", [MarkdownNode.ITALIC], []),
    ("\\*foo `bar* baz`", [MarkdownNode.CODE_BLOCK], [MarkdownNode.ITALIC]),
    ("* foo `bar* baz`", [MarkdownNode.CODE_BLOCK], [MarkdownNode.ITALIC]),
]


@pytest.mark.parametrize("test_in, has, does_not_have", test_cases, ids=[i + 1 for i in range(len(test_cases))])
def test_markdown(test_in, has, does_not_have):
    tree = parse_markdown(test_in)

    for case in has:
        assert has_node_type(tree, case) is True

    for case in does_not_have:
        assert has_node_type(tree, case) is False
