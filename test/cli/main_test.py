import unittest

from typer.testing import CliRunner  # type: ignore

from symeo_python.cli.main import cli


class MainTest(unittest.TestCase):
    def test_app(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["-k", "Test"])
        assert result.exit_code == 0
