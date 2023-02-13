from symeo_python.config.conf_loader import ConfLoaderPort
from symeo_python.config.conf_parser import ConfParserPort


class CliPort:
    def generate_configuration_from_contract_file(self, config_contract: str):
        pass

    def load_configuration_values(self, cli_input_data: dict):
        pass


class DefaultCliAdapter(CliPort):
    def __init__(
        self, conf_parser_port: ConfParserPort, conf_loader_port: ConfLoaderPort
    ):
        self.__conf_parser_port = conf_parser_port
        self.__conf_loader_port = conf_loader_port

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.__conf_parser_port.generate_configuration(config_contract)

    def load_configuration_values(self, cli_input_data: dict):
        pass
