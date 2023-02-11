import unittest

from typer.testing import CliRunner  # type: ignore

from symeo_python.cli.cli_adapter import CliPort
from symeo_python.cli.symeo_python_cli import (DEFAULT_CONFIG_FORMAT_PATH,
                                               SymeoPythonCli)


class MainTest(unittest.TestCase):
    def test_should_run_cli_build_command(self):
        # Given
        cli_adapter_mock = CliAdapterMock()
        cli = SymeoPythonCli(cli_adapter_mock).load_commands()
        runner = CliRunner()

        # When
        result = runner.invoke(cli, "build")

        # Then

        self.assertTrue(
            cli_adapter_mock.config_contract.endswith(
                DEFAULT_CONFIG_FORMAT_PATH.replace("./", "")
            )
        )
        self.assertEqual(0, result.exit_code)


class CliAdapterMock(CliPort):

    config_contract: str

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.config_contract = config_contract
