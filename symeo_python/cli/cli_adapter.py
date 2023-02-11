from symeo_python.yaml.yaml_to_class_converter import YamlToClassPort


class CliPort:
    def generate_configuration_from_contract_file(self, config_contract: str):
        pass


class DefaultCliAdapter(CliPort):
    def __init__(self, yaml_to_class_port: YamlToClassPort):
        self.__yaml_to_class_port = yaml_to_class_port

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.__yaml_to_class_port.parse_configuration_from_path(config_contract)
