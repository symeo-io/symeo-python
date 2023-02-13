import os

from symeo_python.cli.process_runner import ProcessRunnerPort
from symeo_python.config.conf_loader import (
    SYMEO_API_KEY,
    SYMEO_LOCAL_FILE,
)
from symeo_python.config.conf_parser import ConfParserPort


class CliPort:
    def generate_configuration_from_contract_file(self, config_contract: str):
        pass

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        pass


class DefaultCliAdapter(CliPort):
    def __init__(
        self, conf_parser_port: ConfParserPort, process_runner_port: ProcessRunnerPort
    ):
        self.__conf_parser_port = conf_parser_port
        self.__process_runner_port = process_runner_port

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.__conf_parser_port.generate_configuration(config_contract)

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        if "api_key" in cli_input_data:
            os.environ[SYMEO_API_KEY] = cli_input_data["api_key"]
        elif "config_values_path" in cli_input_data:
            os.environ[SYMEO_LOCAL_FILE] = cli_input_data["config_values_path"]
        else:
            raise Exception("Missing api_key or config_values_path")
        self.__process_runner_port.run_process(cli_input_data["sub_process"])