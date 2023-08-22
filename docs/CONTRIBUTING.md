# Contributing to TOOL_NAME

TODO -- describe gitflow, require PRs...

## Use pre-commit hooks

Pre-commit can automatically format your code, check for spelling errors, etc. every time you commit.

Install [pre-commit](https://pre-commit.com/#installation) if you haven't already,
then run `pre-commit install` to install the hooks specified in `.pre-commit-config.yaml`.
Pre-commit will run the hooks every time you commit.

## Versions

Increment the version number following semantic versioning[^3] in the `VERSION` file.

[^3]: semantic versioning guidelines https://semver.org/

## Changelog

Keep the changelog up to date with all changes in `docs/CHANGELOG.md`.

## VS code extensions

If you use VS code, installing [nf-core extension pack](https://marketplace.visualstudio.com/items?itemName=nf-core.nf-core-extensionpack) is recommended.
