import os
import shutil
import tempfile
import unittest

import yaml

from test.yaml_converter.resources.expected_python_files.complex_yaml_with_complex_class_name import (
    Config,
)

# import yaml  # type: ignore

from symeo_python.configuration.config_parser import ConfigParserAdapter
from symeo_python.yaml_converter.yaml_to_class_converter import YamlToClassAdapter


class YamlToClassConverterTest(unittest.TestCase):

    __temp_dir: str
    __current_absolute_path = os.path.dirname(os.path.abspath(__file__))

    def setUp(self) -> None:
        self.__temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.__temp_dir)

    def test_should_convert_simple_yaml_files(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_1.yml", "simple_yaml_1.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_2.yml", "simple_yaml_2.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_with_two_attributes.yml", "simple_yaml_with_two_attributes.py"
        )

    def test_should_convert_complex_yaml_files(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "yaml_with_nested_conf.yml", "yaml_with_nested_conf.py"
        )

    def test_should_convert_complex_name(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "yaml_with_complex_name.yml", "yaml_with_complex_name.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "complex_yaml_with_complex_class_name.yml",
            "complex_yaml_with_complex_class_name.py",
        )

    def test_should_load_complex_yaml_to_class(self):
        # Given
        yaml_file_name = "complex_yaml_with_complex_class_name.yml"
        given_conf_file = f"{self.__current_absolute_path}/resources/given_conf_yaml_files/{yaml_file_name}"

        with open(given_conf_file, "r") as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            config = Config(yaml_data)
            self.assertEqual(config.application_name, "symeo-python")
            self.assertEqual(
                config.infrastructure.database.mongo_db.url, "http://localhost"
            )
            self.assertEqual(config.infrastructure.database.mongo_db.port, 5132)
            self.assertEqual(config.infrastructure.name, "fake")
            self.assertEqual(config.infrastructure.github.api, "http://github.api.com")

    def __assert_generated_python_file_equals_expected_python_file(
        self, yaml_file_name, python_file_name
    ):
        given_yaml_file = f"{self.__current_absolute_path}/resources/given_contract_yaml_files/{yaml_file_name}"
        target_path = f"{self.__temp_dir}/%s" % python_file_name
        yaml_to_class_converter = YamlToClassAdapter(target_path)
        expected_python_file = f"{self.__current_absolute_path}/resources/expected_python_files/{python_file_name}"
        # When
        yaml_to_class_converter.parse_configuration_from_path(given_yaml_file)

        # Then
        self.assertEqual(
            ConfigParserAdapter.get_file_md5(expected_python_file),
            ConfigParserAdapter.get_file_md5(target_path),
        )
