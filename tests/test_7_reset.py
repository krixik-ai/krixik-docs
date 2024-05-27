import pytest
from utilities import base_dir
from utilities.name_check import get_code_from_markdown, load_md_doc
from utilities.converter import collect_mkdocks_toc

toc_paths = collect_mkdocks_toc()
success_data = [base_dir + "/docs/" + path for path in toc_paths if path if "index.md" not in path]


@pytest.mark.parametrize("docpath", success_data)
def test_1(docpath):
    """test that reset_pipeline is in final code block of input docfile markdown path"""
    markdown_content = load_md_doc(docpath)
    code_blocks = get_code_from_markdown(markdown_content)
    create_exist = False
    for block in code_blocks:
        if "krixik.create_pipeline" in block:
            create_exist = True
            break
    if create_exist:
        print(code_blocks[-1])
        assert "reset_pipeline(pipeline)" in code_blocks[-1], f".reset_pipeline not found in final code block of {docpath}"
