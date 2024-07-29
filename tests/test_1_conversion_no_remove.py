import pytest
from utilities import base_dir
from utilities.converter import convert_notebook_no_remove, collect_mkdocks_toc

toc_files = collect_mkdocks_toc()
    
@pytest.mark.parametrize("docfile", toc_files)
def test_1(docfile):
    """success test that notebook to markdown conversion"""
    docpath = f"{base_dir}/docs/" + docfile.replace(".md", ".ipynb")
    print(f"docpath --> {docpath}")
    assert convert_notebook_no_remove(docpath) is None