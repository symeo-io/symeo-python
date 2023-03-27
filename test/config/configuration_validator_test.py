import os
import shutil
import tempfile
import unittest
from typing import List
from unittest import mock
from unittest.mock import MagicMock

import faker
import yaml

from symeo_python.api_client.symeo_api_client import SymeoApiClientAdapter
from symeo_python.configuration.config_loader import SYMEO_API_KEY
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
        self.__should_successfully_validate_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values.yml")
        self.__should_successfully_validate_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_without_optionals.yml")

    def test_should_fetch_api_values_and_validate_configuration(self):
        self.__should_successfully_validate_configuration_with_api_values("simple_contract_file.yml",
                                                                          "simple_local_values.yml")

    def test_should_refuse_validation_for_configuration_with_local_values(self):
        expected_errors_1 = [
            f'The property "vcs-provider.remote-vcs.github" of your configuration contract is missing in your configuration values.']
        self.__should_refuse_validation_for_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_missing_contract_property.yml",
                                                                            expected_errors_1)
        expected_errors_2 = [
            f'Configuration property "vcs-provider.local" has type "<class \'int\'>" while configuration contract defined "vcs-provider.local" as "boolean"',
            f'Configuration property "vcs-provider.remote-vcs.github.api-url" has type "<class \'float\'>" while configuration contract defined "vcs-provider.remote-vcs.github.api-url" as "string"']
        self.__should_refuse_validation_for_configuration_with_local_values("complex_contract_file.yml",
                                                                            "complex_local_values_wrong_type_property.yml",
                                                                            expected_errors_2)
        expected_errors_3 = [
            f'The property "database.host" of your configuration contract is missing in your configuration values.']
        self.__should_refuse_validation_for_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values_missing_contract_property.yml",
                                                                            expected_errors_3)
        expected_errors_4 = [
            f'Configuration property "database.host" has type "<class \'int\'>" while configuration contract defined "database.host" as "string"']
        self.__should_refuse_validation_for_configuration_with_local_values("simple_contract_file.yml",
                                                                            "simple_local_values_wrong_type_property.yml",
                                                                            expected_errors_4)

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