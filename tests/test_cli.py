import tempfile
from pathlib import Path

from typer.testing import CliRunner

from abbsolve.cli.cli import app

runner = CliRunner()


def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_app_finds_candidate():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        (temp_dir_path / "file1.txt").write_text("HyperText Markup Language (HTML)")
        result = runner.invoke(app, ["HTML", "-d", temp_dir])
        assert result.exit_code == 0
        assert "HyperText Markup Language" in result.stdout


def test_app_finds_candidate_with_sources():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        file_path = temp_dir_path / "file1.txt"
        file_path.write_text("HyperText Markup Language (HTML)")
        result = runner.invoke(app, ["HTML", "-d", temp_dir, "--with-sources"])
        assert result.exit_code == 0
        assert "HyperText Markup Language:" in result.stdout
        assert str(file_path) in result.stdout


def test_app_no_candidates_found():
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(app, ["XYZ", "-d", temp_dir])
        assert result.exit_code == 0
        assert "No candidates found for 'XYZ'" in result.stdout


def test_app_value_error():
    result = runner.invoke(app, ["H", "-d", "."])
    assert result.exit_code == 1
    assert "Error: Initialism must be at least 2 characters long." in result.stderr
