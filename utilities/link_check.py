import markdown
import re


def extract_links_from_markdown(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_content)
    return links


def check_file_links(filepath: str,
                     toc_files: list) -> None:
    try:
        links = extract_links_from_markdown("../docs/" + filepath)
        for link in links:
            toc_files.index(link)
    except FileNotFoundError:
        print(f"FAILURE: check_file_links failed - file {filepath} does not exist")
    except Exception as e:
        print(f"FAILURE: check_file_links failed for file {filepath} with exception {e}")