# Change Log
All notable changes to this project will be documented in this file.
 
## 2024-07-11

Link check test updated to deal with "?" symbols in intra doc links.


## 2024-07-10

OCR example output length snipped, collab cells hidden from example markdown files.

### Changed

- single module OCR output snipped
- collab cells hidden in module example docs


## 2024-07-09

New docs urls, spanish draft added.

### Added

New docs url for es added:

- es: https://krixik-docs.readthedocs.io/es-main/


### Changed

Docs url for en changed:

- en: https://krixik-docs.readthedocs.io/latest/




## Collab tabs - 2024-06-05

Collab tabs added, general cleanup of index and readme.

### Added

- Collab tabs have been added to all notebooks that have data-driven running code blocks

- a new variable `data_dir` replaces all relative paths in said notebooks


### Changed

- References to "cli" updated to "client" in readme and index of docs

- docs/system/initialization/install_cli.ipynb --> docs/system/initialization/install_client.ipynb 

- readme verbage update ("secure python apis" --> "secure apis")

- process_output in docs/examples/single_module_examples/single_transcribe.ipynb shortened

## Version update [1.1.17] - 2024-05-28

New page  - adding_your_own_modules_or_models - added for supply side.  Link check test updated to accept certain 400 errors.

### Added

- New "adding your own modules" teaser page under modules 


### Changed

- Link check tests updated to accept 403 (permission) and 429 (too many requests) errors - which can arise when requests-driven test requests deemed bots by receiver.


### Fixed

- Link check intra link failure on README check test.


## [1.1.17] - 2024-05-23

Subset of local tests mapped to github actions.

Release number matching current cli.


### Added

Subset of local tests - covering document link / data / pipeline naming checks - added to github for main merge.



## [Unreleased] - 2024-05-22

Second draft of docs completed and all local tests pass.


### Added

Local tests for data linkage checking.

### Changed

All docs updated to second draft.



## [Unreleased] - 2024-05-15
  
Tests added for local evaluation.

### Added

First draft of all local tests added and pass.

### Changed

Documentation updates to adhere to tests.



## [Unreleased] - 2024-05-03
 
Initial push with first drafts pushed.
 
### Added

First drafts.
 
