from utilities.toc_file_check import compare_toc_to_docs


def test_1():
    """check that listing of mds in toc matches mds in docs/ and all subdirs"""
    in_toc_no_docs, in_docs_no_toc = compare_toc_to_docs()

    assert len(in_toc_no_docs) == 0, f"the following md files were found in mkdocs toc but not in docs/: {in_toc_no_docs}"
    assert len(in_docs_no_toc) == 0, f"the following md files were found in docs/ but not in mkdocks toc: {in_docs_no_toc}"
