import pytest
from utilities.converter import collect_mkdocks_toc
from utilities.link_check import check_file_links, check_readme_links


toc_files = collect_mkdocks_toc()


@pytest.mark.parametrize("docfile", toc_files)
def test_1(docfile):
    """success test that all links from each notebook are valid"""
    dead_links = check_file_links(docfile, toc_files)
    assert len(dead_links) == 0, f"doc {docfile} has deadlinks: {dead_links}"


def test_2():
    """ test README links """
    dead_links = check_readme_links()
    assert len(dead_links) == 0, f"README has deadlines: {dead_links}"
