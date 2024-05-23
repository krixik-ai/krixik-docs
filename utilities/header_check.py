from utilities.utilities import extract_headings_from_markdown, nono_chars
from utilities import base_dir


def check_file_headers(markdown_file: str) -> list:
    headers = extract_headings_from_markdown(f"{base_dir}/docs/" + markdown_file)
    dead_headers = []
    for h in headers:
        for no in nono_chars:
            if no in h:
                dead_headers.append(h)
                continue
    return dead_headers
