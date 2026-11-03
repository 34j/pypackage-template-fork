import tomllib
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.ext import apidoc

project_root = Path(__file__).parent.parent
with (project_root / "pyproject.toml").open("rb") as pyproject_file:
    pyproject = tomllib.load(pyproject_file)

project_metadata = pyproject["project"]
sphinx_metadata = pyproject["tool"]["sphinx"]

project = sphinx_metadata["project"]
copyright = sphinx_metadata["copyright"]
author = project_metadata["authors"][0]["name"]
release = project_metadata["version"]

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]
napoleon_google_docstring = False
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = [
    "_templates",
]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
html_theme = "furo"


def generate_documentation_sources(app: Sphinx, _: Any) -> None:
    """Create temporary Sphinx source pages."""
    sources = {
        "index.md": """```{include} ../README.md

```

```{toctree}
:caption: Project Info
:maxdepth: 2
:glob:

*
```
""",
        "changelog.md": "```{include} ../CHANGELOG.md\n```\n",
    }
    for name, content in sources.items():
        (Path(app.srcdir) / name).write_text(content, encoding="utf-8")


def cleanup_documentation_sources(app: Sphinx, _: Any) -> None:
    """Remove temporary Sphinx source pages."""
    for page in ("index.md", "changelog.md"):
        path = Path(app.srcdir) / page
        if path.exists():
            path.unlink()


def run_apidoc(_: Any) -> None:
    """Generate the API-reference source document."""
    docs_path = Path(__file__).parent
    module_path = project_root / "src" / sphinx_metadata["package"]
    apidoc.main(
        [
            "--force",
            "--module-first",
            "--no-toc",
            "-o",
            docs_path.as_posix(),
            module_path.as_posix(),
        ]
    )


def setup(app: Sphinx) -> None:
    """Register Sphinx build hooks."""
    app.connect("config-inited", generate_documentation_sources)
    app.connect("builder-inited", run_apidoc)
    app.connect("build-finished", cleanup_documentation_sources)
