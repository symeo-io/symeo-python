from pathlib import Path

from typer import Option, Typer, get_app_dir  # type: ignore

from symeo_python.cli.cli_adapter import CliPort

DEFAULT_CONFIG_FORMAT_PATH = "./symeo.config.yml"
DEFAULT_LOCAL_CONFIG_PATH = "./symeo.local.yml"


class SymeoPythonCli:
    __APP_NAME__ = "symeo-python"
    __cli_port: CliPort

    def __init__(self, cli_port: CliPort):
        self.__cli_port = cli_port

    def load_commands(
        self,
    ) -> Typer:
        cli = Typer(no_args_is_help=True)

        @cli.command("build")
        def build(
            config_contract: str = Option(
                DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
            )
        ):
            app_dir = get_app_dir(self.__APP_NAME__)
            config_contract_path: Path = Path(app_dir) / config_contract
            print(
                f"Starting to generate Conf class from configuration contract {config_contract_path}"
            )
            self.__cli_port.generate_configuration_from_contract_file(
                str(config_contract_path)
            )

        #
        # @cli.command("start")
        # def start(
        #     api_key: str = Option("", "--api-key", "-k"),
        #     config_contract: str = Option(
        #         DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
        #     ),
        #     config_file: str = Option(
        #         DEFAULT_CONFIG_FORMAT_PATH, "--config-file", "-f"
        #     ),
        # ):
        #     print(f"Hello {api_key} {config_contract} {config_file}")
        #     cli_input_data = {
        #         "config_contract": config_contract,
        #         "config_file": config_file,
        #     }
        #     if api_key != "":
        #         cli_input_data.api_key = api_key
        #     DefaultCliAdapter(
        #         YamlToClassAdapter()
        #     ).parse_conf_file_and_load_configuration(**cli_input_data)

        return cli
