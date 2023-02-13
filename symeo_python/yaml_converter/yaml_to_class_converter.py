import os
from typing import List

import yaml  # type: ignore


class YamlToClassPort:
    def parse_configuration_from_path(self, configuration_path):
        pass


class YamlToClassAdapter(YamlToClassPort):

    __target_file_path: str
    __ROOT_CONFIG_CLASS_NAME = "Config"
    __TAB = "    "

    def __init__(
        self,
        target_file_path: str = f"{os.path.dirname(os.path.abspath(__file__))}/../configuration/configuration.py",
    ):
        self.__target_file_path = target_file_path

    def parse_configuration_from_path(self, configuration_path):
        with open(configuration_path, "r") as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            class_definition = self.__yaml_data_to_class_with_mapping_methods(
                yaml_data, self.__ROOT_CONFIG_CLASS_NAME, []
            )
            with open(self.__target_file_path, "w") as file:
                print(f"Writing conf from contract to {configuration_path}")
                file.write(class_definition)

    def __yaml_data_to_class_with_mapping_methods(
        self, yaml_data: dict, class_name: str, nested_classes: List[str]
    ) -> str:
        attribute = ""
        constructor = f"{self.__TAB}def __init__(self, yaml_data):\n"
        (
            attribute,
            constructor,
        ) = self.__yaml_data_to_attribute_constructor_and_nested_classes(
            attribute, constructor, nested_classes, yaml_data
        )
        conf_class = ""
        if class_name == self.__ROOT_CONFIG_CLASS_NAME:
            python_conf_file_content = ""
            for nested_classe in nested_classes:
                python_conf_file_content += f"{nested_classe}\n\n"
            conf_class = python_conf_file_content
        conf_class += f"class {class_name}:\n{attribute}\n{constructor}"
        return conf_class

    def __yaml_data_to_attribute_constructor_and_nested_classes(
        self, attribute, constructor, nested_classes, yaml_data
    ):
        for key in yaml_data:
            attribute_name = str(key).replace("-", "_")
            if "type" in yaml_data[key]:
                constructor += f'{self.__TAB}{self.__TAB}self.{attribute_name} = yaml_data["{key}"]\n'
                type = self.__get_type(yaml_data[key]["type"])
                attribute += f"{self.__TAB}{attribute_name}: {type}\n"
            else:
                nested_class_name = self.__get_camel_cased_class_name(key)
                constructor += f'{self.__TAB}{self.__TAB}self.{attribute_name} = {nested_class_name}(yaml_data["{key}"])\n'
                nested_classes.append(
                    self.__yaml_data_to_class_with_mapping_methods(
                        yaml_data[key], nested_class_name, nested_classes
                    )
                )
                attribute += f"{self.__TAB}{attribute_name}: {nested_class_name}\n"
        return attribute, constructor

    @staticmethod
    def __get_camel_cased_class_name(class_name):
        camel_case_class_name = ""
        if "-" in class_name:
            for sub_name in class_name.split("-"):
                camel_case_class_name += sub_name.capitalize()
        else:
            camel_case_class_name = class_name.capitalize()
        return camel_case_class_name

    @staticmethod
    def __get_type(type: str) -> str:
        if type == "string":
            return "str"
        elif type == "integer":
            return "int"
        raise Exception(f"Wrong type {type}")
