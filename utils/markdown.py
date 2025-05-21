# utils/markdown.py
import re

def extract_code_blocks(content):
    """
    Extracts all Python code blocks from a markdown-formatted string.
    Returns a list of code snippets (strings).
    """
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
    return [block.strip() for block in code_blocks if block.strip()]
