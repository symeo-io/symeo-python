import os
import shutil
import tempfile
import unittest
from typing import List
from unittest import mock

import yaml

from symeo_python.api_client.symeo_api_client import SymeoApiClientAdapter
from symeo_python.configuration.config_validator import ConfigValidatorAdapter


class ConfigurationValidatorTest(unittest.TestCase):
    __current_absolute_path = os.path.dirname(os.path.abspath(__file__))

    def setUp(self) -> None:
        self.__temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.__temp_dir)

    def test_should_validate_local_configuration(self):
        self.__should_successfully_validate_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values.yml")
        self.__should_successfully_validate_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values_without_optionals.yml")
        self.__should_successfully_validate_configuration_with_local_values("simple_contract_file_with_regex.yml",
                                                                            "simple_local_values_with_regex.yml")
        self.__should_successfully_validate_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values.yml")
        self.__should_successfully_validate_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_without_optionals.yml")
        self.__should_successfully_validate_configuration_with_local_values("complex_contract_file_with_regex.yml",
                                                                            "complex_local_values_with_regex.yml")

    def test_should_fetch_api_values_and_validate_configuration(self):
        self.__should_successfully_validate_configuration_with_api_values("simple_contract_file.yml",
                                                                          "simple_local_values.yml")

    def test_should_refuse_validation_for_configuration_with_local_values(self):
        expected_errors_1 = [
            f'The property [bold white]"vcs-provider.remote-vcs.github"[/bold white] of your configuration contract [bold red]is missing[/bold red] in your configuration values.']
        self.__should_refuse_validation_for_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_missing_contract_property.yml",
                                                                            expected_errors_1)
        expected_errors_2 = [
            f'Configuration property [bold white]"vcs-provider.local"[/bold white] has type [bold red]"<class \'int\'>"[/bold red] while configuration contract defined "vcs-provider.local" as [bold green]"boolean"[/bold green]',
            f'Configuration property [bold white]"vcs-provider.remote-vcs.github.api-url"[/bold white] has type [bold red]"<class \'float\'>"[/bold red] while configuration contract defined "vcs-provider.remote-vcs.github.api-url" as [bold green]"string"[/bold green]']
        self.__should_refuse_validation_for_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_wrong_type_property.yml",
                                                                            expected_errors_2)
        expected_errors_3 = [
            f'The property [bold white]"database.host"[/bold white] of your configuration contract [bold red]is missing[/bold red] in your configuration values.']
        self.__should_refuse_validation_for_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values_missing_contract_property.yml",
                                                                            expected_errors_3)
        expected_errors_4 = [
            f'Configuration property [bold white]"database.host"[/bold white] has type [bold red]"<class \'int\'>"[/bold red] while configuration contract defined "database.host" as [bold green]"string"[/bold green]']
        self.__should_refuse_validation_for_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values_wrong_type_property.yml",
                                                                            expected_errors_4)
        expected_errors_5 = [
            r'Configuration property [bold white]"user.email"[/bold white] with value "regex-error" does not match regex [bold green]"^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+).([a-zA-Z]{2,5})$"[/bold green] defined in contract']
        self.__should_refuse_validation_for_configuration_with_local_values("simple_contract_file_with_regex.yml",
                                                                            "simple_local_values_wrong_regex.yml",
                                                                            expected_errors_5)
        expected_errors_6 = [
            r'Configuration property [bold white]"user.email"[/bold white] with value "toto.test" does not match regex [bold green]"^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+).([a-zA-Z]{2,5})$"[/bold green] defined in contract',
            r'Configuration property [bold white]"user.password"[/bold white] with value "passw0rd123!" does not match regex [bold green]"^[a-zA-Z0-9]+$"[/bold green] defined in contract'
        ]
        self.__should_refuse_validation_for_configuration_with_local_values("complex_contract_file_with_regex.yml",
                                                                            "complex_local_values_wrong_regex.yml",
                                                                            expected_errors_6)

    def __should_refuse_validation_for_configuration_with_local_values(self, contract_file: str, values_file: str,
                                                                       expected_errors: List[str]):
        given_contract_file = f"{self.__current_absolute_path}/resources/given_contract_files/{contract_file}"
        api_client_adaptor = SymeoApiClientAdapter()
        config_validator = ConfigValidatorAdapter(api_client_adaptor)
        with mock.patch.dict(os.environ, {
            "SYMEO_LOCAL_FILE": f"{os.path.dirname(os.path.abspath(__file__))}/resources/given_values_files/{values_file}"},
                             clear=True):
            errors_for_validation = config_validator.validate_config_from_env(given_contract_file)
            for error in expected_errors:
                self.assertIn(error, errors_for_validation)

    def __should_successfully_validate_configuration_with_local_values(self, contract_file, values_file):
        given_contract_file = f"{self.__current_absolute_path}/resources/given_contract_files/{contract_file}"
        api_client_adaptor = SymeoApiClientAdapter()
        config_validator = ConfigValidatorAdapter(api_client_adaptor)
        with mock.patch.dict(os.environ, {
            "SYMEO_LOCAL_FILE": f"{os.path.dirname(os.path.abspath(__file__))}/resources/given_values_files/{values_file}"},
                             clear=True):
            errors_for_validation = config_validator.validate_config_from_env(given_contract_file)
            self.assertEqual(len(errors_for_validation), 0)

    def __should_successfully_validate_configuration_with_api_values(self, contract_file, values_file):
        given_contract_file = f"{self.__current_absolute_path}/resources/given_contract_files/{contract_file}"
        api_client_adaptor = SymeoApiClientAdapterMock()
        api_client_adaptor.mocked_return_value_path = f"{self.__current_absolute_path}/resources/given_values_files/{values_file}"
        config_validator = ConfigValidatorAdapter(api_client_adaptor)
        with mock.patch.dict(os.environ, {
            "SYMEO_API_KEY": "fake_api_key", "SYMEO_API_URL": "fake_api_url"
        }, clear=True):
            errors_for_validation = config_validator.validate_config_from_env(given_contract_file)
            self.assertEqual(len(errors_for_validation), 0)


class SymeoApiClientAdapterMock(SymeoApiClientAdapter):
    mocked_return_value_path: str

    def get_conf_values_for_api_key(self, api_url: str, api_key: str):
        with open(self.mocked_return_value_path, "r") as yaml_contract:
            return yaml.load(yaml_contract, Loader=yaml.FullLoader)
