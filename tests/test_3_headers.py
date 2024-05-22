from utilities.header_check import check_file_headers
from utilities.converter import collect_mkdocks_toc
from utilities.link_check import check_file_links
import pytest


toc_files = collect_mkdocks_toc()


@pytest.mark.parametrize("docfile", toc_files)
def test_1(docfile):
    """success test that all headers from each notebook are valid"""
    dead_links = check_file_headers(docfile)
    assert len(dead_links) == 0, f"doc {docfile} has dead headers: {dead_links}"