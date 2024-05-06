import yaml
import subprocess


def collect_mkdocks_toc():
    # open mkdocs toc and collect all entries
    file_path = "../mkdocs.yml"
    with open(file_path, "r") as file:
        mkdocks_toc = yaml.safe_load(file)

    # upnack toc
    pipeline_examples_docs = mkdocks_toc["nav"][3]["Pipeline examples"]
    system_docs = mkdocks_toc["nav"][5]["System"][0]["methods"]
    modules_docs = mkdocks_toc["nav"][4]["Modules"][0]["currently available"]

    # collect paths to example docs
    examples_mds = []
    for item in pipeline_examples_docs:
        item_values = list(item.values())[0]
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


def convert_notebook(docpath: str) -> None:
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


def convert_all_notebooks():
    # collect all toc entries from mkdocs yaml
    all_toc_files = collect_mkdocks_toc()
    
    # convert files
    for i in range(len(all_toc_files)):
        docpath = "../docs/" + all_toc_files[i].replace(".md",".ipynb")
        convert_notebook(docpath)
