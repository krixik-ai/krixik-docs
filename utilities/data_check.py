import os
import re
from utilities.converter import collect_mkdocks_toc
from utilities import base_dir
from utilities.utilities import get_code_from_markdown, load_md_doc, list_files_in_directory

acceptable_extensions = ["txt", "docx", "pptx", "png", "jpg", "jpeg", "mp3", "npy", "json"]
all_input_data_links = list_files_in_directory(base_dir + "/data/input/")


def is_attempted_data_path(input_string: str) -> bool:
    pattern = r"^(?!#)\w+\s*=\s*(['\"]).*?\1"
    return bool(re.match(pattern, input_string))


def is_data_input_path(input_string: str) -> bool:
    pattern = r".*input/.*"
    return bool(re.match(pattern, input_string))


def is_data_output_path(input_string: str) -> bool:
    pattern = r".*output/.*"
    return bool(re.match(pattern, input_string))


def extract_quoted_portion(input_string: str) -> list:
    # Check if the string does not start with #
    if input_string.startswith("#"):
        return []

    # Regex pattern to find all quoted portions in the string
    pattern = r"['\"](.*?)['\"]"

    # Find all matches
    matches = re.findall(pattern, input_string)

    return matches


def check_all_page_data_links() -> tuple:
    # get all doc links from toc
    all_docs = collect_mkdocks_toc()

    # loop over docs, examine data links
    all_page_data_links = []
    all_page_dead_links = []
    for i, page in enumerate(all_docs):
        # get md code blocks for next doc
        md_filepath = base_dir + "/docs/" + all_docs[i]
        markdown_content = load_md_doc(md_filepath)
        code_blocks = get_code_from_markdown([markdown_content])

        # loop over code blocks and extract data links
        page_data_links = []
        for block in code_blocks:
            lines = block.split("\n")
            lines = [v for v in lines if len(v) > 0]
            for line in lines:
                extraction = extract_quoted_portion(line)
                if len(extraction) > 0:
                    for element in extraction:
                        if is_data_input_path(element):
                            for ext in acceptable_extensions:
                                if element.endswith(ext):
                                    absolute_link = os.path.abspath(os.path.join(os.path.dirname(md_filepath), "../../../data", element))
                                    page_data_links.append(absolute_link)

        page_data_links = list(set(page_data_links))
        all_page_data_links += page_data_links
        dead_page_links = [v for v in page_data_links if v not in all_input_data_links]
        if len(dead_page_links) > 0:
            page_entry = {}
            page_entry["page"] = md_filepath
            page_entry["dead_page_links"] = dead_page_links
            all_page_dead_links.append(page_entry)
    return list(set(all_page_data_links)), all_page_dead_links


def check_for_dead_data_links() -> tuple:
    # collect all data links from page, and dead links not present in data/input/
    all_page_data_links, all_page_dead_links = check_all_page_data_links()

    # collect all links in data/input not present in all data links collected from pages
    all_data_dead_links = list(set(all_input_data_links) - set(all_page_data_links))
    return all_page_dead_links, all_data_dead_links
