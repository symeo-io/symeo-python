import os
import unittest

from symeo_python.config.conf_parser import ConfParser
from symeo_python.yaml.yaml_to_class_converter import YamlToClassAdapter


class ConfigurationParserTest(unittest.TestCase):

    __current_absolute_path = os.path.dirname(os.path.abspath(__file__))

    def test_should_not_load_configuration_for_missing_file(self):
        # Given
        configuration_parser = ConfParser(YamlToClassAdapter("fake"))
        configuration_path = "fake"
        exception: Exception = None

        # When
        try:
            configuration_parser.load_configuration(configuration_path)
        except Exception as e:
            exception = e

        # Then
        self.assertIsNotNone(exception)
        self.assertEqual(
            f"Configuration file {configuration_path} not found", str(exception)
        )

    def test_should_not_load_configuration_for_file_not_in_yaml(self):
        # Given
        configuration_parser = ConfParser(YamlToClassAdapter("fake"))
        configuration_path = f"{self.__current_absolute_path}/resources/not_supported_file_extension.json"

        exception: Exception = None

        # When
        try:
            configuration_parser.load_configuration(configuration_path)
        except Exception as e:
            exception = e

        # Then
        self.assertIsNotNone(exception)
        self.assertEqual(
            f"Wrong configuration file format for {configuration_path} . Only .yml and .yaml are accepted",
            str(exception),
        )

    def test_should_load_configuration(self):
        # Given
        yaml_to_class_converter_mock = YamlToClassAdapterMock("fake")
        configuration_parser = ConfParser(yaml_to_class_converter_mock)
        configuration_path = f"{self.__current_absolute_path}/resources/simple_yaml.yml"

        # When
        configuration_parser.load_configuration(configuration_path)

        # Then
        self.assertEqual(yaml_to_class_converter_mock.count, 1)


class YamlToClassAdapterMock(YamlToClassAdapter):

    count: int = 0

    def parse_configuration_from_path(self, configuration_path):
        self.count += 1