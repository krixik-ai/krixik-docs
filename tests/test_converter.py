import importlib
import pytest
collect_mkdocks_toc = importlib.import_module("krixik-docs.utilities.converter.collect_mkdocks_toc").collect_mkdocks_toc()
convert_all_notebooks = importlib.import_module("krixik-docs.utilities.converter.convert_all_notebooks").convert_all_notebooks()


def test_1():
    """success test that notebook to markdown conversion"""
    convert_all_notebooks()


