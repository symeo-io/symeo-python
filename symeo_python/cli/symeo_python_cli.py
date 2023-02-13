import os
from pathlib import Path
from typing import List

from typer import Option, Typer, get_app_dir  # type: ignore

from symeo_python.cli.cli import CliPort

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
                f"Starting to generate Config class from configuration contract {config_contract_path}"
            )
            self.__cli_port.generate_configuration_from_contract_file(
                str(config_contract_path)
            )

        @cli.command()
        def start(
            sub_process: List[str],
            api_key: str = Option("", "--api-key", "-k"),
            config_contract: str = Option(
                DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
            ),
            config_values: str = Option(
                DEFAULT_LOCAL_CONFIG_PATH, "--config-values", "-f"
            ),
        ):
            print(
                f"api_key={api_key} config_contract={config_contract} config_values={config_values} sub_command={' '.join(sub_process)}"
            )
            config_contract_path: Path = Path(os.getcwd()) / config_contract
            config_values_path: Path = Path(os.getcwd()) / config_values
            cli_input_data = {
                "config_contract_path": str(config_contract_path),
                "config_values_path": str(config_values_path),
                "sub_process": sub_process,
            }
            if api_key != "":
                cli_input_data["api_key"] = api_key
            self.__cli_port.prepare_env_and_start_sub_process(cli_input_data)

        return cli
