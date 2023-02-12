import os
from pathlib import Path
from typing import List

from typer import Option, Typer, get_app_dir  # type: ignore

from symeo_python.cli.cli_adapter import CliPort

DEFAULT_CONFIG_FORMAT_PATH = "./symeo.config.yml"
DEFAULT_LOCAL_CONFIG_PATH = "./symeo.local.yml"


class SymeoPythonCli:
    __cli_port: CliPort

    def __init__(self, cli_port: CliPort):
        self.__cli_port = cli_port

    def load_commands(
        self,
    ) -> Typer:
        cli = Typer()

        @cli.command()
        def build(
            config_contract: str = Option(
                DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
            )
        ):
            config_contract_path: Path = Path(os.getcwd()) / config_contract
            print(
                f"Starting to generate Conf class from configuration contract {config_contract_path}"
            )
            self.__cli_port.generate_configuration_from_contract_file(
                str(config_contract_path)
            )

        @cli.command()
        def start(
            sub_command: List[str],
            api_key: str = Option("", "--api-key", "-k"),
            config_contract: str = Option(
                DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
            ),
            config_file: str = Option(
                DEFAULT_LOCAL_CONFIG_PATH, "--config-file", "-f"
            ),
        ):
            print(f"api_key={api_key} config_contract={config_contract} config_file={config_file} sub_command={' '.join(sub_command)}")
            cli_input_data = {
                "config_contract": config_contract,
                "config_file": config_file,
            }
            if api_key != "":
                cli_input_data.api_key = api_key


        return cli
