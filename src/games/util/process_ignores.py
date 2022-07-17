import re

from util import MarkdownNode, parse_markdown

to_ignore = MarkdownNode.CODE_BLOCK | MarkdownNode.SPOILER | MarkdownNode.BLOCKQUOTE


match_mentions = re.compile(r"<@[!&]*\d+>", re.ASCII)
match_channels = re.compile(r"<#\d+>", re.ASCII)
match_custom_emotes = re.compile(r"<:[a-z_]+:\d+>", re.IGNORECASE | re.ASCII)


def process_ignores(message: str) -> str:
    ast = parse_markdown(message)
    no_markdown_str = "".join("" if node_type & to_ignore else content for node_type, content in ast)
    no_markdown_str = match_mentions.sub("", no_markdown_str)
    no_markdown_str = match_channels.sub("", no_markdown_str)
    no_markdown_str = match_custom_emotes.sub("", no_markdown_str)
    return no_markdown_str
