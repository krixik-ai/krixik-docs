# Contributing to krixik documentation

Table of contents

- [Adding a new page to documentation](#adding-a-new-page-to-documentation)
- [Before pushing checklist](#before-pushing-checklist)
- [Testing overview](#testing-overview)

Python 3.10 or later is required to build and run documentation tests.


## Adding a new page to documentation

Each new page in documentation begins as a jupyter notebook.  This notebook is converted to markdown and tested before adding to official documentation.

If you want a notebook included in documentation / testing it **must** be 

- placed in a (subdirectory of) the `docs` directory
- reference your page in `mkdocs.yml` at the base of this repository

Note that a valid reference listing in `mkdocks.yml` does not include `docs`, and starts with any subdirectory/path *after* `docs`.  For example, if a page called `my_new_demo.md` is located in `docs/demos/mydemos/my_new_demo.md` then its reference in `mkdocs.yml` should look like

- 'my new demo name': demos/mydemos/my_new_demo.md

Since your documentation will come from a jupyter notebook, make sure to have the corresponding notebook

demos/mydemos/my_new_demo.ipynb

in the same location.  You do **not** need to generate the associated markdown yourself - this will be done when tests are run.

**Do not leave any notebook in docs that you do not want run during tests.**


Follow best practices in your notebook layout by abiding by the following content rules:

1.  Tag any cells you want removed / output removed when converted to markdown
    - `remove_output`: tag to remove cell output when converting to markdown
    - `remove_cell`: remove entire cell (input and output) when converting to markdown
    - `skip-execution`: add to code cells you want ignored in testing notebook
    - `raises-exception`: add to any code cell that should fail in testing notebook
2.  Clean up your pipelines at the end of each notebook
    - Make sure your notebook ends with a python cell invoking `reset_pipeline` on any pipeline(s) created (this will be tested and if you do not do this your tests will  fail)
3.  Direct `local_save_directory` for `process` or `.fetch_output` return files to `data/output`.  This output should be pushed along with new pages - this is so any user who views your page can also examine the corresponding output


## Before pushing checklist

- make sure all notebooks pass tests locally
- clean up the `data/output` directory - remove everything.  This directory is where all output from demo notebooks is directed so that users can easily see input-output.  If we do not clean it up before each push the data will aggregate.
- cleanup the `data/pipeline_configs` directory - remove everything.  This directory is where all saved configs from documentation are stored.
- add any new pages to the `mkdocs` table of contents


WARNING: if you change the structure of the `mkdocs` table of contents beyond adding pages - e.g., its basic section - you may break step 1 of testing described below. 


## Testing overview

Tests should be run locally if any changes are made to documentation that are to be proposed for changes upstream.  Tests will be run on github with any changes merged to the main branch of documentation.

Documentation tests consist of the following steps

0.  Noteobook formatting

Next notebooks are formatted (using [ruff](https://github.com/astral-sh/ruff)).  This does not change the content of your notebook, it will just clean it up (e.g., remove un-needed spacing) and standardize it. 


1.  Initial notebook conversion

The toc from the `mkdocs.yml` is examined.  The notebook associated with each markdown file found is converted to markdown - with all "remove_cell" tags ignored.  

This initial conversion is done so that the tests that follow  - tests 2- 4  (the toc_file_check, links check, and names check) - can be performed.

The "remove_cell" tags are ignored so that the reset test (test 5) can be performed properly.


2.  Toc - docs check

This test cross-references the markdown files named in the `mkdocks.yml` toc with those present in the `docs/` directory.

If any entries in the `mkdocks.yml` toc are not found in `docs/` and vice-versa - the test fails.


3.  Link checking

The validity of all links in each page are checked.  These links come in three flavors. 

A.  Intra page link: a link to a section in the page itself

These are typically in the table of contents of the page near the top.  They look like:

[a page section](#a-page-section)

B.  Inter-page links

These can be scattered throughout a page and link from one to another.  They look like

[a link to another page](subdir/some_other_page.md)

All subdirs must belong to the `docs` directory for these links.

**IMPORTANT:** all inter-page links must be relative - absolute links [are not supported yet](https://www.mkdocs.org/user-guide/writing-your-docs/).

C.  General web links

General web links look like

[an example web link](https://example.com)


4.  Notebook-unique pipeline check

All pipeline name(s) declared in a notebook must be unique to that notebook.  This is to avoid un-wanted collisions that could confuse new users when using multiple notebooks at the same time / fail tests unnecessarily.

At this step all pipeline name(s) from each notebook are collected and a check is made to ensure that no pipeline name is found two notebooks.


5.  Data link check

A similar check to 4 - only on links to data input into pipelines.  This check is done in two ways:

- all pages are scanned, any link containing the required "/data/input/" is checked to ensure the corresponding file exists in the /data/input/ directory.  this helps ensure every page links to a real file in the data/input directory

- the /data/input/ directory is examined, if any file is un-used in all pages it is flagged.  this helps ensure that the data/input directory contains only files used in pages.



6.  Reset end

To prevent pipeline collisions and general good practice cleanup the final code cell in every notebook containing a `create_pipeline` invoccation should end with `.reset_pipeline`.

We test that the final code cell of such notebooks contain

```python
reset_pipeline(...)
```

This cell is tagged with `remove_cell` and will be removed in the final markdown conversion.


7.  Notebook execution

Each notebook is executed and successful completion of each code cell *not* marked with the tag `ignore_test` is confirmed.


8.  Final markdown conversion

After all notebooks have passed the previous step they are converted again to markdown.  All `remove_cell` tags are obeyed.

