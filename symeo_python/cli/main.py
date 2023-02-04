import typer  # type: ignore

DEFAULT_CONFIG_FORMAT_PATH = "./symeo.config.yml"
DEFAULT_LOCAL_CONFIG_PATH = "./symeo.local.yml"
cli = typer.Typer(no_args_is_help=True)


@cli.command()
def generate_conf_and_run_command(
    env_key: str = typer.Option(..., "--env_key", "-k"),
    file: str = typer.Option(DEFAULT_CONFIG_FORMAT_PATH, "--file", "-f"),
    env_file: str = typer.Option(DEFAULT_CONFIG_FORMAT_PATH, "--env_file", "-e"),
):
    print(f"Hello {file} {env_key} {env_file}")


if __name__ == "__main__":
    cli()
