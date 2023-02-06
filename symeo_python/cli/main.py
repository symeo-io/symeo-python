import typer  # type: ignore

from symeo_python.cli.cli_adapter import DefaultCliAdapter

DEFAULT_CONFIG_FORMAT_PATH = "./symeo.config.yml"
DEFAULT_LOCAL_CONFIG_PATH = "./symeo.local.yml"
cli = typer.Typer(no_args_is_help=True)


@cli.command()
def generate_conf_and_run_command(
    api_key: str = typer.Option("", "--api-key", "-k"),
    config_contract: str = typer.Option(
        DEFAULT_CONFIG_FORMAT_PATH, "--config-contract", "-c"
    ),
    config_file: str = typer.Option(DEFAULT_CONFIG_FORMAT_PATH, "--config-file", "-f"),
):
    print(f"Hello {api_key} {config_contract} {config_file}")
    DefaultCliAdapter().parse_conf_file_and_load_configuration(
        api_key, config_contract, config_file
    )


if __name__ == "__main__":
    cli()
