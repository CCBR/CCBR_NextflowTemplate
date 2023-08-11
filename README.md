# Nextflow Template

CCBR template for creating Nextflow pipelines

This template takes inspiration from nektool[^1] and the nf-core template. If you plan to contribute your pipeline to nf-core, don't use this template -- instead follow their instructions[^2].

[^1]: nektool https://github.com/beardymcjohnface/nektool
[^2]: instructions for nf-core pipelines https://nf-co.re/docs/contributing/tutorials/creating_with_nf_core

## Getting started

1. Create a new repository from this template using either of these options:
   - [**The GitHub web interface**](https://github.com/CCBR/CCBR_NextflowTemplate):
     Click "Use this template" and "Create a new repository", then choose an owner (CCBR) and the repository name as the new tool's name.
   - [**The GitHub command line interface**](https://cli.github.com/):
     ```sh
     gh repo create CCBR/TOOL_NAME \
        --description "One-line description of your tool" \
        --public \
        --template CCBR/CCBR_NextflowTemplate \
        --confirm
     ```
1. Change all instances of `TOOL_NAME` throughout the repo with the actual tool name. Places include:
   - `docs/CHANGELOG.md`
   - `mkdocs.yml`
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
1. Write your documentation in `docs/` and enable GitHub Pages.
   - In settings, go to General > Pages and select the `gh-pages` branch.
     mkdocs will build your site under the `gh-pages` branch, and GitHub Pages will make it available at `https://ccbr.github.io/TOOL_NAME`.

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

### Use pre-commit hooks

Pre-commit can automatically format your code, check for spelling errors, etc. every time you commit.

Install [pre-commit](https://pre-commit.com/#installation) if you haven't already,
then run `pre-commit install` to install the hooks specified in `.pre-commit-config.yaml`.
Pre-commit will run the hooks every time you commit.

### Versions

Increment the version number following semantic versioning[^3] in `src/TOOL_NAME/VERSION`

[^3]: semantic versioning guidelines https://semver.org/

### Changelog

Keep the changelog up to date with any user-facing changes in `docs/CHANGELOG.md`
