from __future__ import annotations

import string
from enum import Flag, auto, unique
from typing import List, Sequence, Tuple

from util import unicode


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


# For efficiency purposes, this is a separate function
def _parse_markdown_no_blockquote(
    to_parse: str, *, _inside: MarkdownNode = MarkdownNode.DEFAULT, _start: int = 0, _end: int = -1
) -> Sequence[Tuple[MarkdownNode, str]]:
    if _inside & MarkdownNode.CODE_BLOCK:
        # don't interpret stuff in code blocks
        return [(_inside, to_parse[_start:_end])]

    return_tree: List[Tuple[MarkdownNode, str]] = []
    return_text = []

    i = _start
    while i < _end:
        if to_parse[i] == "\\":
            append_backslash = i + 1 >= _end or to_parse[i + 1] in string.ascii_letters

            if append_backslash:
                return_text.append(to_parse[i])

            if i + 1 < _end:
                return_text.append(to_parse[i + 1])

            i += 2

            continue

        for characters, node_type in chars_to_node:
            if to_parse.startswith(characters, i, _end):
                if characters == "*" and i + 1 < _end and to_parse[i + 1] in unicode.whitespace:
                    # discord doesn't match this, we shouldn't either
                    continue

                start_index = i + len(characters)
                # greedily match
                end_index = to_parse.find(characters, start_index, _end)

                if end_index == -1:
                    continue

                if characters == "```":
                    # ignore until first whitespace if multiline
                    if to_parse.find("\n", start_index, end_index) != -1:
                        new_start_index = _string_find_char(to_parse, unicode.whitespace, start_index, end_index)
                        if new_start_index < end_index:
                            start_index = new_start_index

                return_tree.append((_inside, "".join(return_text)))
                return_tree.extend(
                    _parse_markdown_no_blockquote(
                        to_parse, _inside=(_inside | node_type), _start=start_index, _end=end_index
                    ),
                )
                return_tree.extend(
                    _parse_markdown_no_blockquote(
                        to_parse, _inside=_inside, _start=end_index + len(characters), _end=_end
                    )
                )
                return return_tree

        return_text.append(to_parse[i])

        i += 1

    return [(_inside, "".join(return_text))]


def _parse_markdown_blockquote(
    to_parse: str, *, _inside: MarkdownNode = MarkdownNode.DEFAULT, _start: int, _end: int
) -> Sequence[Tuple[MarkdownNode, str]]:
    return_tree: List[Tuple[MarkdownNode, str]] = []

    current_newline = _start - 1
    prev_newline: int

    while current_newline < _end:
        prev_newline = current_newline + 1
        current_newline = location if (location := to_parse.find("\n", prev_newline, _end)) != -1 else _end

        if to_parse.startswith("> ", prev_newline, current_newline):
            return_tree.extend(
                _parse_markdown_no_blockquote(to_parse, _inside=_inside, _start=_start, _end=prev_newline)
            )
            return_tree.extend(
                _parse_markdown_no_blockquote(
                    to_parse, _inside=(_inside | MarkdownNode.BLOCKQUOTE), _start=prev_newline + 2, _end=current_newline
                )
            )
            return_tree.extend(_parse_markdown_blockquote(to_parse, _inside=_inside, _start=current_newline, _end=_end))
            return return_tree

        elif to_parse.startswith(">>> ", prev_newline, current_newline):
            return_tree.extend(
                _parse_markdown_no_blockquote(to_parse, _inside=_inside, _start=_start, _end=prev_newline)
            )
            return_tree.extend(
                _parse_markdown_no_blockquote(
                    to_parse, _inside=(_inside | MarkdownNode.BLOCKQUOTE), _start=prev_newline + 4, _end=_end
                )
            )
            return return_tree

    return _parse_markdown_no_blockquote(to_parse, _inside=_inside, _start=_start, _end=_end)


def _string_find_char(to_parse: str, to_look: str, start: int = 0, end: int = -1) -> int:
    for index in range(start, end):
        if to_parse[index] in to_look:
            return index

    return -1


def parse_markdown(to_parse: str) -> Sequence[Tuple[MarkdownNode, str]]:
    return _parse_markdown_blockquote(to_parse, _start=0, _end=len(to_parse))
