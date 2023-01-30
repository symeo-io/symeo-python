import unittest

from symeo_python.config.configuration_parser import ConfigurationParser


class ConfigurationParserTest(unittest.TestCase):
    def test_should_not_load_configuration_for_missing_file(self):
        # Given
        configuration_parser = ConfigurationParser()
        configuration_path = "fake"
        exception: Exception = None

        # When
        try:
            configuration_parser.load_configuration(configuration_path)
        except Exception as e:
            exception = e

        # Then
        self.assertIsNotNone(exception)
        self.assertEquals(
            f"Configuration file {configuration_path} not found", str(exception)
        )

    def test_should_not_load_configuration_for_file_not_in_yaml(self):
        # Given
        configuration_parser = ConfigurationParser()
        configuration_path = "resources/fake.json"

        exception: Exception = None

        # When
        try:
            configuration_parser.load_configuration(configuration_path)
        except Exception as e:
            exception = e

        # Then
        self.assertIsNotNone(exception)
        self.assertEquals(
            f"Wrong configuration file format for {configuration_path} . Only .yml and .yaml are accepted",
            str(exception),
        )
