from typer.testing import CliRunner  # type: ignore

from symeo_python.cli.main import cli

runner = CliRunner()


def test_app():
    result = runner.invoke(cli, ["-k", "Test"])
    assert result.exit_code == 0
