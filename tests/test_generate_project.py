from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def base_answers():
    return {
        "user_name": "Jeanne Deau",
        "github_user": "actions-user",
        "project_name": "Snake Farm",
        "project_short_description": "A sample Snake farming project.",
        "version": "0.0.1",
        "open_source_license": "MIT",
        "documentation": True,
        "run_uv_sync": False,
        "initial_commit": True,
        "setup_github": False,
        "setup_pre_commit": False,
    }


def _check_file_contents(
    file_path: Path,
    expected_strs: Sequence[str] = (),
    unexpect_strs: Sequence[str] = (),
):
    assert file_path.exists()
    file_content = file_path.read_text()
    for content in expected_strs:
        assert content in file_content
    for content in unexpect_strs:
        assert content not in file_content


def test_defaults_values(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
):
    dst_path = tmp_path / "snake-farm"
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert tmp_path.exists()
    _check_file_contents(
        dst_path / "README.md",
        ["# Snake Farm"],
    )
    _check_file_contents(
        dst_path / "pyproject.toml",
        [
            'name = "snake-farm"',
            'version = "0.0.0"',
            'license = "MIT"',
        ],
    )
    _check_file_contents(
        dst_path / "renovate.json",
        expected_strs=["https://github.com/34j/renovate-config/blob/main/python.json"],
    )


@pytest.mark.parametrize(
    ("license", "expect_exists", "expected_strs", "unexpected_strs"),
    [
        (
            "MIT",
            True,
            ["MIT License"],
            ["Apache License", "GNU GENERAL PUBLIC LICENSE"],
        ),
        (
            "Apache-2.0",
            True,
            ["Apache License"],
            ["MIT License", "GNU GENERAL PUBLIC LICENSE"],
        ),
        (
            "GPL-3.0-only",
            True,
            ["GNU GENERAL PUBLIC LICENSE"],
            ["MIT License", "Apache License"],
        ),
        (
            "Not open source",
            False,
            [],
            [],
        ),
    ],
)
def test_licenses(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    license: str,
    expect_exists: bool,
    expected_strs: list[str],
    unexpected_strs: list[str],
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "open_source_license": license},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    license_file = dst_path / "LICENSE"
    if expect_exists:
        _check_file_contents(
            license_file,
            expected_strs=expected_strs,
            unexpect_strs=unexpected_strs,
        )
    else:
        assert not license_file.exists()


@pytest.mark.parametrize("generate_doc", [True, False])
def test_documentation(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    generate_doc: bool,
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "documentation": generate_doc},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    if generate_doc:
        assert not (dst_path / "docs" / "index.md").exists()
        _check_file_contents(
            dst_path / ".readthedocs.yml",
            expected_strs=[
                "configuration: docs/conf.py",
                "method: uv",
                "command: sync",
                "- docs",
            ],
            unexpect_strs=['python: "3.13"'],
        )
        _check_file_contents(
            dst_path / "pyproject.toml",
            expected_strs=["docs = [", "sphinx", "myst-parser", "sphinx-math-dollar"],
            unexpect_strs=["[tool.sphinx]", 'project = "Snake Farm"', "copyright ="],
        )
        _check_file_contents(
            dst_path / "docs" / "conf.py",
            expected_strs=[
                "pyproject = tomllib.load(pyproject_file)",
                'line.removeprefix("# ").strip()',
                "package_path = next(",
                'app.connect("config-inited", generate_documentation_sources)',
                '"index.md": """```{include} ../README.md',
            ],
            unexpect_strs=["copyright ="],
        )
        assert not (dst_path / "docs" / "changelog.md").exists()
    else:
        assert not (dst_path / "docs").exists()
        assert not (dst_path / ".readthedocs.yml").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=["docs = [", "sphinx==", "myst-parser"],
        )


@pytest.mark.parametrize("has_cli", [True, False])
def test_cli(
    tmp_path: Path,
    base_answers: dict[str, str | bool],
    has_cli: bool,
):
    dst_path = tmp_path / "snake-farm"
    copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**base_answers, "has_cli": has_cli},
        defaults=True,
        unsafe=True,
    )

    assert tmp_path.exists()
    if has_cli:
        _check_file_contents(
            dst_path / "src" / "snake_farm" / "__main__.py",
            expected_strs=["app()"],
        )
        _check_file_contents(
            dst_path / "src" / "snake_farm" / "cli.py",
            expected_strs=["app = App()"],
        )
        _check_file_contents(
            dst_path / "pyproject.toml",
            expected_strs=['scripts.snake-farm = "snake_farm.cli:app"'],
        )
    else:
        assert not (dst_path / "src" / "snake_farm" / "__main__.py").exists()
        assert not (dst_path / "src" / "snake_farm" / "cli.py").exists()
        _check_file_contents(
            dst_path / "pyproject.toml",
            unexpect_strs=['scripts.snake-farm = "snake_farm.cli:app"'],
        )
