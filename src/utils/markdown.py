from __future__ import annotations

from enum import IntEnum, auto
from typing import Optional, Sequence, Tuple, Union


# noinspection PyArgumentList
class MarkdownNode(IntEnum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    BOLD_ITALIC = auto()
    UNDERLINE = auto()
    CODEBLOCK = auto()
    BLOCKQUOTE = auto()
    SPOILER = auto()
    TREE = auto()


MarkdownTree = Sequence[Tuple[MarkdownNode, Union[str, "MarkdownTree"]]]  # type: ignore

chars_to_node: Sequence[Tuple[str, MarkdownNode]] = [
    ("***", MarkdownNode.BOLD_ITALIC),
    ("**", MarkdownNode.BOLD),
    ("*", MarkdownNode.ITALIC),
    ("__", MarkdownNode.UNDERLINE),
    ("_", MarkdownNode.ITALIC),
    ("||", MarkdownNode.SPOILER),
    ("```", MarkdownNode.CODEBLOCK),
    ("`", MarkdownNode.CODEBLOCK),
]


def parse_markdown(
    input_markdown: str, *, _check_blockquote: bool = True, _inside: Optional[MarkdownNode] = None
) -> MarkdownTree:
    if _check_blockquote:
        lines = input_markdown.split("\n")
        for idx, line in enumerate(lines):
            if line.startswith("> "):
                return [
                    (MarkdownNode.TREE, parse_markdown("\n".join(lines[:idx]), _check_blockquote=False)),  # before
                    (MarkdownNode.BLOCKQUOTE, parse_markdown(line[2:], _check_blockquote=False)),  # inside
                    (MarkdownNode.TREE, parse_markdown("\n".join(lines[idx + 1 :]))),  # after
                ]

            elif line.startswith(">>> "):
                return [
                    (MarkdownNode.TREE, parse_markdown("\n".join(lines[:idx]), _check_blockquote=False)),  # before
                    (
                        MarkdownNode.BLOCKQUOTE,
                        parse_markdown("\n".join(lines[idx:])[4:], _check_blockquote=False),
                    ),  # inside
                ]

    if _inside != MarkdownNode.CODEBLOCK:
        for i in range(len(input_markdown)):
            for characters, node_type in chars_to_node:
                if input_markdown.startswith(characters, i):
                    start_index = i + len(characters)
                    # greedily match
                    try:
                        end_index = input_markdown.index(characters, i + len(characters)) + len(characters)
                        print(input_markdown, characters, end_index)

                        if characters == "```":
                            # ignore first line if it is multiline
                            try:
                                new_start_index = input_markdown.index("\n", i + len(characters))
                                if new_start_index < end_index:
                                    start_index = new_start_index
                            except ValueError:
                                pass
                        return [
                            (MarkdownNode.TEXT, input_markdown[:i]),
                            (
                                node_type,
                                parse_markdown(
                                    input_markdown[start_index : end_index - len(characters)],
                                    _check_blockquote=False,
                                    _inside=node_type,
                                ),
                            ),
                            (MarkdownNode.TREE, parse_markdown(input_markdown[end_index:], _check_blockquote=False)),
                        ]
                    except ValueError:
                        continue

    return [(MarkdownNode.TEXT, input_markdown)]
