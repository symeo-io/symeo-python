import os
from pathlib import Path
from typing import List

from typer import Option, Typer  # type: ignore

from symeo_python.cli.cli import CliPort

DEFAULT_CONFIG_CONTRACT_PATH = "./symeo.config.yml"
DEFAULT_CONFIG_VALUES_PATH = "./symeo.local.yml"
DEFAULT_SYMEO_API_URL = "https://api-staging.symeo.io/api/v1/values"


class SymeoPythonCli:
    __cli_port: CliPort

    def __init__(self, cli_port: CliPort):
        self.__cli_port = cli_port

    def load_commands(
        self,
    ) -> Typer:
        cli = Typer()

        def generate_config(config_contract):
            config_contract_path: Path = Path(os.getcwd()) / config_contract
            print(
                f"Starting to generate Config class from configuration contract {config_contract_path}"
            )
            self.__cli_port.generate_configuration_from_contract_file(
                str(config_contract_path)
            )

        @cli.command()
        def build(
            config_contract: str = Option(
                DEFAULT_CONFIG_CONTRACT_PATH, "--config-contract", "-c"
            )
        ):
            generate_config(config_contract)

        @cli.command()
        def start(
            sub_process: List[str],
            api_key: str = Option("", "--api-key", "-k"),
            api_url: str = Option(DEFAULT_SYMEO_API_URL, "--api-url", "-a"),
            config_values: str = Option(
                DEFAULT_CONFIG_VALUES_PATH, "--config-values", "-f"
            ),
            config_contract: str = Option(
                DEFAULT_CONFIG_CONTRACT_PATH, "--config-contract", "-c"
            ),
        ):
            generate_config(config_contract)
            config_values_path: Path = Path(os.getcwd()) / config_values
            cli_input_data = {
                "config_values_path": str(config_values_path),
                "sub_process": sub_process,
            }
            if api_key != "":
                cli_input_data["api_key"] = api_key
                cli_input_data["api_url"] = api_url
            self.__cli_port.prepare_env_and_start_sub_process(cli_input_data)

        return cli
