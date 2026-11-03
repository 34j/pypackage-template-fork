# Python Package Template

[![CI Status](https://img.shields.io/github/actions/workflow/status/browniebroke/pypackage-template/ci.yml?branch=main&label=Test&logo=github&style=flat-square)](https://github.com/browniebroke/pypackage-template/actions/workflows/ci.yml?query=branch%3Amain)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

Project template for a Python Package using Copier.

## Features

- Project for Python 3.12+.
- Testing with Pytest using GitHub actions.
- Packaging powered by [uv].
- Optionally generates a CLI entry point powered by [Cyclopts].
- Uses [Ruff] for formatting and linting.
- Comes with [prek] hook config for [Ruff].
- Style guide enforced on CI.
- Dependencies kept up to date by [Renovate].
- Follow to [the conventional commits][conventional-commits] specification.
- Automated releasing using [python-semantic-release][python-semantic-release].
- Documentation configured with Sphinx and [MyST Parser][myst].
- Follows the contributor covenant code of conduct.
- Standardised list of GitHub labels synchronised on push to master using [the labels CLI][pylabels].

## Usage

Generate a new project with:

```shell
copier copy --trust "gh:browniebroke/pypackage-template" path-to-project
```

This will prompt you for a few questions and create new directory with the name you used as project slug.

> _Note:_
> the `--trust` option is required because this template may execute some tasks after generating the project, like initialising the git repo, installing dependencies and so forth. These are all listed in the `copier.yml` of this repo, under the `_tasks` key. They are all optional and safe to run. You can take my word for it, or better, check the code yourself!

### Start developing

The project uses [uv] for dependencies management and packaging. Make sure you have it installed in your development machine. To install the development dependencies in a virtual environment, type:

```shell
uv sync
```

This will also generate a `uv.lock` file, you should track this file in version control. To execute the test suite, call pytest inside uv's virtual environment via `uv run`:

```shell
uv run pytest
```

Check out the [uv] documentation for more information on the available commands.

### GitHub Actions

When you first push to GitHub, it'll start a `ci` GitHub workflow that you can see in the "Actions" tab of your repository. This workflow runs a couple of jobs:

- The `test` job derives its Python-version matrix from the version-specific classifiers in `pyproject.toml`.
- A few things will run in the lint job:
  - Ruff format
  - Ruff lint with several flake8, isort and pyupgrade plugins.

A `labels` workflow will also run and synchronise the GitHub labels from the shared configuration.

### Automated release

By following the conventional commits specification, we're able to completely automate versioning and releasing to PyPI. It runs on every push to your main branch, as part of the `release` job of the `ci.yml` workflow. You shouldn't need to create a token, but you'll need to setup [trusted publisher](https://docs.pypi.org/trusted-publishers/using-a-publisher/) for the project.

#### Trusted publisher setup

The first time you push, the workflow will try to create a release in PyPI, however the project doesn't exist there yet, which seems like a chicken and egg situation. Luckily, you can add a trusted publisher before creating the PyPI project here: https://pypi.org/manage/account/publishing/. Here are the infos that you should use:

- PyPI project name: what you've entered as "project slug"
- Owner: your GitHub username
- Repository name: what you've entered as "project slug"
- Workflow name: `ci.yml`
- Environment name: `release`

If the release phase failed the first time, you might have to remove the release and tag from GitHub, and perhaps tidy up the changelog.

#### How it works

Here is an overview of what it's doing:

- Check the commit log since the last release, and determine the next version to be released.
- If no significant change detected, stop here (e.g. just dependencies update).
- Otherwise, bump the version in code locations specified in `setup.cfg`.
- Update the `CHANGELOG.md` file.
- Commit changes.
- Create a git tag.
- Push to GitHub.
- Create a release in GitHub with the changes as release notes.
- Build the source and binary distribution (wheel).
- Upload the sources to PyPI and attach them to the Github release, using trusted publisher.

For more details, check out the [conventional commits website][conventional-commits] and [Python semantic release][python-semantic-release] GitHub action.

### Prek

The project comes with the config for [prek]. If you're not familiar with it, follow their documentation on how to install it and set it up.

### Documentation

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST parser for Sphinx][myst].

To enable it, you might need to go [into your dashboard][rtd-dashboard] and import the project from Github. Everything else should work out of the box.

### Dependencies update

The project dependencies are kept up to date with [Renovate] which requires [the Github app][renovate-gh-app] to be installed.

The main advantage of Renovate over Dependabot is the auto-merge option, which is configured to automatically merge minor/patch updates with all the CI checks passing. It supports a variety of package managers, including uv, GitHub actions and pre-commit hooks (used by prek) which are used by default.

[uv]: https://docs.astral.sh/uv/
[Cyclopts]: https://cyclopts.readthedocs.io/
[Ruff]: https://pypi.org/project/ruff/
[prek]: https://prek.j178.dev/
[renovate]: https://docs.renovatebot.com/
[renovate-gh-app]: https://github.com/apps/renovate
[conventional-commits]: https://www.conventionalcommits.org
[python-semantic-release]: https://github.com/relekang/python-semantic-release
[myst]: https://myst-parser.readthedocs.io
[pylabels]: https://github.com/hackebrot/labels
[pypi]: https://pypi.org/
[rtd-dashboard]: https://readthedocs.org/dashboard/
