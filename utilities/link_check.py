import re
import os
import markdown
import requests
from utilities import base_dir
from utilities.utilities import extract_headings_from_markdown, nono_chars

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}


def extract_links_from_markdown(markdown_file: str) -> tuple:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_content)

    # split into intra, inter, and outer links
    inter_links = []
    intra_links = []
    outer_links = []
    for link in links:
        if link[0] == "#":
            intra_links.append(link)
        elif link[:4] == "http":
            outer_links.append(link)
        else:
            # convert to absolute link
            absolute_link = os.path.abspath(os.path.join(os.path.dirname(markdown_file), link))
            absolute_link = "docs/" + absolute_link.split("/docs/", 1)[-1]
            inter_links.append(absolute_link)

    return intra_links, inter_links, outer_links


def check_file_links(filepath: str, toc_files: list) -> list:
    intra_links = []
    inter_links = []
    outer_links = []
    headings = []
    try:
        intra_links, inter_links, outer_links = extract_links_from_markdown(f"{base_dir}/docs/" + filepath)
        headings = extract_headings_from_markdown(f"{base_dir}/docs/" + filepath)
    except FileNotFoundError:
        print(f"FAILURE: check_file_links failed - file {filepath} does not exist")
    except Exception as e:
        print(f"FAILURE: check_file_links failed for file {filepath} with exception {e}")

    dead_links = []

    # check intra_links for dead links
    for link in intra_links:
        for no in nono_chars:
            if no in link:
                dead_links.append(link)
                continue
        if link not in headings:
            dead_links.append(link)

    # check inter_links for dead links
    toc_files = ["docs/" + v for v in toc_files]
    for link in inter_links:
        for no in nono_chars:
            if no in link:
                dead_links.append(link)
                continue

        # check if link directs to heading
        if "#" in link:
            link_split = link.split("#")
            if len(link_split) != 2:
                dead_links.append(link)
                continue
            page = link_split[0]
            specific_heading = link_split[1]
            if page not in toc_files:
                dead_links.append(link)
                continue
            headings = extract_headings_from_markdown(f"{base_dir}/" + page)
            if "#" + specific_heading not in headings:
                dead_links.append(link)
        elif link not in toc_files:
            dead_links.append(link)

    for link in outer_links:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code not in [200, 403, 429]:
            print(f"link {link} failed with response {response}")  # very strange - this line seems necessary for tests to pass on github
            dead_links.append(link)

    dead_links = [v for v in dead_links if "info@krixik.com" not in v]

    return dead_links


def check_readme_links() -> list:
    intra_links = []
    inter_links = []
    outer_links = []
    headings = []
    filepath = ""
    try:
        filepath = f"{base_dir}/" + "README.md"
        intra_links, inter_links, outer_links = extract_links_from_markdown(filepath)
        headings = extract_headings_from_markdown(filepath)
    except FileNotFoundError:
        print(f"FAILURE: check_file_links failed - file {filepath} does not exist")
    except Exception as e:
        print(f"FAILURE: check_file_links failed for file {filepath} with exception {e}")

    dead_links = []

    # check intra_links for dead links
    for link in intra_links:
        for no in nono_chars:
            if no in link:
                dead_links.append(link)
                break
        if link not in headings:
            dead_links.append(link)

    for link in outer_links:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code not in [200, 403, 429]:
            print(f"link {link} failed with response {response}")  # very strange - this line seems necessary for tests to pass on github
            dead_links.append(link)

    dead_links = [v for v in dead_links if "info@krixik.com" not in v]

    return dead_links
