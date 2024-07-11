import re
from pathlib import Path

nono_chars = ["{", "}"]


def extract_headings_from_markdown(markdown_file) -> list:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    headings = re.findall(r"^#+\s+(.+)$", markdown_content, flags=re.MULTILINE)
    del headings[0]
    toc_headings = []
    for h in headings:
        ht = "#" + "-".join(h.lower().replace("`", "").split(" "))
        ht = ht.replace("?", "")
        toc_headings.append(ht)
    return toc_headings


def list_files_in_directory(directory: str) -> list:
    path = Path(directory)
    files = [str(file) for file in path.iterdir() if file.is_file()]
    return files


def get_code_from_markdown(lines: list[str], *, language: str = "python") -> list[str]:
    """Outputs extracted code blocks from a list of strings of markdown text"""
    # from: https://github.com/tassaron/get_code_from_markdown
    regex = re.compile(
        r"(?P<start>^```(?P<block_language>(\w|-)+)\n)(?P<code>.*?\n)(?P<end>```)",
        re.DOTALL | re.MULTILINE,
    )
    blocks = [(match.group("block_language"), match.group("code")) for match in regex.finditer("".join(lines))]
    return [block for block_language, block in blocks if block_language == language]


def load_md_doc(md_filepath: str) -> str:
    with open(md_filepath, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    return markdown_content
