import yaml  # type: ignore


class YamlToClassConverter:

    # f"{os.path.dirname(os.path.abspath(__file__))}/conf.py"
    __target_file_path: str
    __ROOT_CONFIG_CLASS_NAME = "Conf"
    __TAB = "    "

    def __init__(self, target_file_path: str):
        self.__target_file_path = target_file_path

    def parse_configuration_from_path(self, configuration_path):
        with open(configuration_path, "r") as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            class_definition = self.__yaml_data_to_class(
                yaml_data, self.__ROOT_CONFIG_CLASS_NAME
            )
            with open(self.__target_file_path, "w") as file:
                file.write(class_definition)

    def __yaml_to_attributes_and_nested_classes(self, yaml_data):
        attributes = ""
        nested_classes = ""
        for key in yaml_data:
            attribute_name = str(key).replace("-", "_")
            if "type" not in yaml_data[key].keys():
                nested_classes += self.__yaml_data_to_class(yaml_data[key], key)
                nested_class_name = self.__get_camel_cased_class_name(key)
                nested_classes += f"{attribute_name}: {nested_class_name}\n"
            else:
                attributes += (
                    f"    {attribute_name}: {self.__get_type(yaml_data[key]['type'])}\n"
                )
        return attributes, nested_classes

    def __yaml_data_to_class(self, yaml_data: dict, class_name: str) -> str:
        attributes, nested_classes = self.__yaml_to_attributes_and_nested_classes(
            yaml_data
        )
        camel_case_class_name = self.__get_camel_cased_class_name(class_name)
        class_definition = f"class {camel_case_class_name}:\n{attributes}"
        if nested_classes != "":
            for line in nested_classes.split("\n"):
                if line == "":
                    class_definition += line
                else:
                    class_definition += f"{self.__TAB}{line}\n"
        return class_definition

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
