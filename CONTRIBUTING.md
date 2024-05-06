# Contributing to krixik documentation

Table of contents

- [Adding a new page to documentation](#adding-a-new-page-to-documentation)
- [Before pushing checklist](#before-pushing-checklist)
- [Testing overview](#testing-overview)


## Adding a new page to documentation

Each new page in documentation begins as a jupyter notebook.  This notebook is converted to markdown and tested before adding to official documentation.

If you want a notebook included in documentation / testing it **must** be 

- placed in a (subdirectory of) the `docs` directory
- referenced in `mkdocs.yml` at the base of this repository

Note that a valid reference listing in `mkdocks.yml` does not include `docs`, and starts with any subdirectory/path *after* `docs`.  For example, if a page called `my_new_demo.md` is located in `docs/demos/mydemos/my_new_demo.md` then its reference in `mkdocs.yml` should look like

- 'my new demo name': demos/mydemos/my_new_demo.md

Since your documentation will come from a jupyter notebook, make sure to have the corresponding notebook

demos/mydemos/my_new_demo.ipynb

in the same location.  You do **not** need to generate the associated markdown yourself - this will be done when tests are run.


Follow best practices in your notebook layout by abiding by the following content rules:

1.  Tag any cells you want removed / output removed when converted to markdown
    - `remove_output`: tag to remove cell output 
    - `remove_cell`: remove entire cell (input and output)
    - `ignore_test`: add to code cells you want ignored in testing
    - `raises-exception`: add to any code cell that should fail in testing
2.  Clean up your pipelines at the end of each notebook
    - Make sure your notebook ends with a python cell invoking `reset_pipeline` on any pipeline(s) created

## Before pushing checklist

- make sure all notebooks pass tests locally
- clean up the `data/output` directory - remove everything.  This directory is where all output from demo notebooks is directed so that users can easily see input-output.  If we do not clean it up before each push the data will aggregate.
- add any new pages to the `mkdocs` table of contents

WARNING: if you change the structure of the `mkdocs` table of contents beyond adding pages - e.g., its basic section - you may break step 1 of testing described below. 


## Testing overview

Tests should be run locally if any changes are made to documentation that are to be proposed for changes upstream.  Tests will be run on github with any changes merged to the main branch of documentation.

Documentation tests consist of the following steps

1.  the `mkdocs.yml` table of contents is analyzed, and all references to documentation pages are collected.  

A list of references to markdown files are gathered at this step.  For example, from a reference like this

- 'my new demo name': demos/mydemos/my_new_demo.md

the link 

demos/mydemos/my_new_demo.md

is collected.


2.  Reference to notebook check

The validity of all links in each page are checked.  These links come in three flavors.

1.  Intra page link: a link to a section in the page itself

These are typically in the table of contents of the page near the top.  They look like:

[a page section](#a-page-section)

2.  Inter-page links

These can be scattered throughout a page and link from one to another.  They look like

[a link to another page](subdir/some_other_page.md)

All subdirs must belong to the `docs` directory for these links.

3.  General web links

General web links look like

[an example web link](https://example.com)


3.  Notebook-unique pipeline check

All pipeline name(s) declared in a notebook must be unique to that notebook.  This is to avoid un-wanted collisions that could confuse new users when using multiple notebooks at the same time / fail tests unnecessarily.

At this step all pipeline name(s) from each notebook are collected and a check is made to ensure that no pipeline name is found two notebooks.


4.  Noteobook formatting

Next notebooks are formatted (using [ruff](https://github.com/astral-sh/ruff)).  This does not change the content of your notebook, it will just clean it up (e.g., remove un-needed spacing) and standardize it. 


5.  Link validation

All referenced notebooks are converted to markdown for link validation.  This includes

- local intra-page link validation: intra page links are validated.  These are typically links to sections of a page listed in the page's table of contents, and look like

[my demo section](#my-demo-section)


- local inter-page link validation: local links to documentation pages of the form [a local link](demos/mydemos/my_new_demo.md) are validated by checking that the linked-to file `demos/mydemos/my_new_demo.md` exists in its proposed location under the `docs` directory

- outbound links: any links to outbound sites like [my link](https://google.com) are checked using the `requests` library


6.  Notebook execution

Each notebook is executed and successful completion of each code cell *not* marked with the tag `ignore_test` is confirmed.

7.  Final markdown rendering

After all notebooks have passed the previous step they are converted again to markdown.

Each notebook must contain unique pipeilne name(s) - this is to avoid collision when testing / using other notebooks.

Tag any cells you want removed / output removed when converted to markdown
    - `remove_output`: tag to remove cell output 
    - `remove_cell`: remove entire cell (input and output)
    - `ignore_test`: add to code cells you want ignored in testing
    - `raises-exception`: add to any code cell that should fail in testing