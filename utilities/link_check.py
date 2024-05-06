import markdown
import re
import requests
from utilities import base_dir


def extract_links_from_markdown(markdown_file: str) -> list:
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_content)
    return links


def extract_headings_from_markdown(markdown_file) -> list:
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    headings = re.findall(r'^#+\s+(.+)$', markdown_content, flags=re.MULTILINE)
    del headings[0]
    toc_headings = []
    for h in headings:
        ht = "#" + "-".join(h.lower().replace("`","").split(" "))
        toc_headings.append(ht)
    return toc_headings


def check_file_links(filepath: str,
                     toc_files: list) -> list:
    links = []
    headings = []
    try:
        links = extract_links_from_markdown(f"{base_dir}/docs/" + filepath)
        headings = extract_headings_from_markdown(f"{base_dir}/docs/" + filepath)
    except FileNotFoundError:
        print(f"FAILURE: check_file_links failed - file {filepath} does not exist")
    except Exception as e:
        print(f"FAILURE: check_file_links failed for file {filepath} with exception {e}")
    
    # filter out toc links and headings
    dead_links = []
    for link in links:
        if link not in toc_files and link not in headings:
            dead_links.append(link)
            
    # check dead links with requests
    last_dead_links = []
    for link in dead_links:
        response = requests.get(link)
        if response.status_code not in range(200, 404):
            last_dead_links.append(link)
    return last_dead_links

