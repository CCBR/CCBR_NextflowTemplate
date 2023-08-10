# Nextflow Template

CCBR template for creating Nextflow pipelines

This template takes inspiration from nektool[^1] and the nf-core template. If you plan to contribute your pipeline to nf-core, don't use this template -- instead follow their instructions[^2].

[^1]: nektool https://github.com/beardymcjohnface/nektool]
[^2]: instructions for nf-core pipelines https://nf-co.re/docs/contributing/tutorials/creating_with_nf_core

## Getting started

1. On GitHub, click "Use this template" and "Create a new repository".
1. Choose an owner and repository name.
1. Change all instances of `TOOL_NAME` throughout the repo with the actual tool name. Places include: 
    - `README.md`
    - `pyproject.toml`
    - `src/TOOL_NAME`
    - `src/TOOL_NAME/CITATION`
    - `src/TOOL_NAME/__main__.py`
1. Edit `pyproject.toml` with correct information for your tool. You will likely need to change:
    - author names and emails
    - dependencies
    - project URLs
1. Write your nextflow workflow in `src/TOOL_NAME/workflow`.
1. Write your documentation in `docs/`.

You can look for instances of `TOOL_NAME` in case you missed any with grep:
```sh
grep -r "TOOL_NAME" *
```

## Usage

Install the tool in edit mode:
```sh
pip3 install -e . 
```

Run the example
```sh
TOOL_NAME run --input "Hello world"
```

## Maintaining your tool

- Increment the version number following semantic versioning[^3] in `src/TOOL_NAME/VERSION`
- Keep the changelog up to date with any user-facing changes in `CHANGELOG.md`

[^3]: semantic versioning guidelines https://semver.org/
