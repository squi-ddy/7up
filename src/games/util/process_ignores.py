from utils import parse_markdown, MarkdownNode

to_ignore = MarkdownNode.CODE_BLOCK | MarkdownNode.SPOILER | MarkdownNode.BLOCKQUOTE


def process_ignores(message: str) -> str:
    ast = parse_markdown(message)
    return "".join("" if node_type & to_ignore else content for node_type, content in ast)
