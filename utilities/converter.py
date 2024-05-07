import yaml
import subprocess
from utilities import base_dir


def collect_mkdocks_toc():
    # open mkdocs toc and collect all entries
    file_path = f"{base_dir}/mkdocs.yml"
    with open(file_path, "r") as file:
        mkdocks_toc = yaml.safe_load(file)
                
    # upnack toc
    home_doc = mkdocks_toc["nav"][0]["Home"]
    pipeline_examples_docs = mkdocks_toc["nav"][1]["Pipeline examples"]
    modules_overview = mkdocks_toc["nav"][2]["Modules"][0]["overview"]
    modules_docs = mkdocks_toc["nav"][2]["Modules"][1]["currently available"]
    system_overview = mkdocks_toc["nav"][3]["System"][0]["overview"]
    system_docs = mkdocks_toc["nav"][3]["System"][1]["methods"]

    # collect paths to example docs
    examples_mds = [home_doc, modules_overview, system_overview]
    for item in pipeline_examples_docs:
        item_values = list(item.values())[0]
        if isinstance(item_values, str):
            examples_mds.append(item_values)
        else:
            for subitem in item_values:
                docpath = list(subitem.values())[0]
                examples_mds.append(docpath)
        
    # collect paths to system docs
    system_mds = []
    for item in system_docs:
        docpath = list(item.values())[0]
        system_mds.append(docpath)
        
    # collect paths to modules docs
    modules_mds = []
    for item in modules_docs:
        docpath = list(item.values())[0]
        modules_mds.append(docpath)
        
    # merge all mds
    all_mds = examples_mds + system_mds + modules_mds
    return all_mds


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
            "markdown"
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
        docpath = f"{base_dir}/docs/" + all_toc_files[i].replace(".md",".ipynb")
        convert_notebook_remove(docpath)


def convert_notebook_no_remove(docpath: str) -> None:
    try:
        command = [
            "jupyter",
            "nbconvert",
            f"{docpath}",
            "--TagRemovePreprocessor.enabled=True",
            "--to",
            "markdown"
        ]
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
        docpath = f"{base_dir}/docs/" + all_toc_files[i].replace(".md",".ipynb")
        convert_notebook_no_remove(docpath)