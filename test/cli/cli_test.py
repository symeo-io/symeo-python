import os
import unittest
from typing import List

from symeo_python.cli.cli import DefaultCliAdapter
from symeo_python.cli.process_runner import ProcessRunnerPort
from symeo_python.configuration.config_loader import SYMEO_LOCAL_FILE, SYMEO_API_KEY
from symeo_python.configuration.config_parser import ConfigParserPort


class CliTest(unittest.TestCase):
    def test_should_parse_conf_from_yaml(self):
        # Given
        conf_parser_mock = ConfigParserAdapterMock()
        process_runner_adapter_mock = ProcessRunnerAdapterMock()
        cli_adapter = DefaultCliAdapter(conf_parser_mock, process_runner_adapter_mock)
        contract_path = "fake/config/contract/path"

        # When
        cli_adapter.generate_configuration_from_contract_file(contract_path)

        # Then
        self.assertEqual(contract_path, conf_parser_mock.configuration_path)
        self.assertIsNone(process_runner_adapter_mock.process)

    def test_should_prepare_env_with_api_key_and_run_sub_process(self):
        # Given
        conf_parser_mock = ConfigParserAdapterMock()
        process_runner_adapter_mock = ProcessRunnerAdapterMock()
        cli_adapter = DefaultCliAdapter(conf_parser_mock, process_runner_adapter_mock)
        api_key = "FAKE_API_KEY_111"
        api_url = "http://fake.111"
        sub_process = ["echo", "'Test1'"]
        cli_input_data = {
            "api_key": api_key,
            "api_url": api_url,
            "sub_process": sub_process,
        }

        # When
        cli_adapter.prepare_env_and_start_sub_process(cli_input_data)

        # Then
        self.assertEqual(sub_process, process_runner_adapter_mock.process)
        self.assertEqual(api_key, os.getenv(SYMEO_API_KEY))

    def test_should_prepare_env_with_local_file_and_run_sub_process(self):
        # Given
        conf_parser_mock = ConfigParserAdapterMock()
        process_runner_adapter_mock = ProcessRunnerAdapterMock()
        cli_adapter = DefaultCliAdapter(conf_parser_mock, process_runner_adapter_mock)
        config_values_path = "./fake_local_file_111.yml"
        api_url = "http://fake.111"
        sub_process = ["echo", "'Test2'"]
        cli_input_data = {
            "config_values_path": config_values_path,
            "api_url": api_url,
            "sub_process": sub_process,
        }

        # When
        cli_adapter.prepare_env_and_start_sub_process(cli_input_data)

        # Then
        self.assertEqual(sub_process, process_runner_adapter_mock.process)
        self.assertEqual(config_values_path, os.getenv(SYMEO_LOCAL_FILE))

    def test_should_raise_exception_for_missing_cli_input_data(self):
        # Given
        conf_parser_mock = ConfigParserAdapterMock()
        process_runner_adapter_mock = ProcessRunnerAdapterMock()
        cli_adapter = DefaultCliAdapter(conf_parser_mock, process_runner_adapter_mock)
        sub_process = ["echo", "'Test2'"]
        cli_input_data = {
            "sub_process": sub_process,
        }

        # When
        exception = None
        try:
            cli_adapter.prepare_env_and_start_sub_process(cli_input_data)
        except Exception as e:
            exception = e

        # Then
        self.assertEqual(
            str(exception), "Missing api_key/api_url or config_values_path"
        )


class ProcessRunnerAdapterMock(ProcessRunnerPort):

    process: str = None

    def run_process(self, process: List[str]) -> None:
        self.process = process


class ConfigParserAdapterMock(ConfigParserPort):
    configuration_path: str

    def generate_configuration(self, configuration_path: str) -> None:
        self.configuration_path = configuration_path
