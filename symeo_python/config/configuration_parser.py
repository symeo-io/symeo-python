import os

from symeo_python.config.conf import Conf
from symeo_python.yaml.yaml_to_class_converter import YamlToClassConverter


class ConfigurationParser:

    __SUPPORTED_EXTENSIONS__ = [".yml", ".yaml"]
    __yaml_to_class_converter: YamlToClassConverter

    def __init__(self, yaml_to_class_converter: YamlToClassConverter):
        self.__yaml_to_class_converter = yaml_to_class_converter

    def load_configuration(self, configuration_path: str) -> Conf:
        if os.path.isfile(configuration_path) is False:
            raise Exception(f"Configuration file {configuration_path} not found")
        else:
            if self.validate_file_extension(configuration_path):
                return self.__yaml_to_class_converter.parse_configuration_from_path(
                    configuration_path
                )
            else:
                raise Exception(
                    f"Wrong configuration file format for {configuration_path} . Only .yml and .yaml are accepted"
                )

    def validate_file_extension(self, configuration_path):
        is_file_extension_supported = False
        for supported_extension in self.__SUPPORTED_EXTENSIONS__:
            if configuration_path.endswith(supported_extension):
                is_file_extension_supported = True
        return is_file_extension_supported
