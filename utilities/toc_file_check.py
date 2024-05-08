import os
import fnmatch
from utilities import base_dir
from utilities.converter import collect_mkdocks_toc


def list_files_recursively(directory, exclude_list=None):
    if exclude_list is None:
        exclude_list = []

    file_list = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith(".md"):
                if not any(fnmatch.fnmatch(file_path, pattern) for pattern in exclude_list):
                    keeper_path = file_path.split("/docs/")[-1]
                    file_list.append(keeper_path)

    return file_list


def compare_toc_to_docs():
    mkdocks_toc = collect_mkdocks_toc()
    test_dir = base_dir + "/docs/"
    actual_md_files = list_files_recursively(test_dir)
    in_toc_no_docs = list(set(mkdocks_toc) - set(actual_md_files))
    in_docs_no_toc = list(set(actual_md_files) - set(mkdocks_toc))
    return in_toc_no_docs, in_docs_no_toc
