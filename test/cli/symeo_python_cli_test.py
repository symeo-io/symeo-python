import unittest

from typer.testing import CliRunner  # type: ignore

from symeo_python.cli.cli_adapter import CliPort
from symeo_python.cli.symeo_python_cli import (
    DEFAULT_CONFIG_FORMAT_PATH,
    SymeoPythonCli,
    DEFAULT_LOCAL_CONFIG_PATH,
)


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

    def test_should_run_cli_start_command_in_local_mode(self):
        # Given
        cli_adapter_mock = CliAdapterMock()
        cli = SymeoPythonCli(cli_adapter_mock).load_commands()
        runner = CliRunner()
        fake_sub_process = "fake sub_process"

        # When
        result = runner.invoke(cli, "start -- %s" % fake_sub_process)

        # Then
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            {
                "config_contract": DEFAULT_CONFIG_FORMAT_PATH,
                "config_file": DEFAULT_LOCAL_CONFIG_PATH,
                "sub_process": fake_sub_process.split(" "),
            },
            cli_adapter_mock.cli_input_data,
        )

    def test_should_run_cli_start_command_in_saas_mode(self):
        # Given
        cli_adapter_mock = CliAdapterMock()
        cli = SymeoPythonCli(cli_adapter_mock).load_commands()
        runner = CliRunner()
        fake_sub_process = "fake sub_process"
        fake_api_key = "API_111_222"

        # When
        result = runner.invoke(
            cli, "start -k %s -- %s" % (fake_api_key, fake_sub_process)
        )

        # Then
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            {
                "config_contract_path": DEFAULT_CONFIG_FORMAT_PATH,
                "config_values_path": DEFAULT_LOCAL_CONFIG_PATH,
                "sub_process": fake_sub_process.split(" "),
                "api_key": fake_api_key,
            },
            cli_adapter_mock.cli_input_data,
        )


class CliAdapterMock(CliPort):

    config_contract: str
    cli_input_data: dict

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.config_contract = config_contract

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        self.cli_input_data = cli_input_data
