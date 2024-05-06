import pytest
from utilities.converter import convert_all_notebooks
from utilities.converter import collect_mkdocks_toc
from utilities.link_check import check_file_links
from utilities.name_check import duplicate_name_check


def test_1():
    """success test that notebook to markdown conversion"""
    convert_all_notebooks()


toc_files = collect_mkdocks_toc()
@pytest.mark.parametrize("docfile", toc_files)
def test_2(docfile):
    """success test that all links from each notebook are valid"""
    dead_links = check_file_links(docfile, toc_files)
    assert len(dead_links) == 0, f"doc {docfile} has deadlinks: {dead_links}"


def test_3():
    """ success test that pipeline names are unique per page """
    assert duplicate_name_check()
