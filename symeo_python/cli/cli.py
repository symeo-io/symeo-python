import os
from typing import List

import typer
from rich.console import Console
from rich.table import Table

from symeo_python.cli.process_runner import ProcessRunnerPort
from symeo_python.configuration.config_loader import (
    SYMEO_API_KEY,
    SYMEO_LOCAL_FILE,
    SYMEO_API_URL,
)
from symeo_python.configuration.config_parser import ConfigParserPort
from symeo_python.configuration.config_validator import ConfigValidatorPort


class CliPort:
    def generate_configuration_from_contract_file(self, config_contract: str):
        pass

    def prepare_env_and_start_validation(self, config_contract: str, cli_input_data: dict):
        pass

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        pass


class DefaultCliAdapter(CliPort):
    def __init__(
            self, conf_parser_port: ConfigParserPort, config_validator_port: ConfigValidatorPort,
            process_runner_port: ProcessRunnerPort
    ):
        self.__conf_parser_port = conf_parser_port
        self.__config_validator_port = config_validator_port
        self.__process_runner_port = process_runner_port

    def generate_configuration_from_contract_file(self, config_contract: str):
        self.__conf_parser_port.generate_configuration(config_contract)

    def prepare_env_and_start_validation(self, config_contract: str, cli_input_data: dict):
        self.__prepare_env(cli_input_data)
        errors: List[str] = self.__config_validator_port.validate_config_from_env(config_contract)
        if len(errors) > 0:
            console = Console()
            table = Table("N°", "Error", show_lines=True)
            for error in errors:
                table.add_row(str(errors.index(error) + 1), error)
            console.print(table)
            exit(1)
        print("Configuration values matching contract")

    def prepare_env_and_start_sub_process(self, cli_input_data: dict):
        self.__prepare_env(cli_input_data)
        self.__process_runner_port.run_process(cli_input_data["sub_process"])

    @staticmethod
    def __prepare_env(cli_input_data: dict) -> None:
        if "api_key" in cli_input_data and "api_url" in cli_input_data:
            os.environ[SYMEO_API_KEY] = cli_input_data["api_key"]
            os.environ[SYMEO_API_URL] = cli_input_data["api_url"]
        elif "config_values_path" in cli_input_data:
            os.environ[SYMEO_LOCAL_FILE] = cli_input_data["config_values_path"]
        else:
            raise Exception("Missing api_key/api_url or config_values_path")
