import re
from utilities.converter import collect_mkdocks_toc
from utilities import base_dir
from utilities.utilities import load_md_doc, get_code_from_markdown


def gather_pipeline_names(md_filepath: str) -> list:
    try:
        markdown_content = load_md_doc(md_filepath)
        code_blocks = get_code_from_markdown([markdown_content])
        create_pattern = r"\.create_pipeline\([^)]*\)"
        name_pattern = r'name="([^"]*)"'
        pipeline_names = []
        for block in code_blocks:
            create_matches = []
            create_matches = re.findall(create_pattern, block)
            if len(create_matches) > 0:
                name_matches = []
                for match in create_matches:
                    name_matches = re.findall(name_pattern, match)
                    for item in name_matches:
                        pipeline_names.append(item)
        if len(pipeline_names) > 0:
            pipeline_names = list(set(pipeline_names))
        return pipeline_names
    except Exception as e:
        raise Exception(f"FAILURE: gather_pipeline_names failed on file {markdown_file} with exception {e}")


def duplicate_name_check():
    try:
        # collect all paths to md docs
        all_docs = collect_mkdocks_toc()

        # collect all pipeline names
        all_names = []
        all_md_names = []
        for i in range(len(all_docs)):
            md_filepath = base_dir + "/docs/" + all_docs[i]
            pipeline_names = gather_pipeline_names(md_filepath)
            all_md_names.append(pipeline_names)
            for name in pipeline_names:
                all_names.append(name)

        # determine duplicates
        my_dict = {i: all_names.count(i) for i in all_names}
        keys = list(my_dict.keys())
        duplicates = [key for key in keys if my_dict[key] > 1]

        if len(duplicates) > 0:
            # gather all paths to mds containing duplicate pipeline names
            duplicates_dict = {v: [] for v in duplicates}

            for d in duplicates:
                for i in range(len(all_docs)):
                    docs_names = all_md_names[i]
                    if d in docs_names:
                        duplicates_dict[d].append(all_docs[i])

            print(f"FAILURE: the following pipeline names are found in multiple markdown docs: {duplicates_dict}")
            return False
        return True
    except Exception as e:
        print(f"FAILURE: duplicate_name_check failed with exception {e}")
        return False
