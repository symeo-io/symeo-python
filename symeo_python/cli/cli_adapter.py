import os
import subprocess

from symeo_python.config.conf_loader import ConfLoaderPort, SYMEO_API_KEY, SYMEO_LOCAL_FILE
from symeo_python.config.conf_parser import ConfParserPort


class CliPort:
    def generate_configuration_from_contract_file(self, config_contract: str):
        pass

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        pass


class DefaultCliAdapter(CliPort):
    def __init__(
        self, conf_parser_port: ConfParserPort, conf_loader_port: ConfLoaderPort
    ):
        self.__conf_parser_port = conf_parser_port
        self.__conf_loader_port = conf_loader_port

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.__conf_parser_port.generate_configuration(config_contract)

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        if "api_key" in cli_input_data:
            os.environ[SYMEO_API_KEY] = cli_input_data["api_key"]
        else:
            os.environ[SYMEO_LOCAL_FILE] = cli_input_data["config_values_path"]
        subprocess.run(cli_input_data["sub_process"])
