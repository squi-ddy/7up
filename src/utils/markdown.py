from __future__ import annotations

from enum import Flag, auto, unique
from typing import List, Sequence, Tuple


# noinspection PyArgumentList
@unique
class MarkdownNode(Flag):
    DEFAULT = auto()
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    CODE_BLOCK = auto()
    BLOCKQUOTE = auto()
    SPOILER = auto()


chars_to_node: Sequence[Tuple[str, MarkdownNode]] = [
    ("***", MarkdownNode.BOLD | MarkdownNode.ITALIC),
    ("**", MarkdownNode.BOLD),
    ("*", MarkdownNode.ITALIC),
    ("___", MarkdownNode.UNDERLINE | MarkdownNode.ITALIC),
    ("__", MarkdownNode.UNDERLINE),
    ("_", MarkdownNode.ITALIC),
    ("||", MarkdownNode.SPOILER),
    ("```", MarkdownNode.CODE_BLOCK),
    ("`", MarkdownNode.CODE_BLOCK),
]

special_characters = ["*", "_", "|", "`"]


# For efficiency purposes, this is a separate function
def _parse_markdown_no_blockquote(
    input_markdown: str, *, _inside: MarkdownNode = MarkdownNode.DEFAULT
) -> Sequence[Tuple[MarkdownNode, str]]:
    if _inside & MarkdownNode.CODE_BLOCK:
        # don't interpret stuff in code blocks
        return [(_inside, input_markdown)]

    return_tree: List[Tuple[MarkdownNode, str]] = []
    return_text = []

    i = 0
    while i < len(input_markdown):
        if input_markdown[i] == "\\":
            append_backslash = not (i + 1 < len(input_markdown) and input_markdown[i + 1] in special_characters)

            if append_backslash:
                return_text.append(input_markdown[i])

            if i + 1 < len(input_markdown):
                return_text.append(input_markdown[i + 1])

            i += 2

            continue

        for characters, node_type in chars_to_node:
            if input_markdown.startswith(characters, i):
                if characters == "*" and input_markdown.startswith(characters + " ", i):
                    # discord doesn't match this, we shouldn't either
                    continue

                start_index = i + len(characters)
                # greedily match
                try:
                    end_index = input_markdown.index(characters, i + len(characters))

                    if characters == "```":
                        # ignore first line if it is multiline
                        try:
                            new_start_index = input_markdown.index("\n", i + len(characters))
                            if new_start_index < end_index:
                                start_index = new_start_index
                        except ValueError:
                            pass

                    if characters == "*":
                        # discord doesn't match if a * has a space in front, this deals with that.
                        try:
                            while input_markdown[end_index - 1] == " ":
                                end_index = input_markdown.index(characters, end_index + len(characters))
                        except ValueError:
                            # False match
                            continue

                    return_tree.append((_inside, "".join(return_text)))
                    return_tree.extend(
                        _parse_markdown_no_blockquote(
                            input_markdown[start_index:end_index],
                            _inside=(_inside | node_type),
                        ),
                    )
                    return_tree.extend(
                        _parse_markdown_no_blockquote(input_markdown[end_index + len(characters) :], _inside=_inside)
                    )
                    return return_tree
                except ValueError:
                    continue

        return_text.append(input_markdown[i])

        i += 1

    return [(_inside, "".join(return_text))]


def parse_markdown(
    input_markdown: str, *, _inside: MarkdownNode = MarkdownNode.DEFAULT
) -> Sequence[Tuple[MarkdownNode, str]]:
    return_tree: List[Tuple[MarkdownNode, str]] = []

    lines = input_markdown.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("> "):
            return_tree.extend(_parse_markdown_no_blockquote("\n".join(lines[:idx]), _inside=_inside))
            return_tree.extend(_parse_markdown_no_blockquote(line[2:], _inside=(_inside | MarkdownNode.BLOCKQUOTE)))
            return_tree.extend(parse_markdown("\n".join(lines[idx + 1 :]), _inside=_inside))
            return return_tree

        elif line.startswith(">>> "):
            return_tree.extend(_parse_markdown_no_blockquote("\n".join(lines[:idx]), _inside=_inside))
            return_tree.extend(
                _parse_markdown_no_blockquote("\n".join(lines[idx:])[4:], _inside=(_inside | MarkdownNode.BLOCKQUOTE))
            )
            return return_tree

    return _parse_markdown_no_blockquote(input_markdown, _inside=_inside)
