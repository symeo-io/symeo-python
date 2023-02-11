import os
from hashlib import md5  # type: ignore
from mmap import ACCESS_READ, mmap  # type: ignore

from symeo_python.config.conf import Conf
from symeo_python.yaml.yaml_to_class_converter import YamlToClassAdapter


class ConfParser:

    __SUPPORTED_EXTENSIONS__ = [".yml", ".yaml"]
    __yaml_to_class_converter: YamlToClassAdapter

    def __init__(self, yaml_to_class_converter: YamlToClassAdapter):
        self.__yaml_to_class_converter = yaml_to_class_converter

    def load_configuration(self, configuration_path: str) -> Conf:
        if os.path.isfile(configuration_path) is False:
            raise Exception(f"Configuration file {configuration_path} not found")
        else:
            if self.__validate_file_extension(configuration_path):
                return self.__yaml_to_class_converter.parse_configuration_from_path(
                    configuration_path
                )
            else:
                raise Exception(
                    f"Wrong configuration file format for {configuration_path} . Only .yml and .yaml are accepted"
                )

    def __validate_file_extension(self, configuration_path):
        is_file_extension_supported = False
        for supported_extension in self.__SUPPORTED_EXTENSIONS__:
            if configuration_path.endswith(supported_extension):
                is_file_extension_supported = True
        return is_file_extension_supported

    @staticmethod
    def get_file_md5(file_path) -> str:
        with open(file_path) as file, mmap(  # type: ignore
            file.fileno(), 0, access=ACCESS_READ
        ) as file:
            return md5(file).hexdigest()  # type: ignore
