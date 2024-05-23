import yaml
import subprocess
from utilities import base_dir


def get_all_values(nested_dict: dict) -> list:
    values = []

    def extract_values(d):
        if isinstance(d, dict):
            for key, value in d.items():
                if isinstance(value, dict):
                    extract_values(value)
                elif isinstance(value, list):
                    for item in value:
                        extract_values(item)
                else:
                    values.append(value)
        elif isinstance(d, list):
            for item in d:
                extract_values(item)
        else:
            values.append(d)

    extract_values(nested_dict)
    return values


def collect_mkdocks_toc():
    # open mkdocs toc and collect all entries
    file_path = f"{base_dir}/mkdocs.yml"
    with open(file_path, "r") as file:
        mkdocks_toc = yaml.safe_load(file)
    return get_all_values(mkdocks_toc["nav"])


def convert_notebook_remove(docpath: str) -> None:
    try:
        command = [
            "jupyter",
            "nbconvert",
            f"{docpath}",
            "--TagRemovePreprocessor.enabled=True",
            "--TagRemovePreprocessor.remove_cell_tags=['remove_cell']",
            "--TagRemovePreprocessor.remove_all_outputs_tags=['remove_output']",
            "--to",
            "markdown",
        ]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            print(f"FAILURE: notebook to markdown conversion failed with error: {process.stderr.decode().strip()}")
    except Exception as e:
        print(f"FAILURE: notebook to markdown conversion failed with exception {e}")


def convert_all_notebooks_remove():
    # collect all toc entries from mkdocs yaml
    all_toc_files = collect_mkdocks_toc()

    # convert files
    for i in range(len(all_toc_files)):
        docpath = f"{base_dir}/docs/" + all_toc_files[i].replace(".md", ".ipynb")
        convert_notebook_remove(docpath)


def convert_notebook_no_remove(docpath: str) -> None:
    try:
        command = ["jupyter", "nbconvert", f"{docpath}", "--TagRemovePreprocessor.enabled=True", "--to", "markdown"]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            print(f"FAILURE: notebook to markdown conversion failed with error: {process.stderr.decode().strip()}")
    except Exception as e:
        print(f"FAILURE: notebook to markdown conversion failed with exception {e}")


def convert_all_notebooks_no_remove():
    # collect all toc entries from mkdocs yaml
    all_toc_files = collect_mkdocks_toc()

    # convert files
    for i in range(len(all_toc_files)):
        docpath = f"{base_dir}/docs/" + all_toc_files[i].replace(".md", ".ipynb")
        convert_notebook_no_remove(docpath)
