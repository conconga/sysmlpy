"""Repository-wide syntax smoke test for SysML files."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import pytest

from sysmlpy import loads, analyze


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", "__venv__"}


def _sysml_files() -> list[Path]:
    """Return every repository SysML file, excluding generated environments."""
    return sorted(
        path
        for path in PROJECT_ROOT.rglob("*.sysml")
        if not EXCLUDED_DIRECTORIES.intersection(path.relative_to(PROJECT_ROOT).parts)
    )


def test_all_sysml_files_parse():
    """Parse every ``*.sysml`` file and report syntax failures by path."""
    files = _sysml_files()
    assert files, f"No SysML files found below {PROJECT_ROOT}"

    failures: list[str] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
            # Some grammar classes print non-fatal diagnostics while loading.
            # Keep pytest output focused on actual parse failures.
            with contextlib.redirect_stdout(io.StringIO()):
                i = loads(text)
                analyze(i)
        except Exception as exc:  # noqa: BLE001 - report every parser issue
            relative_path = path.relative_to(PROJECT_ROOT)
            message = str(exc).strip() or "no error message"
            failures.append(f"{relative_path}: {type(exc).__name__}: {message}")

    if failures:
        pytest.fail(
            f"{len(failures)} of {len(files)} SysML files failed to parse:\n"
            + "\n".join(f"- {failure}" for failure in failures)
        )

