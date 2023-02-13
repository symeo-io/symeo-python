import unittest

from symeo_python.cli.cli_adapter import DefaultCliAdapter
from symeo_python.config.conf_loader import ConfLoaderPort
from symeo_python.config.conf_parser import ConfParserPort


class CliAdapterTest(unittest.TestCase):
    def test_should_parse_conf_from_yaml(self):
        # Given
        conf_parser_mock = ConfParserAdapterMock()
        conf_loader_mock = ConfLoaderAdapterMock()
        cli_adapter = DefaultCliAdapter(conf_parser_mock, conf_loader_mock)
        contract_path = "fake/config/contract/path"

        # When
        cli_adapter.generate_configuration_from_contract_file(contract_path)

        # Then
        self.assertEqual(contract_path, conf_parser_mock.configuration_path)


class ConfLoaderAdapterMock(ConfLoaderPort):
    pass


class ConfParserAdapterMock(ConfParserPort):
    configuration_path: str

    def generate_configuration(self, configuration_path: str) -> None:
        self.configuration_path = configuration_path
