from utils import MarkdownNode, parse_markdown


def has_node_type(ast, target_node):
    for node_type, content in ast:
        if node_type == target_node or (
            target_node in (MarkdownNode.BOLD, MarkdownNode.ITALIC) and node_type == MarkdownNode.BOLD_ITALIC
        ):
            return True

        if not isinstance(content, str) and has_node_type(content, target_node):
            return True

    return False


test_cases = [
    ("*foo `bar* baz`", [MarkdownNode.ITALIC], [MarkdownNode.CODEBLOCK]),
    ("`*foo*`", [MarkdownNode.CODEBLOCK], [MarkdownNode.ITALIC]),
    (
        "> ||***__`foobar`__***||",
        [
            MarkdownNode.ITALIC,
            MarkdownNode.BOLD,
            MarkdownNode.CODEBLOCK,
            MarkdownNode.SPOILER,
            MarkdownNode.UNDERLINE,
            MarkdownNode.BLOCKQUOTE,
        ],
        [],
    ),
    ("*\n>>> foo*\nbar\nbaz", [MarkdownNode.BLOCKQUOTE], [MarkdownNode.ITALIC]),
    ("*\n\n*", [MarkdownNode.ITALIC], []),
]


def test_markdown():
    for input_markdown, has, does_not_have in test_cases:
        tree = parse_markdown(input_markdown)

        for case in has:
            assert has_node_type(tree, case) is True

        for case in does_not_have:
            assert has_node_type(tree, case) is False
